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

console.log('DataSight AI Platform ready! 🚀');
