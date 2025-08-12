// Global Variables
let currentData = null;
let charts = {};
let loadingModal;

// Sample data for demo
const sampleData = [
    { date: '2024-01-01', revenue: 15000, customers: 120, satisfaction: 85, category: 'Electronics' },
    { date: '2024-01-02', revenue: 18000, customers: 145, satisfaction: 87, category: 'Electronics' },
    { date: '2024-01-03', revenue: 12000, customers: 98, satisfaction: 82, category: 'Clothing' },
    { date: '2024-01-04', revenue: 22000, customers: 178, satisfaction: 91, category: 'Electronics' },
    { date: '2024-01-05', revenue: 16000, customers: 132, satisfaction: 86, category: 'Electronics' },
    { date: '2024-01-06', revenue: 14000, customers: 115, satisfaction: 84, category: 'Clothing' },
    { date: '2024-01-07', revenue: 19000, customers: 156, satisfaction: 88, category: 'Electronics' },
    { date: '2024-01-08', revenue: 25000, customers: 201, satisfaction: 93, category: 'Electronics' },
    { date: '2024-01-09', revenue: 13000, customers: 108, satisfaction: 81, category: 'Clothing' },
    { date: '2024-01-10', revenue: 21000, customers: 169, satisfaction: 89, category: 'Electronics' },
    { date: '2024-01-11', revenue: 17000, customers: 140, satisfaction: 85, category: 'Electronics' },
    { date: '2024-01-12', revenue: 23000, customers: 184, satisfaction: 92, category: 'Electronics' },
    { date: '2024-01-13', revenue: 15000, customers: 123, satisfaction: 83, category: 'Clothing' },
    { date: '2024-01-14', revenue: 20000, customers: 164, satisfaction: 90, category: 'Electronics' },
    { date: '2024-01-15', revenue: 18000, customers: 148, satisfaction: 87, category: 'Electronics' }
];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    console.log('DataSight AI Platform initialized! 🚀');
});

// File Upload Handler
function handleFileUpload(input) {
    const file = input.files[0];
    if (file && file.type === 'text/csv') {
        showLoading('Uploading and processing your file...', 'Analyzing data structure and content...');
        
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const csv = e.target.result;
                const parsed = parseCSV(csv);
                currentData = parsed;
                
                setTimeout(() => {
                    hideLoading();
                    showDataLoaded();
                    updateMetrics();
                    showDataPreview();
                }, 2000);
            } catch (error) {
                hideLoading();
                alert('Error parsing CSV file. Please ensure it\'s properly formatted.');
            }
        };
        reader.readAsText(file);
    } else {
        alert('Please upload a valid CSV file.');
    }
}

// Parse CSV data
function parseCSV(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
            const values = lines[i].split(',');
            const row = {};
            headers.forEach((header, index) => {
                row[header] = values[index] ? values[index].trim() : '';
            });
            data.push(row);
        }
    }
    
    return data;
}

// Load Sample Data
function loadSampleData() {
    showLoading('Loading sample dataset...', 'Preparing retail analytics data...');
    
    setTimeout(() => {
        currentData = sampleData;
        hideLoading();
        showDataLoaded();
        updateMetrics();
        showDataPreview();
    }, 1500);
}

// Show data loaded state
function showDataLoaded() {
    document.getElementById('metricsRow').style.display = 'flex';
    document.getElementById('analysisControls').style.display = 'block';
    document.getElementById('dataPreview').style.display = 'block';
    
    // Animate metrics
    document.getElementById('metricsRow').classList.add('fade-in');
}

// Update key metrics
function updateMetrics() {
    if (!currentData) return;
    
    const totalRevenue = currentData.reduce((sum, row) => sum + (parseFloat(row.revenue) || 0), 0);
    const totalCustomers = currentData.reduce((sum, row) => sum + (parseFloat(row.customers) || 0), 0);
    const avgSatisfaction = currentData.reduce((sum, row) => sum + (parseFloat(row.satisfaction) || 0), 0) / currentData.length;
    
    // Animate counter updates
    animateCounter('revenueMetric', totalRevenue, '€');
    animateCounter('customersMetric', totalCustomers, '');
    animateCounter('satisfactionMetric', Math.round(avgSatisfaction), '%');
    animateCounter('growthMetric', 23, '%'); // Mock growth rate
}

// Animate counter
function animateCounter(elementId, targetValue, suffix) {
    const element = document.getElementById(elementId);
    const duration = 1500;
    const steps = 60;
    const increment = targetValue / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            element.textContent = (suffix === '€' ? '€' + Math.round(targetValue).toLocaleString() : Math.round(targetValue).toLocaleString() + suffix);
            clearInterval(timer);
        } else {
            element.textContent = (suffix === '€' ? '€' + Math.round(current).toLocaleString() : Math.round(current).toLocaleString() + suffix);
        }
    }, duration / steps);
}

