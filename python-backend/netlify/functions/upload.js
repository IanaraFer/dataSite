// Lightweight multipart parser (avoid broken package main)
function parseMultipartBody(bodyBuffer, boundary) {
  const boundaryBuffer = Buffer.from(`--${boundary}`);
  const endBoundaryBuffer = Buffer.from(`--${boundary}--`);
  const parts = [];
  let start = bodyBuffer.indexOf(boundaryBuffer) + boundaryBuffer.length + 2; // skip CRLF
  while (start >= boundaryBuffer.length + 2 && start < bodyBuffer.length) {
    const end = bodyBuffer.indexOf(boundaryBuffer, start);
    const endAlt = bodyBuffer.indexOf(endBoundaryBuffer, start);
    const partEnd = end === -1 ? endAlt : Math.min(end, endAlt === -1 ? Infinity : endAlt);
    if (partEnd === -1) break;
    const part = bodyBuffer.slice(start, partEnd - 2); // strip trailing CRLF
    const headerEnd = part.indexOf(Buffer.from('\r\n\r\n'));
    const headersBuf = part.slice(0, headerEnd).toString();
    const content = part.slice(headerEnd + 4);
    const dispositionMatch = headersBuf.match(/Content-Disposition:\s*form-data;\s*name="([^"]+)"(?:;\s*filename="([^"]+)")?/i) || headersBuf.match(/Content-Disposition:.*name="([^"]+)"(?:;\s*filename="([^"]+)")?/i);
    const typeMatch = headersBuf.match(/Content-Type:\s*([^\r\n]+)/i);
    const name = dispositionMatch ? dispositionMatch[1] : '';
    const filename = dispositionMatch ? dispositionMatch[2] : undefined;
    const type = typeMatch ? typeMatch[1] : undefined;
    parts.push({ name, filename, type, data: content });
    start = partEnd + boundaryBuffer.length + 2; // skip CRLF
    if (bodyBuffer.slice(partEnd, partEnd + endBoundaryBuffer.length).equals(endBoundaryBuffer)) break;
  }
  return parts;
}
let XLSX = null;
try {
  XLSX = require('xlsx');
} catch (_) {
  XLSX = null;
}

// No external storage for now; process in-memory and return preview

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow POST method
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const contentType = event.headers['content-type'] || event.headers['Content-Type'];
    
    if (!contentType || !contentType.includes('multipart/form-data')) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Content-Type must be multipart/form-data' })
      };
    }

    // Parse multipart form data
    const boundary = contentType.split('boundary=')[1];
    if (!boundary) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Missing multipart boundary' })
      };
    }
    const rawBuffer = event.isBase64Encoded ? Buffer.from(event.body, 'base64') : Buffer.from(event.body || '', 'latin1');
    const parts = parseMultipartBody(rawBuffer, boundary);
    try { console.log('upload parts:', parts.map(p => ({ name: p.name, filename: p.filename, length: p.data ? p.data.length : 0 }))); } catch (_) {}
    
    const filePart = parts.find(part => part.name === 'file');
    const userIdPart = parts.find(part => part.name === 'userId');
    
    if (!filePart) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'No file uploaded' })
      };
    }

    const fileName = filePart.filename || 'upload';
    const fileExtension = fileName.split('.').pop().toLowerCase();
    const userId = userIdPart ? userIdPart.data.toString() : 'anonymous';
    
    // Validate file type
    if (!['csv', 'xlsx', 'xls'].includes(fileExtension)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Only CSV and Excel files are supported' })
      };
    }

    // Check file size (max 20MB)
    if (filePart.data.length > 20 * 1024 * 1024) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'File size must be less than 20MB' })
      };
    }

    // Generate unique file key
    const timestamp = Date.now();
    const safeFileName = fileName.replace(/[^a-zA-Z0-9_.-]/g, '_');
    const fileKey = `uploads/${userId}/${timestamp}_${safeFileName}`;

    // Skipping S3 upload in this environment

    // Process file for preview analytics
    let analyticsPreview = null;
    
    try {
      if (fileExtension === 'csv') {
        analyticsPreview = await processCSV(filePart.data);
      } else if (['xlsx', 'xls'].includes(fileExtension)) {
        analyticsPreview = await processExcel(filePart.data);
      }
    } catch (error) {
      console.error('Analytics processing error:', error);
      // Continue without preview if processing fails
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'File uploaded successfully',
        fileId: fileKey,
        fileName: fileName,
        fileSize: filePart.data.length,
        s3Url: null,
        analyticsPreview: analyticsPreview,
        uploadedAt: new Date().toISOString()
      })
    };

  } catch (error) {
    console.error('Upload error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Failed to upload file. Please try again later.' 
      })
    };
  }
};

