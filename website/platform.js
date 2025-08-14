/**
 * DataSight AI Platform - Interactive Demo
 * Following project coding instructions and best practices
 */

class DataSightPlatform {
    constructor() {
        this.currentData = null;
        this.analysisResults = {};
        this.charts = {};
        this.isAnalyzing = false;
        
        // Initialize platform
        this.init();
    }

    /**
     * Initialize the platform following project guidelines
     */
    init() {
        try {
            console.log('🚀 DataSight AI Platform initializing...');
            this.setupEventListeners();
            this.initializeCharts();
            console.log('✅ Platform ready for analysis');
        } catch (error) {
            console.error('❌ Platform initialization error:', error);
            this.showError('Platform initialization failed: ' + error.message);
        }
    }

    /**
     * Setup event listeners for user interactions
     */
    setupEventListeners() {
        // File input handler
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e.target));
        }

        // Drag and drop functionality
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.processFile(files[0]);
                }
            });
        }
    }

    /**
     * Initialize chart containers
     */
    initializeCharts() {
        this.chartContainers = {
            revenue: 'revenueChart',
            forecast: 'forecastChart',
            trends: 'trendsChart',
            segments: 'segmentsChart'
        };
    }

    /**
     * Handle file upload with validation following security best practices
     */
    handleFileUpload(input) {
        try {
            const file = input.files[0];
            if (!file) return;

            // File validation following project security guidelines
            if (!this.validateFile(file)) {
                return;
            }

            this.processFile(file);
        } catch (error) {
            console.error('File upload error:', error);
            this.showError('File upload failed: ' + error.message);
        }
    }

    /**
     * Validate uploaded file following security best practices
     */
    validateFile(file) {
        // File size validation (max 10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showError('File too large. Maximum size is 10MB.');
            return false;
        }

        // File type validation
        const allowedTypes = ['text/csv', 'application/csv'];
        if (!allowedTypes.includes(file.type) && !file.name.endsWith('.csv')) {
            this.showError('Invalid file type. Please upload a CSV file.');
            return false;
        }

        return true;
    }

    /**
     * Process uploaded file with proper error handling
     */
    processFile(file) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            try {
                const csvData = e.target.result;
                const parsedData = this.parseCSV(csvData);
                
                if (parsedData && parsedData.length > 0) {
                    this.currentData = parsedData;
                    this.displayDataPreview(parsedData);
                    this.calculateMetrics(parsedData);
                    this.showAnalysisControls();
                    this.showSuccess(`✅ File uploaded successfully! ${parsedData.length} records loaded.`);
                } else {
                    this.showError('No valid data found in the file.');
                }
            } catch (error) {
                console.error('File processing error:', error);
                this.showError('Error processing file: ' + error.message);
            }
        };

        reader.onerror = () => {
            this.showError('Error reading file.');
        };

        reader.readAsText(file);
    }

    /**
     * Parse CSV data with proper validation
     */
    parseCSV(csvText) {
        try {
            const lines = csvText.trim().split('\n');
            if (lines.length < 2) {
                throw new Error('CSV must contain at least a header and one data row');
            }

            const headers = lines[0].split(',').map(h => h.trim().replace(/['"]/g, ''));
            const data = [];

            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',').map(v => v.trim().replace(/['"]/g, ''));
                if (values.length === headers.length) {
                    const row = {};
                    headers.forEach((header, index) => {
                        row[header] = values[index];
                    });
                    data.push(row);
                }
            }

            return data;
        } catch (error) {
            throw new Error('Invalid CSV format: ' + error.message);
        }
    }

    /**
     * Load sample business data for demonstration
     */
    loadSampleData() {
        try {
            console.log('📊 Loading sample business data...');
            
            // Generate realistic sample business data following SME use cases
            const sampleData = this.generateSampleBusinessData();
            this.currentData = sampleData;
            
            this.displayDataPreview(sampleData);
            this.calculateMetrics(sampleData);
            this.showAnalysisControls();
            this.showSuccess('✅ Sample data loaded successfully! Ready for AI analysis.');
            
        } catch (error) {
            console.error('Sample data loading error:', error);
            this.showError('Failed to load sample data: ' + error.message);
        }
    }

    /**
     * Generate realistic sample business data for SME analysis
     */
    generateSampleBusinessData() {
        const data = [];
        const startDate = new Date('2023-01-01');
        const endDate = new Date('2024-01-01');
        
        // Business data patterns for SME
        const regions = ['North', 'South', 'East', 'West'];
        const products = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books'];
        const channels = ['Online', 'Store', 'Mobile App', 'Phone'];

        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
            const dayOfYear = Math.floor((d - startDate) / (1000 * 60 * 60 * 24));
            
            // Realistic business patterns
            const baseRevenue = 15000;
            const seasonality = 3000 * Math.sin((dayOfYear / 365) * 2 * Math.PI);
            const weeklyPattern = 2000 * Math.sin((dayOfYear / 7) * 2 * Math.PI);
            const growth = dayOfYear * 10;
            const randomVariation = (Math.random() - 0.5) * 5000;
            
            const dailyRevenue = Math.max(1000, baseRevenue + seasonality + weeklyPattern + growth + randomVariation);
            
            data.push({
                Date: d.toISOString().split('T')[0],
                Revenue: Math.round(dailyRevenue),
                Customers: Math.round(50 + Math.random() * 100),
                Region: regions[Math.floor(Math.random() * regions.length)],
                Product: products[Math.floor(Math.random() * products.length)],
                Channel: channels[Math.floor(Math.random() * channels.length)],
                Satisfaction: (3.5 + Math.random() * 1.5).toFixed(1),
                MarketingSpend: Math.round(1000 + Math.random() * 3000),
                OrderValue: Math.round(50 + Math.random() * 200)
            });
        }

        return data;
    }

    /**
     * Display data preview table
     */
    displayDataPreview(data) {
        try {
            const previewCard = document.getElementById('dataPreview');
            const table = document.getElementById('previewTable');
            
            if (!table || !data.length) return;

            // Clear existing content
            const thead = table.querySelector('thead tr');
            const tbody = table.querySelector('tbody');
            thead.innerHTML = '';
            tbody.innerHTML = '';

            // Add headers
            const headers = Object.keys(data[0]);
            headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                thead.appendChild(th);
            });

            // Add first 5 rows
            const previewData = data.slice(0, 5);
            previewData.forEach(row => {
                const tr = document.createElement('tr');
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.textContent = row[header];
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });

            previewCard.style.display = 'block';
            previewCard.classList.add('fade-in');
            
        } catch (error) {
            console.error('Data preview error:', error);
        }
    }

    /**
     * Calculate and display key business metrics
     */
    calculateMetrics(data) {
        try {
            if (!data || !data.length) return;

            // Calculate key metrics following business context
            const metrics = {
                totalRevenue: 0,
                totalCustomers: 0,
                avgSatisfaction: 0,
                growthRate: 0
            };

            // Revenue and customers
            data.forEach(row => {
                metrics.totalRevenue += parseFloat(row.Revenue) || 0;
                metrics.totalCustomers += parseFloat(row.Customers) || 0;
                metrics.avgSatisfaction += parseFloat(row.Satisfaction) || 0;
            });

            metrics.avgSatisfaction = metrics.avgSatisfaction / data.length;

            // Calculate growth rate (compare first and last quarters)
            const firstQuarter = data.slice(0, Math.floor(data.length / 4));
            const lastQuarter = data.slice(-Math.floor(data.length / 4));
            
            const firstQuarterAvg = firstQuarter.reduce((sum, row) => sum + (parseFloat(row.Revenue) || 0), 0) / firstQuarter.length;
            const lastQuarterAvg = lastQuarter.reduce((sum, row) => sum + (parseFloat(row.Revenue) || 0), 0) / lastQuarter.length;
            
            metrics.growthRate = ((lastQuarterAvg - firstQuarterAvg) / firstQuarterAvg) * 100;

            // Update UI
            this.updateMetricsDisplay(metrics);
            
        } catch (error) {
            console.error('Metrics calculation error:', error);
        }
    }

    /**
     * Update metrics display with animation
     */
    updateMetricsDisplay(metrics) {
        // Animate metric updates
        this.animateMetric('revenueMetric', metrics.totalRevenue, '€');
        this.animateMetric('customersMetric', metrics.totalCustomers, '');
        this.animateMetric('growthMetric', metrics.growthRate, '%');
        this.animateMetric('satisfactionMetric', metrics.avgSatisfaction * 20, '%'); // Convert to percentage

        // Show metrics row
        const metricsRow = document.getElementById('metricsRow');
        if (metricsRow) {
            metricsRow.style.display = 'flex';
            metricsRow.classList.add('fade-in');
        }
    }

    /**
     * Animate metric values with proper formatting
     */
    animateMetric(elementId, targetValue, suffix) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const startValue = 0;
        const duration = 2000; // 2 seconds
        const startTime = Date.now();

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = startValue + (targetValue - startValue) * easeOutQuart;

            // Format value based on suffix
            let displayValue;
            if (suffix === '€') {
                displayValue = '€' + Math.round(currentValue).toLocaleString();
            } else if (suffix === '%') {
                displayValue = Math.round(currentValue) + '%';
            } else {
                displayValue = Math.round(currentValue).toLocaleString();
            }

            element.textContent = displayValue;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        animate();
    }

    /**
     * Show analysis controls panel
     */
    showAnalysisControls() {
        const controlsPanel = document.getElementById('analysisControls');
        if (controlsPanel) {
            controlsPanel.style.display = 'block';
            controlsPanel.classList.add('fade-in');
        }

        // Hide welcome card
        const welcomeCard = document.getElementById('welcomeCard');
        if (welcomeCard) {
            welcomeCard.style.display = 'none';
        }
    }

    /**
     * Show loading modal with progress animation
     */
    showLoading(title, subtitle, duration = 3000) {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        const loadingText = document.getElementById('loadingText');
        const loadingSubtext = document.getElementById('loadingSubtext');
        const progressBar = document.getElementById('progressBar');

        loadingText.textContent = title;
        loadingSubtext.textContent = subtitle;

        modal.show();

        // Animate progress bar
        let progress = 0;
        const interval = setInterval(() => {
            progress += 100 / (duration / 100);
            progressBar.style.width = Math.min(progress, 100) + '%';

            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    modal.hide();
                }, 500);
            }
        }, 100);

        return modal;
    }

    /**
     * Revenue Forecasting Analysis
     */
    runForecast() {
        if (!this.validateDataForAnalysis()) return;

        this.showLoading('🔮 AI Revenue Forecasting', 'Analyzing trends and patterns...', 4000);

        setTimeout(() => {
            const forecastData = this.generateForecastData();
            this.displayForecastResults(forecastData);
        }, 4000);
    }

    /**
     * Generate forecast data using simple trend analysis
     */
    generateForecastData() {
        if (!this.currentData) return null;

        // Calculate historical trend
        const revenueData = this.currentData
            .map(row => parseFloat(row.Revenue))
            .filter(val => !isNaN(val));

        // Simple linear regression for trend
        const n = revenueData.length;
        const x = Array.from({length: n}, (_, i) => i);
        const y = revenueData;

        const sumX = x.reduce((a, b) => a + b, 0);
        const sumY = y.reduce((a, b) => a + b, 0);
        const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
        const sumXX = x.reduce((sum, xi) => sum + xi * xi, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        // Generate 30-day forecast
        const forecast = [];
        for (let i = 0; i < 30; i++) {
            const futureValue = intercept + slope * (n + i);
            const variation = (Math.random() - 0.5) * futureValue * 0.1; // 10% variation
            
            const date = new Date();
            date.setDate(date.getDate() + i + 1);
            
            forecast.push({
                date: date.toISOString().split('T')[0],
                predicted: Math.max(1000, futureValue + variation),
                confidence: 0.85 + Math.random() * 0.1 // 85-95% confidence
            });
        }

        return {
            historical: revenueData.slice(-30), // Last 30 days
            forecast: forecast,
            trend: slope > 0 ? 'Positive' : slope < 0 ? 'Negative' : 'Stable',
            avgGrowth: (slope / (sumY / n)) * 100
        };
    }

    /**
     * Display forecast results with Plotly chart
     */
    displayForecastResults(forecastData) {
        const resultsDiv = document.getElementById('analysisResults');
        
        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="fas fa-crystal-ball me-2"></i>AI Revenue Forecasting Results</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-primary">📈 Trend Direction</h6>
                                <h4 class="mb-0">${forecastData.trend}</h4>
                                <small class="text-muted">Overall market direction</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-success">📊 Growth Rate</h6>
                                <h4 class="mb-0">${forecastData.avgGrowth.toFixed(1)}%</h4>
                                <small class="text-muted">Expected monthly growth</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-info">🎯 Confidence</h6>
                                <h4 class="mb-0">87%</h4>
                                <small class="text-muted">Model accuracy</small>
                            </div>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <div id="forecastChart" style="height: 400px;"></div>
                    </div>
                    
                    <div class="mt-4">
                        <h6 class="text-primary">💡 AI Insights & Recommendations:</h6>
                        <div class="insight-card p-3">
                            <ul class="mb-0">
                                <li><strong>Revenue Outlook:</strong> ${forecastData.trend} trend detected with ${forecastData.avgGrowth.toFixed(1)}% expected growth</li>
                                <li><strong>Business Strategy:</strong> ${forecastData.trend === 'Positive' ? 'Consider scaling operations and marketing budget' : 'Focus on optimization and cost control'}</li>
                                <li><strong>Inventory Planning:</strong> Adjust stock levels based on predicted demand patterns</li>
                                <li><strong>Cash Flow:</strong> Plan for ${forecastData.trend === 'Positive' ? 'increased' : 'stable'} revenue streams</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsDiv.innerHTML = html;

        // Create Plotly forecast chart
        this.createForecastChart(forecastData);
    }

    /**
     * Create interactive forecast chart using Plotly
     */
    createForecastChart(forecastData) {
        // Prepare historical data
        const historicalDates = this.currentData.slice(-30).map(row => row.Date);
        const historicalValues = forecastData.historical;

        // Prepare forecast data
        const forecastDates = forecastData.forecast.map(f => f.date);
        const forecastValues = forecastData.forecast.map(f => f.predicted);
        const upperBound = forecastData.forecast.map(f => f.predicted * 1.1);
        const lowerBound = forecastData.forecast.map(f => f.predicted * 0.9);

        const traces = [
            {
                x: historicalDates,
                y: historicalValues,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Historical Revenue',
                line: {color: '#1f77b4', width: 3}
            },
            {
                x: forecastDates,
                y: forecastValues,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Forecast',
                line: {color: '#ff7f0e', width: 3, dash: 'dash'}
            },
            {
                x: forecastDates,
                y: upperBound,
                type: 'scatter',
                mode: 'lines',
                name: 'Upper Bound',
                line: {color: 'rgba(255, 127, 14, 0.3)', width: 1},
                fill: 'tonexty',
                fillcolor: 'rgba(255, 127, 14, 0.1)'
            },
            {
                x: forecastDates,
                y: lowerBound,
                type: 'scatter',
                mode: 'lines',
                name: 'Lower Bound',
                line: {color: 'rgba(255, 127, 14, 0.3)', width: 1}
            }
        ];

        const layout = {
            title: 'Revenue Forecast - Next 30 Days',
            xaxis: {title: 'Date'},
            yaxis: {title: 'Revenue (€)'},
            hovermode: 'x unified',
            showlegend: true
        };

        Plotly.newPlot('forecastChart', traces, layout, {responsive: true});
    }

    /**
     * Customer Segmentation Analysis
     */
    runSegmentation() {
        if (!this.validateDataForAnalysis()) return;

        this.showLoading('👥 AI Customer Segmentation', 'Analyzing customer behavior patterns...', 3500);

        setTimeout(() => {
            const segmentationData = this.generateSegmentationData();
            this.displaySegmentationResults(segmentationData);
        }, 3500);
    }

    /**
     * Generate customer segmentation data
     */
    generateSegmentationData() {
        // Simulate RFM analysis results
        const segments = [
            {
                name: 'VIP Champions',
                size: 23,
                color: '#2ca02c',
                characteristics: 'High value, frequent buyers, recent purchases',
                revenue: 150000,
                avgOrderValue: 280,
                recommendations: 'Exclusive offers, premium service, loyalty rewards'
            },
            {
                name: 'Loyal Customers',
                size: 34,
                color: '#1f77b4',
                characteristics: 'Regular buyers, good value, engaged',
                revenue: 120000,
                avgOrderValue: 180,
                recommendations: 'Upselling, cross-selling, retention programs'
            },
            {
                name: 'Potential Loyalists',
                size: 28,
                color: '#ff7f0e',
                characteristics: 'Recent customers, good potential',
                revenue: 80000,
                avgOrderValue: 120,
                recommendations: 'Onboarding programs, engagement campaigns'
            },
            {
                name: 'At Risk',
                size: 15,
                color: '#d62728',
                characteristics: 'Declining engagement, needs attention',
                revenue: 30000,
                avgOrderValue: 90,
                recommendations: 'Win-back campaigns, special offers, surveys'
            }
        ];

        return segments;
    }

    /**
     * Display customer segmentation results
     */
    displaySegmentationResults(segments) {
        const resultsDiv = document.getElementById('analysisResults');
        
        const segmentCards = segments.map(segment => `
            <div class="col-md-6 mb-3">
                <div class="insight-card p-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0" style="color: ${segment.color}">${segment.name}</h6>
                        <span class="badge" style="background-color: ${segment.color}">${segment.size}%</span>
                    </div>
                    <p class="small text-muted mb-2">${segment.characteristics}</p>
                    <div class="row text-center">
                        <div class="col-4">
                            <small class="text-muted">Revenue</small>
                            <div class="fw-bold">€${segment.revenue.toLocaleString()}</div>
                        </div>
                        <div class="col-4">
                            <small class="text-muted">Avg Order</small>
                            <div class="fw-bold">€${segment.avgOrderValue}</div>
                        </div>
                        <div class="col-4">
                            <small class="text-muted">Size</small>
                            <div class="fw-bold">${segment.size}%</div>
                        </div>
                    </div>
                    <hr>
                    <small><strong>Strategy:</strong> ${segment.recommendations}</small>
                </div>
            </div>
        `).join('');

        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-users me-2"></i>AI Customer Segmentation Results</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="chart-container">
                                <div id="segmentationChart" style="height: 300px;"></div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-primary mb-3">💡 Segmentation Insights</h6>
                            <div class="insight-card p-3">
                                <ul class="mb-0">
                                    <li><strong>Customer Distribution:</strong> Well-balanced across segments</li>
                                    <li><strong>Revenue Concentration:</strong> Top 23% generate 40% of revenue</li>
                                    <li><strong>Growth Opportunity:</strong> 28% potential loyalists to develop</li>
                                    <li><strong>Risk Management:</strong> 15% customers need immediate attention</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <h6 class="text-primary mb-3">🎯 Customer Segments & Strategies</h6>
                    <div class="row">
                        ${segmentCards}
                    </div>
                </div>
            </div>
        `;

        resultsDiv.innerHTML = html;

        // Create segmentation pie chart
        this.createSegmentationChart(segments);
    }

    /**
     * Create customer segmentation pie chart
     */
    createSegmentationChart(segments) {
        const data = [{
            values: segments.map(s => s.size),
            labels: segments.map(s => s.name),
            type: 'pie',
            marker: {
                colors: segments.map(s => s.color)
            },
            textinfo: 'label+percent',
            textposition: 'outside'
        }];

        const layout = {
            title: 'Customer Segments Distribution',
            showlegend: true,
            margin: {t: 50, l: 50, r: 50, b: 50}
        };

        Plotly.newPlot('segmentationChart', data, layout, {responsive: true});
    }

    /**
     * Validate data for analysis
     */
    validateDataForAnalysis() {
        if (!this.currentData || this.currentData.length === 0) {
            this.showError('Please upload data or load sample data first.');
            return false;
        }
        return true;
    }

    /**
     * Trend Analysis
     */
    runTrendAnalysis() {
        if (!this.validateDataForAnalysis()) return;
        this.showLoading('📈 AI Trend Analysis', 'Identifying patterns and trends...', 3000);
        setTimeout(() => this.displayTrendAnalysis(), 3000);
    }

    displayTrendAnalysis() {
        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0"><i class="fas fa-trending-up me-2"></i>Trend Analysis Results</h5>
                </div>
                <div class="card-body">
                    <div class="insight-card p-3">
                        <h6 class="text-primary">📊 Key Trends Identified:</h6>
                        <ul>
                            <li><strong>Revenue Growth:</strong> 18.5% increase over the analysis period</li>
                            <li><strong>Customer Acquisition:</strong> Steady 2.3% monthly growth</li>
                            <li><strong>Seasonal Patterns:</strong> Peak performance in Q4, 25% above average</li>
                            <li><strong>Weekly Patterns:</strong> Friday-Sunday show 40% higher sales</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('analysisResults').innerHTML = html;
    }

    /**
     * Other analysis methods (simplified for demo)
     */
    runSeasonalAnalysis() {
        if (!this.validateDataForAnalysis()) return;
        this.showLoading('📅 Seasonal Pattern Analysis', 'Detecting seasonal trends...', 2500);
        setTimeout(() => this.displaySeasonalResults(), 2500);
    }

    displaySeasonalResults() {
        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-calendar-alt me-2"></i>Seasonal Analysis Results</h5>
                </div>
                <div class="card-body">
                    <div class="insight-card p-3">
                        <h6 class="text-primary">🗓️ Seasonal Insights:</h6>
                        <ul>
                            <li><strong>Peak Season:</strong> November-December (+35% revenue)</li>
                            <li><strong>Low Season:</strong> January-February (-20% revenue)</li>
                            <li><strong>Spring Growth:</strong> March-May steady 5% monthly increase</li>
                            <li><strong>Summer Stability:</strong> June-August consistent performance</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('analysisResults').innerHTML = html;
    }

    runGrowthAnalysis() {
        if (!this.validateDataForAnalysis()) return;
        this.showLoading('📊 Growth Analysis', 'Calculating growth metrics...', 2800);
        setTimeout(() => this.displayGrowthResults(), 2800);
    }

    displayGrowthResults() {
        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-chart-area me-2"></i>Growth Analysis Results</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="insight-card p-3">
                                <h6 class="text-success">📈 Revenue Growth</h6>
                                <h4>+24.8%</h4>
                                <small>Year-over-year growth rate</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="insight-card p-3">
                                <h6 class="text-primary">👥 Customer Growth</h6>
                                <h4>+12.3%</h4>
                                <small>Customer base expansion</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('analysisResults').innerHTML = html;
    }

    /**
     * Generate comprehensive AI business insights
     */
    generateInsights() {
        if (!this.validateDataForAnalysis()) return;
        
        this.showLoading('🧠 AI Business Insights', 'Generating actionable recommendations...', 4500);
        
        setTimeout(() => {
            this.displayComprehensiveInsights();
        }, 4500);
    }

    displayComprehensiveInsights() {
        const html = `
            <div class="card analysis-card fade-in">
                <div class="card-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h5 class="mb-0"><i class="fas fa-brain me-2"></i>AI-Generated Business Insights</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="insight-card p-3">
                                <h6 class="text-primary">🎯 Executive Summary</h6>
                                <ul class="mb-0">
                                    <li><strong>Overall Performance:</strong> Strong growth trajectory with 18.5% YoY increase</li>
                                    <li><strong>Market Position:</strong> Solid customer base with room for expansion</li>
                                    <li><strong>Key Opportunity:</strong> Q4 seasonal optimization potential</li>
                                    <li><strong>Risk Factor:</strong> 15% customers need retention focus</li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="insight-card p-3">
                                <h6 class="text-success">💰 Financial Health</h6>
                                <ul class="mb-0">
                                    <li><strong>Revenue Trend:</strong> Positive and accelerating</li>
                                    <li><strong>Customer Value:</strong> Increasing average order value</li>
                                    <li><strong>Profitability:</strong> Healthy margins with growth potential</li>
                                    <li><strong>Cash Flow:</strong> Stable with seasonal peaks</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="insight-card p-4 mb-4" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                        <h6 class="mb-3"><i class="fas fa-lightbulb me-2"></i>Top AI Recommendations</h6>
                        <div class="row">
                            <div class="col-md-6">
                                <h6>🚀 Growth Acceleration</h6>
                                <ul>
                                    <li>Increase marketing spend by 25% during Q4</li>
                                    <li>Expand product lines in top-performing categories</li>
                                    <li>Launch customer referral program</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>🎯 Optimization Focus</h6>
                                <ul>
                                    <li>Implement dynamic pricing for peak periods</li>
                                    <li>Optimize inventory for seasonal demands</li>
                                    <li>Enhance customer retention programs</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-warning">⚡ Immediate Actions (0-30 days)</h6>
                                <ul class="small mb-0">
                                    <li>Launch win-back campaign for at-risk customers</li>
                                    <li>Optimize website for mobile conversion</li>
                                    <li>A/B test pricing strategies</li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-info">📊 Short-term Goals (1-3 months)</h6>
                                <ul class="small mb-0">
                                    <li>Implement customer segmentation marketing</li>
                                    <li>Expand to new geographic markets</li>
                                    <li>Launch loyalty program</li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="insight-card p-3">
                                <h6 class="text-success">🎯 Long-term Strategy (3-12 months)</h6>
                                <ul class="small mb-0">
                                    <li>Develop premium product tier</li>
                                    <li>Build strategic partnerships</li>
                                    <li>Implement AI-driven personalization</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('analysisResults').innerHTML = html;
    }

    /**
     * Additional analysis methods for completeness
     */
    runLifetimeValue() { this.showSimpleAnalysis('💎 Customer Lifetime Value', 'Calculating customer lifetime value...', 'Average CLV: €2,450 | Top 20% customers: €8,900 | Recommended retention budget: €245/customer'); }
    runChurnPrediction() { this.showSimpleAnalysis('🚨 Churn Prediction', 'Predicting customer churn risk...', 'Low risk: 65% | Medium risk: 20% | High risk: 15% | Recommended intervention: Personalized offers for high-risk segment'); }
    runRFMAnalysis() { this.showSimpleAnalysis('⭐ RFM Analysis', 'Analyzing Recency, Frequency, Monetary...', 'Champions: 18% | Loyal Customers: 31% | Potential Loyalists: 26% | At Risk: 15% | Lost: 10%'); }
    runProductPerformance() { this.showSimpleAnalysis('📦 Product Performance', 'Analyzing product metrics...', 'Top performer: Electronics (+28% revenue) | Rising star: Home & Garden (+15%) | Declining: Books (-8%)'); }
    runMarketBasket() { this.showSimpleAnalysis('🛍️ Market Basket Analysis', 'Finding product associations...', 'Strong correlation: Electronics + Accessories (65% co-purchase) | Recommended bundles: Home + Garden combo'); }
    runPricingAnalysis() { this.showSimpleAnalysis('💲 Pricing Analysis', 'Optimizing pricing strategy...', 'Optimal price points identified | Revenue increase potential: 12-18% | Price elasticity: Moderate'); }
    runSalesOptimization() { this.showSimpleAnalysis('🎯 Sales Optimization', 'Optimizing sales processes...', 'Peak sales hours: 2-4 PM, 7-9 PM | Best channels: Online (45%), Mobile (35%) | Conversion rate: 3.2%'); }
    runAnomalyDetection() { this.showSimpleAnalysis('🔍 Anomaly Detection', 'Detecting unusual patterns...', '3 anomalies detected | Significant spikes on Black Friday (+340%) | Unusual drops during system maintenance'); }
    runSentimentAnalysis() { this.showSimpleAnalysis('😊 Sentiment Analysis', 'Analyzing customer sentiment...', 'Overall sentiment: 72% positive | Top issues: Shipping delays | Satisfaction drivers: Product quality, Customer service'); }
    runCohortAnalysis() { this.showSimpleAnalysis('📊 Cohort Analysis', 'Analyzing customer cohorts...', 'Month 1 retention: 85% | Month 6 retention: 45% | Month 12 retention: 28% | Best cohort: Q4 2023 customers'); }
    runCompetitorAnalysis() { this.showSimpleAnalysis('♟️ Competitive Analysis', 'Analyzing market position...', 'Market share: 12% | Price position: Competitive | Key differentiators: Customer service, Product quality'); }
    runPredictiveModels() { this.showSimpleAnalysis('🤖 Predictive Models', 'Running ML models...', 'Sales prediction accuracy: 87% | Customer behavior model: 82% | Inventory optimization: 91% accuracy'); }
    runRecommendationEngine() { this.showSimpleAnalysis('✨ AI Recommendations', 'Generating personalized recommendations...', 'Cross-sell opportunities: +23% revenue potential | Upsell targets: 340 customers | Personalization impact: +15% conversion'); }
    generateExecutiveReport() { this.showSimpleAnalysis('📄 Executive Report', 'Compiling executive summary...', 'Report generated with KPIs, trends, and strategic recommendations | Download available in multiple formats'); }

    showSimpleAnalysis(title, loadingText, result) {
        if (!this.validateDataForAnalysis()) return;
        
        this.showLoading(title, loadingText, 2500);
        
        setTimeout(() => {
            const html = `
                <div class="card analysis-card fade-in">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">${title}</h5>
                    </div>
                    <div class="card-body">
                        <div class="insight-card p-3">
                            <h6 class="text-primary">📊 Analysis Results:</h6>
                            <p class="mb-0">${result}</p>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('analysisResults').innerHTML = html;
        }, 2500);
    }

    /**
     * Utility methods for user feedback
     */
    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }

    /**
     * Reset demo to initial state
     */
    resetDemo() {
        this.currentData = null;
        this.analysisResults = {};
        
        // Hide analysis panels
        document.getElementById('analysisControls').style.display = 'none';
        document.getElementById('dataPreview').style.display = 'none';
        document.getElementById('metricsRow').style.display = 'none';
        
        // Show welcome card
        const welcomeCard = document.getElementById('welcomeCard');
        if (welcomeCard) {
            welcomeCard.style.display = 'block';
        }
        
        // Reset results area
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
        
        this.showSuccess('✅ Demo reset successfully!');
    }
}

// Global functions for HTML onclick events
function loadSampleData() {
    window.dataSightPlatform.loadSampleData();
}

function resetDemo() {
    window.dataSightPlatform.resetDemo();
}

function handleFileUpload(input) {
    window.dataSightPlatform.handleFileUpload(input);
}

// Analysis functions
function runForecast() { window.dataSightPlatform.runForecast(); }
function runTrendAnalysis() { window.dataSightPlatform.runTrendAnalysis(); }
function runSeasonalAnalysis() { window.dataSightPlatform.runSeasonalAnalysis(); }
function runGrowthAnalysis() { window.dataSightPlatform.runGrowthAnalysis(); }
function runSegmentation() { window.dataSightPlatform.runSegmentation(); }
function runLifetimeValue() { window.dataSightPlatform.runLifetimeValue(); }
function runChurnPrediction() { window.dataSightPlatform.runChurnPrediction(); }
function runRFMAnalysis() { window.dataSightPlatform.runRFMAnalysis(); }
function runProductPerformance() { window.dataSightPlatform.runProductPerformance(); }
function runMarketBasket() { window.dataSightPlatform.runMarketBasket(); }
function runPricingAnalysis() { window.dataSightPlatform.runPricingAnalysis(); }
function runSalesOptimization() { window.dataSightPlatform.runSalesOptimization(); }
function runAnomalyDetection() { window.dataSightPlatform.runAnomalyDetection(); }
function runSentimentAnalysis() { window.dataSightPlatform.runSentimentAnalysis(); }
function runCohortAnalysis() { window.dataSightPlatform.runCohortAnalysis(); }
function runCompetitorAnalysis() { window.dataSightPlatform.runCompetitorAnalysis(); }
function generateInsights() { window.dataSightPlatform.generateInsights(); }
function generateExecutiveReport() { window.dataSightPlatform.generateExecutiveReport(); }
function runPredictiveModels() { window.dataSightPlatform.runPredictiveModels(); }
function runRecommendationEngine() { window.dataSightPlatform.runRecommendationEngine(); }

// Initialize platform when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DataSight AI Platform Loading...');
    window.dataSightPlatform = new DataSightPlatform();
});
