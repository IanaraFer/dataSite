const AWS = require('aws-sdk');
const multipart = require('parse-multipart-data');
const csv = require('csv-parse');
const XLSX = require('xlsx');

// Configure AWS S3
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'eu-west-1'
});

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
    const contentTypeRaw = event.headers['content-type'] || event.headers['Content-Type'] || '';
    const contentType = String(contentTypeRaw);
    
    if (!contentType.includes('multipart/form-data')) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Content-Type must be multipart/form-data' })
      };
    }

    // Normalize boundary and body encoding
    let boundary = contentType.split('boundary=')[1] || '';
    boundary = boundary.replace(/^"|"$/g, '');
    const bodyBuffer = event.isBase64Encoded
      ? Buffer.from(event.body || '', 'base64')
      : Buffer.from(event.body || '', 'utf8');

    // Parse multipart form data
    const parts = multipart.parse(bodyBuffer, boundary);
    
    const filePart = parts.find(part => part.name === 'file' || part.name === 'businessData');
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

    // Check file size (max 10MB)
    if (filePart.data.length > 10 * 1024 * 1024) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'File size must be less than 10MB' })
      };
    }

    // Generate unique file key
    const timestamp = Date.now();
    const safeUserId = userId.replace(/[^a-zA-Z0-9_-]/g, 'anon');
    const fileKey = `uploads/${safeUserId}/${timestamp}-${fileName}`;

    // Upload to S3
    const uploadParams = {
      Bucket: process.env.S3_BUCKET_NAME || 'analyticacore-uploads',
      Key: fileKey,
      Body: filePart.data,
      ContentType: filePart.type || 'application/octet-stream',
      Metadata: {
        originalName: fileName,
        userId: userId,
        uploadedAt: new Date().toISOString()
      }
    };

    const uploadResult = await s3.upload(uploadParams).promise();

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
        s3Url: uploadResult.Location,
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
  return new Promise((resolve, reject) => {
    const records = [];
    const parser = csv.parse(buffer.toString(), {
      columns: true,
      skip_empty_lines: true,
      max_records: 100 // Limit for preview
    });
    
    parser.on('readable', function() {
      let record;
      while (record = parser.read()) {
        records.push(record);
      }
    });
    
    parser.on('error', reject);
    
    parser.on('end', function() {
      const analytics = generateAnalyticsPreview(records);
      resolve(analytics);
    });
  });
}

// Process Excel file for analytics preview
async function processExcel(buffer) {
  try {
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
      message: `Columns with missing data: ${lowQualityColumns.join(', ') || 'None'}. Consider data cleaning.`
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
      message: `Columns likely containing IDs: ${highCardinalityColumns.join(', ') || 'None'}. These can be used for data linking.`
    });
  }
  
  return insights;
}