// Show data preview
function showDataPreview() {
    if (!currentData || currentData.length === 0) return;
    
    const table = document.getElementById('previewTable');
    const headers = Object.keys(currentData[0]);
    
    // Create headers
    const headerRow = table.querySelector('thead tr');
    headerRow.innerHTML = '';
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    
    // Create rows (show first 5 rows)
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    const displayData = currentData.slice(0, 5);
    
    displayData.forEach(row => {
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = row[header] || '';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Run Forecast Analysis
function runForecast() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Running AI forecast model...', 'Analyzing trends and patterns...');
    
    setTimeout(() => {
        hideLoading();
        showForecastResults();
    }, 3000);
}

// Show Forecast Results
function showForecastResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    // Generate mock forecast data
    const forecastData = generateForecastData();
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-crystal-ball me-2"></i>Revenue Forecast</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <div id="forecastChart"></div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-6">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-primary mb-2">
                                <i class="fas fa-trending-up me-1"></i>Key Insights
                            </h6>
                            <ul class="list-unstyled mb-0">
                                <li class="mb-1">📈 Expected 18% revenue growth next quarter</li>
                                <li class="mb-1">🎯 Peak sales predicted for March 15th</li>
                                <li class="mb-1">⚠️ Potential dip in early February</li>
                                <li class="mb-1">💡 Recommend inventory increase by 25%</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-success mb-2">
                                <i class="fas fa-chart-line me-1"></i>Forecast Accuracy
                            </h6>
                            <div class="d-flex align-items-center mb-2">
                                <span class="me-2">Model Confidence:</span>
                                <div class="progress flex-grow-1">
                                    <div class="progress-bar bg-success" style="width: 87%"></div>
                                </div>
                                <span class="ms-2 fw-bold">87%</span>
                            </div>
                            <small class="text-muted">Based on historical patterns and seasonal trends</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create the forecast chart
    createForecastChart(forecastData);
}

// Generate Forecast Data
function generateForecastData() {
    const historical = currentData.map(row => ({
        date: row.date,
        revenue: parseFloat(row.revenue) || 0
    }));
    
    // Generate future predictions
    const future = [];
    const lastDate = new Date(historical[historical.length - 1].date);
    const baseRevenue = historical[historical.length - 1].revenue;
    
    for (let i = 1; i <= 10; i++) {
        const futureDate = new Date(lastDate);
        futureDate.setDate(lastDate.getDate() + i);
        
        // Simple trend with some randomness
        const trend = baseRevenue * (1 + (i * 0.02)) + (Math.random() - 0.5) * 3000;
        future.push({
            date: futureDate.toISOString().split('T')[0],
            revenue: Math.max(trend, 0)
        });
    }
    
    return { historical, future };
}

// Create Forecast Chart
function createForecastChart(data) {
    const historicalTrace = {
        x: data.historical.map(d => d.date),
        y: data.historical.map(d => d.revenue),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Historical Data',
        line: { color: '#1f77b4', width: 3 },
        marker: { size: 6 }
    };
    
    const forecastTrace = {
        x: data.future.map(d => d.date),
        y: data.future.map(d => d.revenue),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Forecast',
        line: { color: '#ff7f0e', width: 3, dash: 'dash' },
        marker: { size: 6 }
    };
    
    const layout = {
        title: 'Revenue Forecast - Next 10 Days',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Revenue (€)' },
        showlegend: true,
        height: 400,
        margin: { t: 50, r: 50, b: 50, l: 60 }
    };
    
    Plotly.newPlot('forecastChart', [historicalTrace, forecastTrace], layout, {responsive: true});
}

// Run Customer Segmentation
function runSegmentation() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing customer segments...', 'Applying machine learning clustering...');
    
    setTimeout(() => {
        hideLoading();
        showSegmentationResults();
    }, 2500);
}

// Show Segmentation Results
function showSegmentationResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0"><i class="fas fa-users me-2"></i>Customer Segmentation</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="segmentChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-success mb-3">
                                <i class="fas fa-bullseye me-1"></i>Segment Insights
                            </h6>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-primary">Premium</span>
                                    <span class="fw-bold">23%</span>
                                </div>
                                <small class="text-muted">High value, loyal customers</small>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-warning">Standard</span>
                                    <span class="fw-bold">45%</span>
                                </div>
                                <small class="text-muted">Regular purchase behavior</small>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-info">Growth</span>
                                    <span class="fw-bold">32%</span>
                                </div>
                                <small class="text-muted">Potential for upselling</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-primary mb-2">
                                <i class="fas fa-lightbulb me-1"></i>Recommended Actions
                            </h6>
                            <div class="row">
                                <div class="col-md-4">
                                    <strong>Premium Segment:</strong><br>
                                    <small class="text-muted">Offer exclusive products and VIP support</small>
                                </div>
                                <div class="col-md-4">
                                    <strong>Standard Segment:</strong><br>
                                    <small class="text-muted">Focus on retention and cross-selling</small>
                                </div>
                                <div class="col-md-4">
                                    <strong>Growth Segment:</strong><br>
                                    <small class="text-muted">Targeted promotions and education</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create segmentation chart
    createSegmentationChart();
}