// Process CSV file for analytics preview
async function processCSV(buffer) {
  const text = buffer.toString('utf8');
  const lines = text.split(/\r?\n/).filter(line => line.trim().length > 0);
  if (lines.length === 0) return { error: 'No data found in file' };
  const headers = splitCsvLine(lines[0]);
  const records = [];
  for (let i = 1; i < lines.length && records.length < 100; i++) {
    const values = splitCsvLine(lines[i]);
    const record = {};
    for (let j = 0; j < headers.length; j++) {
      record[headers[j]] = values[j] !== undefined ? values[j] : '';
    }
    records.push(record);
  }
  return generateAnalyticsPreview(records);
}

function splitCsvLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (inQuotes) {
      if (char === '"') {
        if (i + 1 < line.length && line[i + 1] === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        current += char;
      }
    } else {
      if (char === '"') {
        inQuotes = true;
      } else if (char === ',') {
        result.push(current);
        current = '';
      } else {
        current += char;
      }
    }
  }
  result.push(current);
  return result;
}

// Process Excel file for analytics preview
async function processExcel(buffer) {
  try {
    if (!XLSX) throw new Error('XLSX not available');
    const workbook = XLSX.read(buffer, { type: 'buffer' });
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    
    // Convert to JSON (limit to 100 rows for preview)
    const records = XLSX.utils.sheet_to_json(worksheet, { 
      range: 0, 
      defval: null 
    }).slice(0, 100);
    
    const analytics = generateAnalyticsPreview(records);
    return analytics;
  } catch (error) {
    throw new Error('Failed to process Excel file');
  }
}

// Generate basic analytics preview
function generateAnalyticsPreview(records) {
  if (!records || records.length === 0) {
    return { error: 'No data found in file' };
  }

  const columns = Object.keys(records[0]);
  const rowCount = records.length;
  
  // Analyze each column
  const columnAnalysis = {};
  
  columns.forEach(column => {
    const values = records.map(record => record[column]).filter(val => val !== null && val !== undefined && val !== '');
    const nonEmptyCount = values.length;
    const emptyCount = rowCount - nonEmptyCount;
    
    // Determine data type
    const numericValues = values.filter(val => !isNaN(parseFloat(val)) && isFinite(val));
    const isNumeric = numericValues.length > values.length * 0.7; // 70% threshold
    
    columnAnalysis[column] = {
      totalValues: rowCount,
      nonEmptyValues: nonEmptyCount,
      emptyValues: emptyCount,
      completeness: ((nonEmptyCount / rowCount) * 100).toFixed(1) + '%',
      dataType: isNumeric ? 'numeric' : 'text',
      uniqueValues: [...new Set(values)].length
    };
    
    // Add numeric statistics if applicable
    if (isNumeric && numericValues.length > 0) {
      const numbers = numericValues.map(val => parseFloat(val));
      columnAnalysis[column].min = Math.min(...numbers);
      columnAnalysis[column].max = Math.max(...numbers);
      columnAnalysis[column].average = (numbers.reduce((a, b) => a + b, 0) / numbers.length).toFixed(2);
    }
  });

  return {
    summary: {
      totalRows: rowCount,
      totalColumns: columns.length,
      columns: columns
    },
    columnAnalysis: columnAnalysis,
    insights: generateInsights(columnAnalysis, rowCount),
    preview: records.slice(0, 5) // First 5 rows for preview
  };
}

// Generate AI insights
function generateInsights(columnAnalysis, rowCount) {
  const insights = [];
  
  // Data quality insights
  const lowQualityColumns = Object.entries(columnAnalysis)
    .filter(([_, analysis]) => parseFloat(analysis.completeness) < 80)
    .map(([column, _]) => column);
    
  if (lowQualityColumns.length > 0) {
    insights.push({
      type: 'warning',
      title: 'Data Quality Alert',
      message: `Columns with missing data: ${lowQualityColumns.join(', ')}. Consider data cleaning.`
    });
  }
  
  // Numeric columns for analysis
  const numericColumns = Object.entries(columnAnalysis)
    .filter(([_, analysis]) => analysis.dataType === 'numeric')
    .map(([column, _]) => column);
    
  if (numericColumns.length > 0) {
    insights.push({
      type: 'opportunity',
      title: 'Analytics Potential',
      message: `${numericColumns.length} numeric columns detected. Perfect for trend analysis, forecasting, and statistical modeling.`
    });
  }
  
  // High cardinality detection
  const highCardinalityColumns = Object.entries(columnAnalysis)
    .filter(([_, analysis]) => analysis.uniqueValues > rowCount * 0.8)
    .map(([column, _]) => column);
    
  if (highCardinalityColumns.length > 0) {
    insights.push({
      type: 'info',
      title: 'Unique Identifiers',
      message: `Columns likely containing IDs: ${highCardinalityColumns.join(', ')}. These can be used for data linking.`
    });
  }
  
  return insights;
}
