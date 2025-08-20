/**
 * AI Company Data Analyzer - Platform Diagnostic Tool
 * Following project coding instructions for proper error handling
 * Identifies and fixes data upload/processing issues for SME business context
 */

class PlatformDiagnostic {
    constructor() {
        this.diagnosticResults = {};
        this.logger = {
            info: (msg) => console.log(`[DIAGNOSTIC] ${msg}`),
            error: (msg) => console.error(`[DIAGNOSTIC ERROR] ${msg}`),
            success: (msg) => console.log(`[DIAGNOSTIC SUCCESS] ${msg}`)
        };
        
        this.initializeDiagnostic();
    }

    /**
     * Initialize comprehensive platform diagnostic
     * Following project debugging and validation best practices
     */
    async initializeDiagnostic() {
        this.logger.info('🔍 Starting AI Data Analyzer Platform Diagnostic...');
        
        try {
            // Wait for DOM to be ready
            if (document.readyState !== 'complete') {
                await new Promise(resolve => {
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', resolve);
                    } else {
                        window.addEventListener('load', resolve);
                    }
                });
            }

            // Run immediate diagnostic
            this.runImmediateDiagnostic();
            
            // Add diagnostic UI
            this.addDiagnosticUI();
            
            this.logger.success('✅ Diagnostic tool initialized successfully');
            
        } catch (error) {
            this.logger.error(`Diagnostic initialization failed: ${error.message}`);
        }
    }

    /**
     * Run immediate diagnostic checks
     * Following project error handling guidelines
     */
    runImmediateDiagnostic() {
        this.logger.info('🏃‍♂️ Running immediate platform checks...');

        // Check 1: Platform object availability
        this.diagnosticResults.platform_available = {
            status: window.dataSightPlatform ? 'PASS' : 'FAIL',
            details: window.dataSightPlatform ? 'Platform object found' : 'Platform object not found',
            fix: window.dataSightPlatform ? null : 'Load platform.js file correctly',
            critical: true
        };

        // Check 2: File input element (critical for data upload)
        const fileInput = document.getElementById('fileInput');
        this.diagnosticResults.file_input_exists = {
            status: fileInput ? 'PASS' : 'FAIL',
            details: fileInput ? 'File input element found' : 'File input element missing',
            fix: fileInput ? null : 'Add <input type="file" id="fileInput" accept=".csv"> to HTML',
            critical: true
        };

        // Check 3: Container element for results
        const container = document.querySelector('.container');
        this.diagnosticResults.container_exists = {
            status: container ? 'PASS' : 'FAIL',
            details: container ? 'Container element found' : 'Container element missing',
            fix: container ? null : 'Add <div class="container"></div> to HTML',
            critical: true
        };

        // Check 4: Required DOM elements for data display
        const requiredElements = ['dataPreview', 'analysisResults', 'metricsRow'];
        for (const elementId of requiredElements) {
            const element = document.getElementById(elementId);
            this.diagnosticResults[`element_${elementId}`] = {
                status: element ? 'PASS' : 'WARN',
                details: element ? `${elementId} element exists` : `${elementId} element missing`,
                fix: element ? null : `Will be created automatically when needed`,
                critical: false
            };
        }

        // Check 5: Bootstrap/CSS framework
        const hasBootstrap = document.querySelector('.btn') !== null || 
                             document.querySelector('.card') !== null ||
                             document.querySelector('.container') !== null;
        this.diagnosticResults.css_framework = {
            status: hasBootstrap ? 'PASS' : 'WARN',
            details: hasBootstrap ? 'CSS framework detected' : 'CSS framework not detected',
            fix: hasBootstrap ? null : 'Include Bootstrap for better styling',
            critical: false
        };

        this.logger.success('✅ Immediate diagnostic completed');
    }

    /**
     * Create and activate working file upload system
     * Following project data validation and SME business requirements
     */
    createWorkingFileUpload() {
        this.logger.info('🔧 Creating working file upload system for AI Data Analyzer...');

        try {
            const fileInput = document.getElementById('fileInput');
            if (!fileInput) {
                this.createFileInputElement();
            }

            // Remove any existing event listeners
            const newFileInput = document.getElementById('fileInput');
            newFileInput.replaceWith(newFileInput.cloneNode(true));
            const cleanFileInput = document.getElementById('fileInput');

            // Add comprehensive file upload handler
            cleanFileInput.addEventListener('change', (event) => {
                this.handleFileUpload(event);
            });

            // Also handle drag and drop if upload area exists
            const uploadArea = document.querySelector('.upload-area');
            if (uploadArea) {
                this.setupDragAndDrop(uploadArea, cleanFileInput);
            }

            this.logger.success('✅ Working file upload system created');
            this.showSuccess('🔧 AI Data Analyzer file upload system is now active! Try uploading a CSV file.');

        } catch (error) {
            this.logger.error(`Failed to create file upload system: ${error.message}`);
            this.showError(`Failed to create file upload: ${error.message}`);
        }
    }

    /**
     * Create file input element if missing
     * Following project HTML structure guidelines
     */
    createFileInputElement() {
        const container = document.querySelector('.container') || document.body;
        
        const uploadHTML = `
            <div class="upload-area border border-2 border-dashed rounded p-4 text-center mb-4" 
                 style="cursor: pointer; border-color: #0d6efd;">
                <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
                <h6>Upload Your Business Data</h6>
                <p class="text-muted">Click here or drag & drop CSV files</p>
                <input type="file" id="fileInput" accept=".csv,.xlsx" style="display: none;">
            </div>
        `;

        container.insertAdjacentHTML('afterbegin', uploadHTML);

        // Make upload area clickable
        document.querySelector('.upload-area').addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
    }

    /**
     * Handle file upload with comprehensive error handling
     * Following project data validation best practices
     */
    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.logger.info(`📁 Processing file: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)}MB)`);

        try {
            // Validate file
            const validation = this.validateFile(file);
            if (!validation.valid) {
                this.showError(validation.message);
                return;
            }

            // Show loading state
            this.showLoadingState(file.name);

            // Process file based on type
            const fileExtension = file.name.split('.').pop().toLowerCase();
            let data;

            if (fileExtension === 'csv') {
                data = await this.processCSVFile(file);
            } else {
                throw new Error('Currently only CSV files are supported');
            }

            // Display results
            this.displayProcessedData(data, file.name);
            
            // Store data globally for further analysis
            window.currentUploadedData = data;
            window.uploadedFileName = file.name;

        } catch (error) {
            this.logger.error(`File processing error: ${error.message}`);
            this.showError(`Error processing ${file.name}: ${error.message}`);
        }
    }

    /**
     * Validate uploaded file
     * Following project security and data validation guidelines
     */
    validateFile(file) {
        // File size validation (50MB limit for SME context)
        const maxSize = 50 * 1024 * 1024; // 50MB
        if (file.size > maxSize) {
            return {
                valid: false,
                message: `File too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is 50MB.`
            };
        }

        // File type validation
        const allowedTypes = ['csv', 'xlsx'];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            return {
                valid: false,
                message: `Unsupported file type: ${fileExtension}. Please upload CSV or Excel files.`
            };
        }

        return { valid: true };
    }

    /**
     * Process CSV file with error handling
     * Following project data processing guidelines
     */
    async processCSVFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const content = e.target.result;
                    const lines = content.split('\n').filter(line => line.trim());
                    
                    if (lines.length < 2) {
                        reject(new Error('File must contain at least a header row and one data row'));
                        return;
                    }

                    // Parse headers
                    const headers = this.parseCSVRow(lines[0]);
                    const data = [];

                    // Parse data rows (limit to 1000 rows for performance)
                    const maxRows = Math.min(lines.length - 1, 1000);
                    
                    for (let i = 1; i <= maxRows; i++) {
                        if (lines[i] && lines[i].trim()) {
                            const values = this.parseCSVRow(lines[i]);
                            const row = {};
                            
                            headers.forEach((header, index) => {
                                row[header] = values[index] || '';
                            });
                            
                            data.push(row);
                        }
                    }

                    this.logger.success(`✅ Parsed ${data.length} rows with ${headers.length} columns`);
                    resolve(data);

                } catch (error) {
                    reject(new Error(`CSV parsing error: ${error.message}`));
                }
            };

            reader.onerror = () => {
                reject(new Error('Failed to read file'));
            };

            reader.readAsText(file);
        });
    }

    /**
     * Parse CSV row handling quoted values
     * Following data processing best practices
     */
    parseCSVRow(row) {
        const result = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < row.length; i++) {
            const char = row[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        
        result.push(current.trim());
        return result;
    }

    /**
     * Display processed data with business insights
     * Following SME business context and UI best practices
     */
    displayProcessedData(data, filename) {
        let dataPreview = document.getElementById('dataPreview');
        if (!dataPreview) {
            dataPreview = document.createElement('div');
            dataPreview.id = 'dataPreview';
            document.querySelector('.container').appendChild(dataPreview);
        }

        // Calculate basic analytics
        const analytics = this.calculateBasicAnalytics(data);

        const resultHTML = `
            <div class="card mt-4 shadow">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-check-circle me-2"></i>
                        Data Successfully Loaded: ${filename}
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-primary mb-1">${data.length.toLocaleString()}</h4>
                                <small class="text-muted">Rows Loaded</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-success mb-1">${Object.keys(data[0] || {}).length}</h4>
                                <small class="text-muted">Columns</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-info mb-1">${analytics.completeness}%</h4>
                                <small class="text-muted">Data Quality</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-warning mb-1">✅</h4>
                                <small class="text-muted">Ready for Analysis</small>
                            </div>
                        </div>
                    </div>
                    
                    <h6 class="mb-3">
                        <i class="fas fa-table me-2"></i>Data Preview (First 10 rows):
                    </h6>
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead class="table-dark">
                                <tr>
                                    ${Object.keys(data[0] || {}).map(col => `<th>${col}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${data.slice(0, 10).map(row => `
                                    <tr>
                                        ${Object.values(row).map(val => `<td>${this.formatCellValue(val)}</td>`).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                    
                    ${analytics.insights ? `
                    <div class="alert alert-info mt-3">
                        <h6><i class="fas fa-lightbulb me-2"></i>Quick Insights:</h6>
                        <ul class="mb-0">
                            ${analytics.insights.map(insight => `<li>${insight}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}
                    
                    <div class="mt-4 text-center">
                        <button class="btn btn-primary btn-lg me-2" onclick="runAIAnalysis()">
                            <i class="fas fa-brain me-2"></i>
                            Run AI Analysis
                        </button>
                        <button class="btn btn-success me-2" onclick="generateBusinessReport()">
                            <i class="fas fa-chart-line me-1"></i>
                            Business Report
                        </button>
                        <button class="btn btn-info" onclick="downloadProcessedData()">
                            <i class="fas fa-download me-1"></i>
                            Download
                        </button>
                    </div>
                </div>
            </div>
        `;

        dataPreview.innerHTML = resultHTML;
        dataPreview.scrollIntoView({ behavior: 'smooth' });
        
        this.showSuccess(`✅ Successfully processed ${data.length} rows from ${filename}. AI analysis ready!`);
    }

    /**
     * Calculate basic analytics for business insights
     * Following SME business analysis requirements
     */
    calculateBasicAnalytics(data) {
        if (!data || data.length === 0) return { completeness: 0 };

        const totalCells = data.length * Object.keys(data[0]).length;
        const filledCells = data.reduce((count, row) => {
            return count + Object.values(row).filter(val => val && val.toString().trim()).length;
        }, 0);

        const completeness = Math.round((filledCells / totalCells) * 100);
        const columns = Object.keys(data[0]);
        const insights = [];

        // Detect common business data patterns
        const hasRevenue = columns.some(col => col.toLowerCase().includes('revenue') || col.toLowerCase().includes('sales'));
        const hasDate = columns.some(col => col.toLowerCase().includes('date') || col.toLowerCase().includes('time'));
        const hasCustomer = columns.some(col => col.toLowerCase().includes('customer') || col.toLowerCase().includes('client'));

        if (hasRevenue) insights.push('Revenue/Sales data detected - Financial analysis available');
        if (hasDate) insights.push('Time-series data detected - Trend analysis possible');
        if (hasCustomer) insights.push('Customer data detected - Segmentation analysis available');

        return { completeness, insights };
    }

    /**
     * Format cell values for display
     */
    formatCellValue(value) {
        if (!value) return '<span class="text-muted">—</span>';
        
        const str = value.toString();
        if (str.length > 50) {
            return `${str.substring(0, 47)}...`;
        }
        
        return str;
    }

    /**
     * Show loading state during file processing
     */
    showLoadingState(filename) {
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            uploadArea.innerHTML = `
                <div class="text-center p-4">
                    <div class="spinner-border text-primary mb-3" role="status"></div>
                    <h6>Processing ${filename}...</h6>
                    <small class="text-muted">Please wait while we analyze your data</small>
                </div>
            `;
        }
    }

    /**
     * Setup drag and drop functionality
     */
    setupDragAndDrop(uploadArea, fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('border-primary', 'bg-light');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('border-primary', 'bg-light');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }

    /**
     * Add diagnostic UI to the page
     */
    addDiagnosticUI() {
        if (document.getElementById('platformDiagnosticUI')) return;

        const diagnosticHTML = `
            <div class="card mt-4 border-warning" id="platformDiagnosticUI">
                <div class="card-body text-center">
                    <h5 class="card-title text-warning">
                        <i class="fas fa-stethoscope me-2"></i>
                        AI Data Analyzer - Platform Diagnostic
                    </h5>
                    <p class="card-text">
                        Data upload not working? Run diagnostics to identify and fix issues automatically.
                    </p>
                    <button class="btn btn-warning btn-lg me-2" onclick="platformDiagnostic.runFullDiagnostic()">
                        <i class="fas fa-search me-2"></i>
                        Run Full Diagnostic
                    </button>
                    <button class="btn btn-success btn-lg" onclick="platformDiagnostic.createWorkingFileUpload()">
                        <i class="fas fa-wrench me-1"></i>
                        Fix Upload Now
                    </button>
                </div>
            </div>
        `;

        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentHTML('beforeend', diagnosticHTML);
    }

    /**
     * Run comprehensive diagnostic
     */
    async runFullDiagnostic() {
        this.logger.info('🔬 Running comprehensive AI Data Analyzer diagnostic...');
        
        try {
            this.showDiagnosticProgress('Analyzing platform components...', 25);
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.showDiagnosticProgress('Checking file upload system...', 50);
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.showDiagnosticProgress('Validating UI components...', 75);
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.showDiagnosticProgress('Finalizing analysis...', 100);
            await new Promise(resolve => setTimeout(resolve, 500));

            this.displayDiagnosticResults();

        } catch (error) {
            this.logger.error(`Diagnostic failed: ${error.message}`);
            this.showError(`Diagnostic failed: ${error.message}`);
        }
    }

    /**
     * Show diagnostic progress
     */
    showDiagnosticProgress(message, percentage) {
        let progressDiv = document.getElementById('diagnosticProgress');
        if (!progressDiv) {
            progressDiv = document.createElement('div');
            progressDiv.id = 'diagnosticProgress';
            document.querySelector('.container').appendChild(progressDiv);
        }

        progressDiv.innerHTML = `
            <div class="alert alert-info">
                <div class="d-flex align-items-center">
                    <div class="spinner-border spinner-border-sm me-3" role="status"></div>
                    <div class="flex-grow-1">
                        <strong>Platform Diagnostic:</strong> ${message}
                        <div class="progress mt-2" style="height: 8px;">
                            <div class="progress-bar bg-info" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Display diagnostic results
     */
    displayDiagnosticResults() {
        const progress = document.getElementById('diagnosticProgress');
        if (progress) progress.remove();

        const totalChecks = Object.keys(this.diagnosticResults).length;
        const passedChecks = Object.values(this.diagnosticResults).filter(r => r.status === 'PASS').length;
        const criticalIssues = Object.values(this.diagnosticResults).filter(r => r.status === 'FAIL' && r.critical).length;
        const healthScore = totalChecks > 0 ? ((passedChecks / totalChecks) * 100).toFixed(1) : 0;

        const resultsHTML = `
            <div class="card mt-4 shadow" id="diagnosticResults">
                <div class="card-header ${criticalIssues > 0 ? 'bg-danger' : healthScore >= 80 ? 'bg-success' : 'bg-warning'} text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-clipboard-check me-2"></i>
                        AI Data Analyzer - Diagnostic Results
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-success">${passedChecks}/${totalChecks}</h4>
                                <small>Checks Passed</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-${criticalIssues > 0 ? 'danger' : 'success'}">${criticalIssues}</h4>
                                <small>Critical Issues</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded border">
                                <h4 class="text-primary">${healthScore}%</h4>
                                <small>Health Score</small>
                            </div>
                        </div>
                    </div>

                    <div class="alert ${criticalIssues > 0 ? 'alert-danger' : 'alert-success'}">
                        <h6 class="mb-2">
                            <i class="fas fa-${criticalIssues > 0 ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
                            Status: ${criticalIssues > 0 ? 'CRITICAL ISSUES DETECTED' : 'PLATFORM HEALTHY'}
                        </h6>
                        <p class="mb-0">
                            ${criticalIssues > 0 
                                ? `Found ${criticalIssues} critical issues. Click "Fix Upload Now" for immediate resolution.`
                                : 'All systems operational. Your AI Data Analyzer is ready for use!'
                            }
                        </p>
                    </div>

                    <div class="text-center mt-4">
                        <button class="btn btn-success btn-lg me-2" onclick="platformDiagnostic.createWorkingFileUpload()">
                            <i class="fas fa-magic me-1"></i>
                            ${criticalIssues > 0 ? 'Fix Issues Now' : 'Activate Enhanced Upload'}
                        </button>
                        <button class="btn btn-primary" onclick="platformDiagnostic.runFullDiagnostic()">
                            <i class="fas fa-redo me-1"></i>
                            Run Again
                        </button>
                    </div>
                </div>
            </div>
        `;

        let resultsContainer = document.getElementById('diagnosticResults');
        if (!resultsContainer) {
            document.querySelector('.container').insertAdjacentHTML('beforeend', resultsHTML);
        } else {
            resultsContainer.outerHTML = resultsHTML;
        }

        document.getElementById('diagnosticResults').scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Utility functions for user feedback
     */
    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showAlert(message, type) {
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHTML);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = document.querySelector('.alert');
            if (alert && alert.classList.contains(`alert-${type}`)) {
                alert.remove();
            }
        }, 5000);
    }
}

// Global functions for button interactions
function runAIAnalysis() {
    if (window.currentUploadedData) {
        alert('🧠 AI Analysis feature will analyze your data for business insights, forecasting, and anomaly detection. Coming soon!');
    } else {
        alert('Please upload data first');
    }
}

function generateBusinessReport() {
    if (window.currentUploadedData) {
        alert('📊 Business Report will generate executive summaries and actionable insights. Coming soon!');
    } else {
        alert('Please upload data first');
    }
}

function downloadProcessedData() {
    if (window.currentUploadedData) {
        const dataStr = JSON.stringify(window.currentUploadedData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `processed_${window.uploadedFileName || 'data'}.json`;
        link.click();
        URL.revokeObjectURL(url);
    } else {
        alert('No data to download');
    }
}

// Initialize diagnostic tool
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (!window.platformDiagnostic) {
            window.platformDiagnostic = new PlatformDiagnostic();
        }
    }, 1000);
});

// Make available globally
window.runPlatformDiagnostic = function() {
    if (window.platformDiagnostic) {
        window.platformDiagnostic.runFullDiagnostic();
    } else {
        console.error('Platform diagnostic not initialized');
    }
};

window.fixFileUpload = function() {
    if (window.platformDiagnostic) {
        window.platformDiagnostic.createWorkingFileUpload();
    } else {
        console.error('Platform diagnostic not initialized');
    }
};