// Create Segmentation Chart
function createSegmentationChart() {
    const data = [{
        values: [23, 45, 32],
        labels: ['Premium Customers', 'Standard Customers', 'Growth Customers'],
        type: 'pie',
        marker: {
            colors: ['#1f77b4', '#ffc107', '#17a2b8']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    }];
    
    const layout = {
        title: 'Customer Segments Distribution',
        height: 400,
        showlegend: true,
        margin: { t: 50, r: 50, b: 50, l: 50 }
    };
    
    Plotly.newPlot('segmentChart', data, layout, {responsive: true});
}

// Run Anomaly Detection
function runAnomalyDetection() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Detecting anomalies...', 'Scanning for unusual patterns...');
    
    setTimeout(() => {
        hideLoading();
        showAnomalyResults();
    }, 2000);
}

// Show Anomaly Results
function showAnomalyResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-warning text-dark">
                <h5 class="mb-0"><i class="fas fa-search me-2"></i>Anomaly Detection</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <div id="anomalyChart"></div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-6">
                        <div class="insight-card p-3 rounded border-warning">
                            <h6 class="text-warning mb-2">
                                <i class="fas fa-exclamation-triangle me-1"></i>Anomalies Detected
                            </h6>
                            <ul class="list-unstyled mb-0">
                                <li class="mb-2">
                                    <span class="badge bg-danger me-2">HIGH</span>
                                    Revenue spike on Jan 8th (+67% above normal)
                                </li>
                                <li class="mb-2">
                                    <span class="badge bg-warning me-2">MED</span>
                                    Unusual customer drop on Jan 9th
                                </li>
                                <li class="mb-2">
                                    <span class="badge bg-info me-2">LOW</span>
                                    Satisfaction score variance detected
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="insight-card p-3 rounded border-success">
                            <h6 class="text-success mb-2">
                                <i class="fas fa-check-circle me-1"></i>Recommended Actions
                            </h6>
                            <ul class="list-unstyled mb-0">
                                <li class="mb-1">🔍 Investigate Jan 8th revenue source</li>
                                <li class="mb-1">📧 Follow up with Jan 9th customers</li>
                                <li class="mb-1">📊 Review satisfaction feedback</li>
                                <li class="mb-1">🚨 Set up automated alerts</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    createAnomalyChart();
}

// Create Anomaly Chart
function createAnomalyChart() {
    const normalData = currentData.filter((_, i) => i !== 7 && i !== 8); // Exclude anomalies
    const anomalies = [currentData[7], currentData[8]]; // Jan 8th and 9th
    
    const normalTrace = {
        x: normalData.map(d => d.date),
        y: normalData.map(d => parseFloat(d.revenue)),
        type: 'scatter',
        mode: 'markers',
        name: 'Normal Data',
        marker: { color: '#1f77b4', size: 8 }
    };
    
    const anomalyTrace = {
        x: anomalies.map(d => d.date),
        y: anomalies.map(d => parseFloat(d.revenue)),
        type: 'scatter',
        mode: 'markers',
        name: 'Anomalies',
        marker: { color: '#dc3545', size: 12, symbol: 'diamond' }
    };
    
    const layout = {
        title: 'Revenue Anomaly Detection',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Revenue (€)' },
        showlegend: true,
        height: 400,
        margin: { t: 50, r: 50, b: 50, l: 60 }
    };
    
    Plotly.newPlot('anomalyChart', [normalTrace, anomalyTrace], layout, {responsive: true});
}

// Generate AI Insights
function generateInsights() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Generating AI insights...', 'Analyzing business patterns...');
    
    setTimeout(() => {
        hideLoading();
        showInsightsResults();
    }, 2500);
}

// Show Insights Results
function showInsightsResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="fas fa-lightbulb me-2"></i>AI Business Insights</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-lg-8">
                        <div class="insight-card p-4 rounded mb-3">
                            <h6 class="text-primary mb-3">
                                <i class="fas fa-brain me-2"></i>Key Business Insights
                            </h6>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <div class="p-3 bg-light rounded">
                                        <h6 class="text-success mb-2">💰 Revenue Optimization</h6>
                                        <p class="mb-0 small">Your Electronics category generates 73% of revenue. Consider expanding this segment with complementary products.</p>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="p-3 bg-light rounded">
                                        <h6 class="text-warning mb-2">📅 Seasonal Patterns</h6>
                                        <p class="mb-0 small">Weekend sales are 34% higher. Implement weekend-specific promotions to maximize revenue.</p>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="p-3 bg-light rounded">
                                        <h6 class="text-info mb-2">👥 Customer Behavior</h6>
                                        <p class="mb-0 small">High satisfaction correlates with 2.3x higher purchase frequency. Focus on satisfaction scores.</p>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="p-3 bg-light rounded">
                                        <h6 class="text-danger mb-2">⚠️ Risk Factors</h6>
                                        <p class="mb-0 small">Clothing segment shows declining trend. Consider market research or product refresh.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="insight-card p-3 rounded mb-3">
                            <h6 class="text-primary mb-3">📈 ROI Calculator</h6>
                            <div class="mb-3">
                                <label class="form-label">Investment (€)</label>
                                <input type="number" class="form-control" id="investment" value="10000" onchange="calculateROI()">
                            </div>
                            <div class="text-center p-3 bg-success text-white rounded">
                                <h4 class="mb-0" id="roiResult">340%</h4>
                                <small>Predicted ROI</small>
                            </div>
                        </div>
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-primary mb-3">🎯 Quick Actions</h6>
                            <div class="d-grid gap-2">
                                <button class="btn btn-sm btn-outline-primary">Export Report</button>
                                <button class="btn btn-sm btn-outline-success">Schedule Alert</button>
                                <button class="btn btn-sm btn-outline-info">Share Insights</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Calculate ROI
function calculateROI() {
    const investment = parseFloat(document.getElementById('investment').value) || 0;
    const predictedReturn = investment * 3.4; // Mock calculation
    const roi = ((predictedReturn - investment) / investment * 100).toFixed(0);
    document.getElementById('roiResult').textContent = roi + '%';
}

// Show Loading Modal
function showLoading(title, subtitle) {
    document.getElementById('loadingText').textContent = title;
    document.getElementById('loadingSubtext').textContent = subtitle;
    loadingModal.show();
    
    // Animate progress bar
    const progressBar = document.getElementById('progressBar');
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress > 100) progress = 100;
        progressBar.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 200);
}

// Hide Loading Modal
function hideLoading() {
    loadingModal.hide();
    // Reset progress bar
    setTimeout(() => {
        document.getElementById('progressBar').style.width = '0%';
    }, 500);
}

// Reset Demo
function resetDemo() {
    if (confirm('Are you sure you want to reset the demo? All data will be cleared.')) {
        currentData = null;
        document.getElementById('metricsRow').style.display = 'none';
        document.getElementById('analysisControls').style.display = 'none';
        document.getElementById('dataPreview').style.display = 'none';
        document.getElementById('fileInput').value = '';
        
        // Reset analysis results
        document.getElementById('analysisResults').innerHTML = `
            <div class="card analysis-card h-100" id="welcomeCard">
                <div class="card-body text-center py-5">
                    <i class="fas fa-chart-area fs-1 text-primary mb-4"></i>
                    <h3 class="text-primary mb-3">Ready for AI Analysis</h3>
                    <p class="lead text-muted mb-4">
                        Upload your business data or load our sample dataset to see DataSight AI in action. 
                        Our advanced algorithms will automatically analyze your data and provide actionable insights.
                    </p>
                    <div class="row text-center">
                        <div class="col-4">
                            <i class="fas fa-brain text-primary fs-2 mb-2"></i>
                            <h6>AI-Powered</h6>
                            <small class="text-muted">Machine learning algorithms</small>
                        </div>
                        <div class="col-4">
                            <i class="fas fa-bolt text-warning fs-2 mb-2"></i>
                            <h6>Lightning Fast</h6>
                            <small class="text-muted">Results in seconds</small>
                        </div>
                        <div class="col-4">
                            <i class="fas fa-shield-alt text-success fs-2 mb-2"></i>
                            <h6>Secure</h6>
                            <small class="text-muted">Your data stays private</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        console.log('Demo reset successfully! 🔄');
    }
}

// ============================================
// NEW ENHANCED ANALYSIS FUNCTIONS
// ============================================

// Trend Analysis
function runTrendAnalysis() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing trends...', 'Detecting patterns and trends in your data...');
    
    setTimeout(() => {
        hideLoading();
        showTrendAnalysisResults();
    }, 2000);
}

function showTrendAnalysisResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="fas fa-trending-up me-2"></i>Trend Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="trendChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-info mb-3">
                                <i class="fas fa-chart-line me-1"></i>Trend Insights
                            </h6>
                            <div class="alert alert-success border-0 p-2 mb-2">
                                <small><i class="fas fa-arrow-up me-1"></i><strong>Growth Trend:</strong> 18% increase over last 6 months</small>
                            </div>
                            <div class="alert alert-warning border-0 p-2 mb-2">
                                <small><i class="fas fa-exclamation-triangle me-1"></i><strong>Seasonality:</strong> Strong Q4 pattern detected</small>
                            </div>
                            <div class="alert alert-info border-0 p-2 mb-2">
                                <small><i class="fas fa-calendar me-1"></i><strong>Peak Period:</strong> November-December</small>
                            </div>
                            <div class="alert alert-primary border-0 p-2">
                                <small><i class="fas fa-lightbulb me-1"></i><strong>Recommendation:</strong> Increase inventory by 25% for Q4</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create trend chart
    const trendData = [
        {
            x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y: [45000, 48000, 52000, 49000, 55000, 58000, 61000, 59000, 65000, 72000, 89000, 95000],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Revenue Trend',
            line: {color: '#1f77b4', width: 3},
            marker: {size: 8}
        }
    ];
    
    Plotly.newPlot('trendChart', trendData, {
        title: 'Revenue Trend Analysis',
        xaxis: {title: 'Month'},
        yaxis: {title: 'Revenue (€)'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Seasonal Analysis
function runSeasonalAnalysis() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing seasonal patterns...', 'Identifying seasonal trends and cycles...');
    
    setTimeout(() => {
        hideLoading();
        showSeasonalAnalysisResults();
    }, 2200);
}

function showSeasonalAnalysisResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-warning text-dark">
                <h5 class="mb-0"><i class="fas fa-calendar-alt me-2"></i>Seasonal Pattern Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="seasonalChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-warning mb-3">
                                <i class="fas fa-calendar me-1"></i>Seasonal Insights
                            </h6>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-success">Q4</span>
                                    <span class="fw-bold">+45%</span>
                                </div>
                                <small class="text-muted">Peak season performance</small>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-danger">Q1</span>
                                    <span class="fw-bold">-23%</span>
                                </div>
                                <small class="text-muted">Low season period</small>
                            </div>
                            <div class="alert alert-info border-0 p-2">
                                <small><i class="fas fa-chart-bar me-1"></i><strong>Best Months:</strong> Nov, Dec, Jan</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create seasonal chart
    const seasonalData = [
        {
            x: ['Q1', 'Q2', 'Q3', 'Q4'],
            y: [195000, 220000, 235000, 340000],
            type: 'bar',
            name: 'Seasonal Revenue',
            marker: {color: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']}
        }
    ];
    
    Plotly.newPlot('seasonalChart', seasonalData, {
        title: 'Quarterly Seasonal Patterns',
        xaxis: {title: 'Quarter'},
        yaxis: {title: 'Revenue (€)'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Growth Analysis
function runGrowthAnalysis() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Calculating growth metrics...', 'Analyzing growth rates and projections...');
    
    setTimeout(() => {
        hideLoading();
        showGrowthAnalysisResults();
    }, 1800);
}

function showGrowthAnalysisResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0"><i class="fas fa-chart-area me-2"></i>Growth Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="chart-container">
                            <div id="growthChart"></div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-success mb-3">
                                <i class="fas fa-rocket me-1"></i>Growth Metrics
                            </h6>
                            <div class="row text-center mb-3">
                                <div class="col-6">
                                    <div class="border rounded p-2">
                                        <div class="h4 text-success mb-0">+24%</div>
                                        <small class="text-muted">YoY Growth</small>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="border rounded p-2">
                                        <div class="h4 text-info mb-0">+18%</div>
                                        <small class="text-muted">Monthly Growth</small>
                                    </div>
                                </div>
                            </div>
                            <div class="alert alert-success border-0 p-2 mb-2">
                                <small><i class="fas fa-thumbs-up me-1"></i><strong>Strong Growth:</strong> Above industry average</small>
                            </div>
                            <div class="alert alert-info border-0 p-2">
                                <small><i class="fas fa-target me-1"></i><strong>Projection:</strong> €1.2M by year end</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create growth chart
    const growthData = [
        {
            x: ['6 months ago', '5 months ago', '4 months ago', '3 months ago', '2 months ago', 'Last month', 'This month'],
            y: [15, 18, 12, 25, 22, 28, 24],
            type: 'bar',
            name: 'Monthly Growth %',
            marker: {color: '#2ecc71'}
        }
    ];
    
    Plotly.newPlot('growthChart', growthData, {
        title: 'Monthly Growth Rate',
        xaxis: {title: 'Period'},
        yaxis: {title: 'Growth Rate (%)'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Customer Lifetime Value
function runLifetimeValue() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Calculating customer lifetime value...', 'Analyzing customer purchase patterns...');
    
    setTimeout(() => {
        hideLoading();
        showLifetimeValueResults();
    }, 2500);
}

function showLifetimeValueResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-gem me-2"></i>Customer Lifetime Value Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="clvChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-primary mb-3">
                                <i class="fas fa-coins me-1"></i>CLV Insights
                            </h6>
                            <div class="text-center mb-3">
                                <div class="h2 text-primary">€2,850</div>
                                <small class="text-muted">Average CLV</small>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-success">Top 10%</span>
                                    <span class="fw-bold">€8,500</span>
                                </div>
                                <small class="text-muted">Premium customers</small>
                            </div>
                            <div class="alert alert-warning border-0 p-2">
                                <small><i class="fas fa-exclamation-triangle me-1"></i><strong>Focus:</strong> Increase retention by 5% to boost CLV 25%</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create CLV distribution chart
    const clvData = [
        {
            x: ['€0-500', '€500-1000', '€1000-2000', '€2000-5000', '€5000+'],
            y: [125, 203, 287, 156, 45],
            type: 'bar',
            name: 'Customer Count',
            marker: {color: '#3498db'}
        }
    ];
    
    Plotly.newPlot('clvChart', clvData, {
        title: 'Customer Lifetime Value Distribution',
        xaxis: {title: 'CLV Range'},
        yaxis: {title: 'Number of Customers'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Churn Prediction
function runChurnPrediction() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Predicting customer churn...', 'Analyzing customer behavior patterns...');
    
    setTimeout(() => {
        hideLoading();
        showChurnPredictionResults();
    }, 3000);
}

function showChurnPredictionResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0"><i class="fas fa-user-times me-2"></i>Churn Prediction Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="churnChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-danger mb-3">
                                <i class="fas fa-exclamation-circle me-1"></i>Churn Risk
                            </h6>
                            <div class="alert alert-danger border-0 p-2 mb-2">
                                <small><i class="fas fa-users me-1"></i><strong>High Risk:</strong> 87 customers (7.2%)</small>
                            </div>
                            <div class="alert alert-warning border-0 p-2 mb-2">
                                <small><i class="fas fa-user-clock me-1"></i><strong>Medium Risk:</strong> 156 customers (12.9%)</small>
                            </div>
                            <div class="alert alert-success border-0 p-2 mb-3">
                                <small><i class="fas fa-shield-alt me-1"></i><strong>Low Risk:</strong> 967 customers (79.9%)</small>
                            </div>
                            <div class="alert alert-info border-0 p-2">
                                <small><i class="fas fa-lightbulb me-1"></i><strong>Action:</strong> Launch retention campaign for high-risk customers</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create churn prediction chart
    const churnData = [
        {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            values: [967, 156, 87],
            type: 'pie',
            marker: {colors: ['#2ecc71', '#f39c12', '#e74c3c']},
            hole: 0.4
        }
    ];
    
    Plotly.newPlot('churnChart', churnData, {
        title: 'Customer Churn Risk Distribution',
        margin: {t: 50, r: 50, b: 50, l: 50}
    });
}

// RFM Analysis
function runRFMAnalysis() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Running RFM analysis...', 'Analyzing Recency, Frequency, and Monetary value...');
    
    setTimeout(() => {
        hideLoading();
        showRFMAnalysisResults();
    }, 2800);
}

function showRFMAnalysisResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="fas fa-star me-2"></i>RFM Analysis (Recency, Frequency, Monetary)</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="rfmChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-info mb-3">
                                <i class="fas fa-medal me-1"></i>RFM Segments
                            </h6>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-success">Champions</span>
                                    <span class="fw-bold">15%</span>
                                </div>
                                <small class="text-muted">Best customers - high value, frequent, recent</small>
                            </div>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-primary">Loyal</span>
                                    <span class="fw-bold">23%</span>
                                </div>
                                <small class="text-muted">Regular customers - good frequency</small>
                            </div>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-warning">At Risk</span>
                                    <span class="fw-bold">18%</span>
                                </div>
                                <small class="text-muted">Haven't purchased recently</small>
                            </div>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-danger">Lost</span>
                                    <span class="fw-bold">12%</span>
                                </div>
                                <small class="text-muted">Haven't purchased in long time</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create RFM segmentation chart
    const rfmData = [
        {
            x: ['Champions', 'Loyal', 'Potential', 'New', 'At Risk', 'Cannot Lose', 'Lost'],
            y: [180, 276, 195, 89, 216, 67, 144],
            type: 'bar',
            name: 'Customer Count',
            marker: {color: ['#2ecc71', '#3498db', '#9b59b6', '#1abc9c', '#f39c12', '#e67e22', '#e74c3c']}
        }
    ];
    
    Plotly.newPlot('rfmChart', rfmData, {
        title: 'RFM Customer Segmentation',
        xaxis: {title: 'RFM Segment'},
        yaxis: {title: 'Number of Customers'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Product Performance
function runProductPerformance() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing product performance...', 'Evaluating sales and profitability by product...');
    
    setTimeout(() => {
        hideLoading();
        showProductPerformanceResults();
    }, 2200);
}

function showProductPerformanceResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-warning text-dark">
                <h5 class="mb-0"><i class="fas fa-box me-2"></i>Product Performance Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="productChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-warning mb-3">
                                <i class="fas fa-trophy me-1"></i>Top Performers
                            </h6>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-success">Electronics</span>
                                    <span class="fw-bold">€456K</span>
                                </div>
                                <small class="text-muted">73% of total revenue</small>
                            </div>
                            <div class="mb-2">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge bg-info">Clothing</span>
                                    <span class="fw-bold">€123K</span>
                                </div>
                                <small class="text-muted">19% of total revenue</small>
                            </div>
                            <div class="alert alert-success border-0 p-2">
                                <small><i class="fas fa-chart-line me-1"></i><strong>Trend:</strong> Electronics growing 34% YoY</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create product performance chart
    const productData = [
        {
            x: ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports'],
            y: [456000, 123000, 45000, 67000, 89000],
            type: 'bar',
            name: 'Revenue by Category',
            marker: {color: '#f39c12'}
        }
    ];
    
    Plotly.newPlot('productChart', productData, {
        title: 'Product Category Performance',
        xaxis: {title: 'Product Category'},
        yaxis: {title: 'Revenue (€)'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Market Basket Analysis
function runMarketBasket() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing purchase patterns...', 'Finding product associations and cross-selling opportunities...');
    
    setTimeout(() => {
        hideLoading();
        showMarketBasketResults();
    }, 2600);
}

function showMarketBasketResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0"><i class="fas fa-shopping-basket me-2"></i>Market Basket Analysis</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="basketChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-success mb-3">
                                <i class="fas fa-link me-1"></i>Product Associations
                            </h6>
                            <div class="alert alert-success border-0 p-2 mb-2">
                                <small><i class="fas fa-mobile-alt me-1"></i><strong>Phones + Cases:</strong> 87% buy together</small>
                            </div>
                            <div class="alert alert-info border-0 p-2 mb-2">
                                <small><i class="fas fa-laptop me-1"></i><strong>Laptops + Mice:</strong> 65% buy together</small>
                            </div>
                            <div class="alert alert-warning border-0 p-2 mb-2">
                                <small><i class="fas fa-headphones me-1"></i><strong>Headphones + Cables:</strong> 54% buy together</small>
                            </div>
                            <div class="alert alert-primary border-0 p-2">
                                <small><i class="fas fa-bullseye me-1"></i><strong>Opportunity:</strong> Cross-sell can increase revenue by 23%</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create market basket association chart
    const basketData = [
        {
            x: ['Phone + Case', 'Laptop + Mouse', 'Headphones + Cable', 'Book + Bookmark', 'Shirt + Pants'],
            y: [87, 65, 54, 43, 38],
            type: 'bar',
            name: 'Association Strength (%)',
            marker: {color: '#2ecc71'}
        }
    ];
    
    Plotly.newPlot('basketChart', basketData, {
        title: 'Product Association Strength',
        xaxis: {title: 'Product Combinations'},
        yaxis: {title: 'Association Strength (%)'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Pricing Analysis
function runPricingAnalysis() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Analyzing pricing optimization...', 'Evaluating price elasticity and optimization opportunities...');
    
    setTimeout(() => {
        hideLoading();
        showPricingAnalysisResults();
    }, 2400);
}

function showPricingAnalysisResults() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-dollar-sign me-2"></i>Pricing Analysis & Optimization</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="chart-container">
                            <div id="pricingChart"></div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="insight-card p-3 rounded">
                            <h6 class="text-primary mb-3">
                                <i class="fas fa-tag me-1"></i>Pricing Insights
                            </h6>
                            <div class="alert alert-success border-0 p-2 mb-2">
                                <small><i class="fas fa-arrow-up me-1"></i><strong>Electronics:</strong> Can increase price by 8%</small>
                            </div>
                            <div class="alert alert-warning border-0 p-2 mb-2">
                                <small><i class="fas fa-minus me-1"></i><strong>Books:</strong> Price-sensitive category</small>
                            </div>
                            <div class="alert alert-info border-0 p-2 mb-2">
                                <small><i class="fas fa-balance-scale me-1"></i><strong>Optimal:</strong> Clothing prices well positioned</small>
                            </div>
                            <div class="alert alert-primary border-0 p-2">
                                <small><i class="fas fa-coins me-1"></i><strong>Revenue Impact:</strong> +€67K with price optimization</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create pricing elasticity chart
    const pricingData = [
        {
            x: ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports'],
            y: [0.3, 0.8, 1.4, 0.6, 0.9],
            type: 'bar',
            name: 'Price Elasticity',
            marker: {color: ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']}
        }
    ];
    
    Plotly.newPlot('pricingChart', pricingData, {
        title: 'Price Elasticity by Category',
        xaxis: {title: 'Product Category'},
        yaxis: {title: 'Price Elasticity'},
        margin: {t: 50, r: 50, b: 50, l: 80}
    });
}

// Executive Report
function generateExecutiveReport() {
    if (!currentData) {
        alert('Please load data first!');
        return;
    }
    
    showLoading('Generating executive report...', 'Compiling comprehensive business insights...');
    
    setTimeout(() => {
        hideLoading();
        showExecutiveReport();
    }, 3500);
}

function showExecutiveReport() {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="card analysis-card fade-in">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0"><i class="fas fa-file-contract me-2"></i>Executive Summary Report</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        <div class="executive-summary p-4 rounded border">
                            <h4 class="text-dark mb-4"><i class="fas fa-chart-line me-2"></i>Business Performance Overview</h4>
                            
                            <div class="row mb-4">
                                <div class="col-md-3 text-center">
                                    <div class="border rounded p-3 bg-light">
                                        <div class="h3 text-success mb-1">€780K</div>
                                        <small class="text-muted">Total Revenue</small>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="border rounded p-3 bg-light">
                                        <div class="h3 text-info mb-1">1,210</div>
                                        <small class="text-muted">Active Customers</small>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="border rounded p-3 bg-light">
                                        <div class="h3 text-warning mb-1">+24%</div>
                                        <small class="text-muted">YoY Growth</small>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="border rounded p-3 bg-light">
                                        <div class="h3 text-primary mb-1">€2,850</div>
                                        <small class="text-muted">Avg CLV</small>
                                    </div>
                                </div>
                            </div>
                            
                            <h5 class="mb-3"><i class="fas fa-key me-2"></i>Key Findings</h5>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="alert alert-success border-0 mb-2">
                                        <strong>✓ Strong Growth:</strong> 24% year-over-year revenue increase
                                    </div>
                                    <div class="alert alert-success border-0 mb-2">
                                        <strong>✓ Customer Loyalty:</strong> 79.9% of customers are low churn risk
                                    </div>
                                    <div class="alert alert-success border-0">
                                        <strong>✓ Product Focus:</strong> Electronics driving 73% of revenue
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="alert alert-warning border-0 mb-2">
                                        <strong>⚠ Seasonal Dependency:</strong> 45% revenue increase in Q4
                                    </div>
                                    <div class="alert alert-warning border-0 mb-2">
                                        <strong>⚠ At-Risk Customers:</strong> 87 customers need retention focus
                                    </div>
                                    <div class="alert alert-info border-0">
                                        <strong>💡 Opportunity:</strong> Cross-selling can boost revenue 23%
                                    </div>
                                </div>
                            </div>
                            
                            <h5 class="mb-3"><i class="fas fa-bullseye me-2"></i>Strategic Recommendations</h5>
                            <ol class="list-group list-group-flush">
                                <li class="list-group-item border-0"><strong>Inventory Planning:</strong> Increase Q4 inventory by 25% for seasonal demand</li>
                                <li class="list-group-item border-0"><strong>Customer Retention:</strong> Launch targeted campaign for 87 high-risk customers</li>
                                <li class="list-group-item border-0"><strong>Pricing Optimization:</strong> Increase electronics prices by 8% for +€67K revenue</li>
                                <li class="list-group-item border-0"><strong>Cross-Selling:</strong> Implement "frequently bought together" recommendations</li>
                                <li class="list-group-item border-0"><strong>Market Expansion:</strong> Leverage 15% champion customers for referral program</li>
                            </ol>
                            
                            <div class="text-center mt-4">
                                <button class="btn btn-primary me-2" onclick="window.print()">
                                    <i class="fas fa-print me-1"></i>Print Report
                                </button>
                                <button class="btn btn-success" onclick="downloadReport()">
                                    <i class="fas fa-download me-1"></i>Download PDF
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Additional placeholder functions for remaining analysis types
function runSalesOptimization() {
    alert('Sales Optimization analysis coming soon! This feature will identify the best sales strategies and conversion opportunities.');
}

function runSentimentAnalysis() {
    alert('Sentiment Analysis coming soon! This feature will analyze customer feedback and reviews to understand satisfaction levels.');
}

function runCohortAnalysis() {
    alert('Cohort Analysis coming soon! This feature will track customer behavior over time to understand retention patterns.');
}

function runCompetitorAnalysis() {
    alert('Competitor Analysis coming soon! This feature will benchmark your performance against industry standards.');
}

function runPredictiveModels() {
    alert('Predictive Models coming soon! This feature will create custom AI models for your specific business needs.');
}

function runRecommendationEngine() {
    alert('Recommendation Engine coming soon! This feature will provide personalized product and content recommendations.');
}

function downloadReport() {
    alert('PDF download feature coming soon! This will generate a comprehensive business report for download.');
}

console.log('DataSight AI Platform ready! 🚀');
console.log('Enhanced with 16+ analysis types! 📊');
