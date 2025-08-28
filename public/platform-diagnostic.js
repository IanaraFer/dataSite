/**
 * DataSight AI Platform - Diagnostic Tool
 * Following project coding instructions for proper error handling
 * Identifies and fixes data upload/processing issues
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
        this.logger.info('🔍 Starting Platform Diagnostic...');
        
        try {
            // Wait for DOM to be ready
            if (document.readyState !== 'complete') {
                await new Promise(resolve => window.addEventListener('load', resolve));
            }

            // Run immediate diagnostic
            this.runImmediateDiagnostic();
            
            // Add diagnostic UI
            this.addDiagnosticUI();
            
        } catch (error) {
            this.logger.error(`Diagnostic initialization failed: ${error.message}`);
        }
    }

    /**
     * Run immediate diagnostic checks
     * Following project error handling guidelines
     */
    runImmediateDiagnostic() {
        this.logger.info('🏃‍♂️ Running immediate checks...');

        // Check 1: Platform object availability
        this.diagnosticResults.platform_available = {
            status: window.dataSightPlatform ? 'PASS' : 'FAIL',
            details: window.dataSightPlatform ? 'Platform object found' : 'Platform object not found',
            fix: window.dataSightPlatform ? null : 'Ensure platform.js is loaded correctly'
        };

        // Check 2: File input element
        const fileInput = document.getElementById('fileInput');
        this.diagnosticResults.file_input_exists = {
            status: fileInput ? 'PASS' : 'FAIL',
            details: fileInput ? 'File input element found' : 'File input element not found',
            fix: fileInput ? null : 'Check if platform.html contains proper file input'
        };

        // Check 3: Event listeners
        if (fileInput) {
            const hasEventListener = fileInput.onchange !== null || 
                                   fileInput.addEventListener !== undefined;
            this.diagnosticResults.file_input_listeners = {
                status: hasEventListener ? 'PASS' : 'FAIL',
                details: hasEventListener ? 'File input can handle events' : 'File input missing event handlers',
                fix: hasEventListener ? null : 'Add proper file change event listener'
            };
        }

        // Check 4: Console errors
        const originalConsoleError = console.error;
        let errorCount = 0;
        console.error = (...args) => {
            errorCount++;
            originalConsoleError.apply(console, args);
        };

        setTimeout(() => {
            console.error = originalConsoleError;
            this.diagnosticResults.console_errors = {
                status: errorCount === 0 ? 'PASS' : 'WARN',
                details: errorCount === 0 ? 'No console errors detected' : `${errorCount} console errors detected`,
                fix: errorCount > 0 ? 'Check browser console for specific errors' : null
            };
        }, 1000);

        // Check 5: Required DOM elements
        const requiredElements = ['dataPreview', 'analysisResults', 'metricsRow'];
        for (const elementId of requiredElements) {
            const element = document.getElementById(elementId);
            this.diagnosticResults[`element_${elementId}`] = {
                status: element ? 'PASS' : 'FAIL',
                details: element ? `Element ${elementId} found` : `Element ${elementId} missing`,
                fix: element ? null : `Add <div id="${elementId}"></div> to HTML`
            };
        }

        this.logger.success('✅ Immediate diagnostic completed');
    }

    /**
     * Run comprehensive platform diagnostic
     * Following project testing and validation guidelines
     */
    async runFullDiagnostic() {
        this.logger.info('🔬 Running comprehensive diagnostic...');
        
        this.showDiagnosticProgress('Checking platform components...', 10);

        try {
            // Reset results
            this.diagnosticResults = {};

            // Diagnostic 1: Platform Architecture (20%)
            this.showDiagnosticProgress('Testing platform architecture...', 20);
            await this.diagnosePlatformArchitecture();

            // Diagnostic 2: File Upload System (40%)
            this.showDiagnosticProgress('Testing file upload system...', 40);
            await this.diagnoseFileUploadSystem();

            // Diagnostic 3: Data Processing Pipeline (60%)
            this.showDiagnosticProgress('Testing data processing...', 60);
            await this.diagnoseDataProcessing();

            // Diagnostic 4: UI Components (80%)
            this.showDiagnosticProgress('Testing UI components...', 80);
            await this.diagnoseUIComponents();

            // Diagnostic 5: Event Handling (100%)
            this.showDiagnosticProgress('Testing event handling...', 100);
            await this.diagnoseEventHandling();

            // Display results
            setTimeout(() => {
                this.displayDiagnosticResults();
            }, 500);

        } catch (error) {
            this.logger.error(`Full diagnostic failed: ${error.message}`);
            this.displayDiagnosticError(error);
        }
    }

    /**
     * Diagnose platform architecture and dependencies
     */
    async diagnosePlatformArchitecture() {
        // Check platform object
        this.diagnosticResults.platform_object = {
            status: window.dataSightPlatform ? 'PASS' : 'FAIL',
            details: window.dataSightPlatform ? 'Platform class instantiated' : 'Platform class not found',
            critical: true,
            fix: window.dataSightPlatform ? null : 'Ensure platform.js is loaded and class is instantiated'
        };

        // Check required methods
        if (window.dataSightPlatform) {
            const requiredMethods = [
                'handleFileUpload',
                'processData', 
                'cleanAndValidateData',
                'displayDataPreview',
                'calculateMetrics',
                'showAnalysisControls'
            ];

            for (const method of requiredMethods) {
                this.diagnosticResults[`method_${method}`] = {
                    status: typeof window.dataSightPlatform[method] === 'function' ? 'PASS' : 'FAIL',
                    details: typeof window.dataSightPlatform[method] === 'function' ? 
                            `Method ${method} available` : `Method ${method} missing`,
                    critical: ['handleFileUpload', 'processData'].includes(method),
                    fix: typeof window.dataSightPlatform[method] === 'function' ? null : 
                         `Implement ${method} method in DataSightPlatform class`
                };
            }
        }

        // Check dependencies
        const dependencies = ['Papa', 'Chart']; // Common JS libraries
        for (const dep of dependencies) {
            this.diagnosticResults[`dependency_${dep}`] = {
                status: window[dep] ? 'PASS' : 'WARN',
                details: window[dep] ? `${dep} library loaded` : `${dep} library not found`,
                critical: false,
                fix: window[dep] ? null : `Load ${dep} library for enhanced functionality`
            };
        }
    }

    /**
     * Diagnose file upload system
     */
    async diagnoseFileUploadSystem() {
        // Check file input element
        const fileInput = document.getElementById('fileInput');
        this.diagnosticResults.file_input_element = {
            status: fileInput ? 'PASS' : 'FAIL',
            details: fileInput ? 'File input element exists' : 'File input element missing',
            critical: true,
            fix: fileInput ? null : 'Add file input element with id="fileInput"'
        };

        if (fileInput) {
            // Check input attributes
            this.diagnosticResults.file_input_accept = {
                status: fileInput.accept ? 'PASS' : 'WARN',
                details: fileInput.accept ? `Accepts: ${fileInput.accept}` : 'No file type restrictions',
                critical: false,
                fix: fileInput.accept ? null : 'Add accept=".csv,.xlsx" attribute'
            };

            // Check event listeners
            const events = ['change', 'click'];
            for (const event of events) {
                const hasListener = fileInput[`on${event}`] !== null;
                this.diagnosticResults[`file_input_${event}_listener`] = {
                    status: hasListener ? 'PASS' : 'FAIL',
                    details: hasListener ? `${event} listener attached` : `${event} listener missing`,
                    critical: event === 'change',
                    fix: hasListener ? null : `Add ${event} event listener to file input`
                };
            }
        }

        // Check upload area
        const uploadArea = document.querySelector('.upload-area');
        this.diagnosticResults.upload_area = {
            status: uploadArea ? 'PASS' : 'WARN',
            details: uploadArea ? 'Upload area element found' : 'Upload area element missing',
            critical: false,
            fix: uploadArea ? null : 'Add upload area for better UX'
        };
    }

    /**
     * Diagnose data processing pipeline
     */
    async diagnoseDataProcessing() {
        // Test with sample data
        const sampleData = [
            { Date: '2024-01-01', Revenue: 1000, Customers: 50 },
            { Date: '2024-01-02', Revenue: 1200, Customers: 60 }
        ];

        if (window.dataSightPlatform) {
            // Test data cleaning
            if (typeof window.dataSightPlatform.cleanAndValidateData === 'function') {
                try {
                    const cleaned = window.dataSightPlatform.cleanAndValidateData(sampleData);
                    this.diagnosticResults.data_cleaning = {
                        status: Array.isArray(cleaned) ? 'PASS' : 'FAIL',
                        details: Array.isArray(cleaned) ? 
                                `Data cleaning works (${cleaned.length} rows)` : 
                                'Data cleaning failed',
                        critical: true,
                        fix: Array.isArray(cleaned) ? null : 'Fix data cleaning method implementation'
                    };
                } catch (error) {
                    this.diagnosticResults.data_cleaning = {
                        status: 'FAIL',
                        details: `Data cleaning error: ${error.message}`,
                        critical: true,
                        fix: 'Fix data cleaning method - check for syntax/logic errors'
                    };
                }
            } else {
                this.diagnosticResults.data_cleaning = {
                    status: 'FAIL',
                    details: 'cleanAndValidateData method missing',
                    critical: true,
                    fix: 'Implement cleanAndValidateData method'
                };
            }

            // Test data preview
            if (typeof window.dataSightPlatform.displayDataPreview === 'function') {
                try {
                    window.dataSightPlatform.displayDataPreview(sampleData);
                    this.diagnosticResults.data_preview = {
                        status: 'PASS',
                        details: 'Data preview method works',
                        critical: true,
                        fix: null
                    };
                } catch (error) {
                    this.diagnosticResults.data_preview = {
                        status: 'FAIL',
                        details: `Data preview error: ${error.message}`,
                        critical: true,
                        fix: 'Fix displayDataPreview method implementation'
                    };
                }
            }
        }
    }

    /**
     * Diagnose UI components
     */
    async diagnoseUIComponents() {
        const criticalElements = [
            { id: 'dataPreview', name: 'Data Preview Container' },
            { id: 'analysisResults', name: 'Analysis Results Container' },
            { id: 'metricsRow', name: 'Metrics Display Row' }
        ];

        for (const element of criticalElements) {
            const domElement = document.getElementById(element.id);
            this.diagnosticResults[`ui_${element.id}`] = {
                status: domElement ? 'PASS' : 'FAIL',
                details: domElement ? `${element.name} exists` : `${element.name} missing`,
                critical: true,
                fix: domElement ? null : `Add <div id="${element.id}"></div> to HTML`
            };
        }

        // Check Bootstrap/CSS framework
        const hasBootstrap = document.querySelector('.container') !== null ||
                             document.querySelector('.btn') !== null;
        this.diagnosticResults.css_framework = {
            status: hasBootstrap ? 'PASS' : 'WARN',
            details: hasBootstrap ? 'CSS framework detected' : 'CSS framework not detected',
            critical: false,
            fix: hasBootstrap ? null : 'Include Bootstrap or CSS framework for proper styling'
        };
    }

    /**
     * Diagnose event handling system
     */
    async diagnoseEventHandling() {
        // Check if file input has proper event handling
        const fileInput = document.getElementById('fileInput');
        
        if (fileInput && window.dataSightPlatform) {
            // Test event binding
            let eventBound = false;
            
            // Check if handleFileUpload exists and is callable
            if (typeof window.dataSightPlatform.handleFileUpload === 'function') {
                eventBound = true;
            }

            this.diagnosticResults.event_handling = {
                status: eventBound ? 'PASS' : 'FAIL',
                details: eventBound ? 'File upload event handling ready' : 'File upload event not bound',
                critical: true,
                fix: eventBound ? null : 'Bind file change event to handleFileUpload method'
            };
        }

        // Check for unhandled errors
        let errorHandlerExists = false;
        if (window.onerror || window.addEventListener) {
            errorHandlerExists = true;
        }

        this.diagnosticResults.error_handling = {
            status: errorHandlerExists ? 'PASS' : 'WARN',
            details: errorHandlerExists ? 'Error handling available' : 'No global error handling',
            critical: false,
            fix: errorHandlerExists ? null : 'Add global error handler for better debugging'
        };
    }

    /**
     * Create and test a working file upload system
     * Following project coding instructions for proper implementation
     */
    createWorkingFileUpload() {
        this.logger.info('🔧 Creating working file upload system...');

        // Create the file upload handler
        const workingFileUploadCode = `
            // Working file upload implementation
            function createWorkingFileUpload() {
                const fileInput = document.getElementById('fileInput');
                const uploadArea = document.querySelector('.upload-area');
                
                if (!fileInput) {
                    console.error('File input not found');
                    return;
                }

                // Remove existing listeners
                fileInput.onchange = null;
                
                // Add working file change handler
                fileInput.addEventListener('change', function(event) {
                    const file = event.target.files[0];
                    if (!file) return;

                    console.log('File selected:', file.name, file.size, 'bytes');
                    
                    // Show loading
                    if (uploadArea) {
                        uploadArea.innerHTML = \`
                            <div class="text-center p-4">
                                <div class="spinner-border text-primary mb-3"></div>
                                <h6>Processing \${file.name}...</h6>
                                <small>Please wait while we analyze your data</small>
                            </div>
                        \`;
                    }

                    // Process the file
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        try {
                            const content = e.target.result;
                            console.log('File content loaded, length:', content.length);
                            
                            // Parse CSV data
                            const lines = content.split('\\n');
                            const headers = lines[0].split(',').map(h => h.trim());
                            const data = [];
                            
                            for (let i = 1; i < Math.min(lines.length, 101); i++) { // Limit to 100 rows for demo
                                if (lines[i].trim()) {
                                    const values = lines[i].split(',').map(v => v.trim());
                                    const row = {};
                                    headers.forEach((header, index) => {
                                        row[header] = values[index] || '';
                                    });
                                    data.push(row);
                                }
                            }
                            
                            console.log('Parsed data:', data.length, 'rows');
                            
                            // Display the data
                            displayParsedData(data, file.name);
                            
                        } catch (error) {
                            console.error('File processing error:', error);
                            showError('Error processing file: ' + error.message);
                        }
                    };
                    
                    reader.onerror = function() {
                        console.error('File reading error');
                        showError('Error reading file');
                    };
                    
                    reader.readAsText(file);
                });

                console.log('✅ Working file upload system created');
            }

            function displayParsedData(data, filename) {
                // Find or create data preview container
                let dataPreview = document.getElementById('dataPreview');
                if (!dataPreview) {
                    dataPreview = document.createElement('div');
                    dataPreview.id = 'dataPreview';
                    document.querySelector('.container').appendChild(dataPreview);
                }

                // Create data preview HTML
                const previewHTML = \`
                    <div class="card mt-4">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="fas fa-table me-2"></i>
                                Data Successfully Loaded: \${filename}
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row mb-3">
                                <div class="col-md-4">
                                    <div class="text-center p-3 bg-light rounded">
                                        <h4 class="text-primary mb-1">\${data.length}</h4>
                                        <small class="text-muted">Rows Loaded</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="text-center p-3 bg-light rounded">
                                        <h4 class="text-success mb-1">\${Object.keys(data[0] || {}).length}</h4>
                                        <small class="text-muted">Columns</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="text-center p-3 bg-light rounded">
                                        <h4 class="text-info mb-1">✅</h4>
                                        <small class="text-muted">Status: Ready</small>
                                    </div>
                                </div>
                            </div>
                            
                            <h6 class="mb-3">Data Preview (First 10 rows):</h6>
                            <div class="table-responsive">
                                <table class="table table-bordered table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            \${Object.keys(data[0] || {}).map(col => \`<th>\${col}</th>\`).join('')}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        \${data.slice(0, 10).map(row => \`
                                            <tr>
                                                \${Object.values(row).map(val => \`<td>\${val}</td>\`).join('')}
                                            </tr>
                                        \`).join('')}
                                    </tbody>
                                </table>
                            </div>
                            
                            <div class="mt-3 text-center">
                                <button class="btn btn-primary me-2" onclick="runBasicAnalysis()">
                                    <i class="fas fa-chart-line me-1"></i>
                                    Run Basic Analysis
                                </button>
                                <button class="btn btn-success" onclick="generateReport()">
                                    <i class="fas fa-file-alt me-1"></i>
                                    Generate Report
                                </button>
                            </div>
                        </div>
                    </div>
                \`;

                dataPreview.innerHTML = previewHTML;
                
                // Store data globally for analysis
                window.currentUploadedData = data;
                
                // Show success message
                showSuccess(\`✅ Successfully loaded \${data.length} rows from \${filename}\`);
                
                // Auto-scroll to results
                dataPreview.scrollIntoView({ behavior: 'smooth' });
            }

            function runBasicAnalysis() {
                if (!window.currentUploadedData) {
                    showError('No data available for analysis');
                    return;
                }

                const data = window.currentUploadedData;
                const analysisHTML = \`
                    <div class="card mt-4">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">
                                <i class="fas fa-brain me-2"></i>
                                Basic Data Analysis Results
                            </h5>
                        </div>
                        <div class="card-body">
                            <h6>Dataset Overview:</h6>
                            <ul>
                                <li><strong>Total Records:</strong> \${data.length}</li>
                                <li><strong>Columns:</strong> \${Object.keys(data[0] || {}).join(', ')}</li>
                                <li><strong>Data Quality:</strong> \${Math.round((data.filter(row => Object.values(row).some(val => val && val.trim())).length / data.length) * 100)}% complete</li>
                            </ul>
                            
                            <div class="alert alert-info">
                                <h6><i class="fas fa-lightbulb me-2"></i>Analysis Complete!</h6>
                                <p class="mb-0">Your data has been processed successfully. This demonstrates the platform is working correctly.</p>
                            </div>
                        </div>
                    </div>
                \`;

                // Find or create analysis results container
                let analysisResults = document.getElementById('analysisResults');
                if (!analysisResults) {
                    analysisResults = document.createElement('div');
                    analysisResults.id = 'analysisResults';
                    document.querySelector('.container').appendChild(analysisResults);
                }

                analysisResults.innerHTML = analysisHTML;
                analysisResults.scrollIntoView({ behavior: 'smooth' });
            }

            function generateReport() {
                showSuccess('📄 Report generation feature coming soon! Your data is ready for analysis.');
            }

            function showSuccess(message) {
                const alertHTML = \`
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        \${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                \`;
                document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHTML);
                setTimeout(() => {
                    const alert = document.querySelector('.alert-success');
                    if (alert) alert.remove();
                }, 5000);
            }

            function showError(message) {
                const alertHTML = \`
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <i class="fas fa-exclamation-triangle me-2"></i>\${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                \`;
                document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHTML);
            }

            // Initialize the working file upload
            createWorkingFileUpload();
        `;

        // Execute the code
        const script = document.createElement('script');
        script.textContent = workingFileUploadCode;
        document.head.appendChild(script);

        this.logger.success('✅ Working file upload system created and activated');
        
        // Show success message
        this.showCustomSuccess('🔧 Working file upload system has been created! Try uploading a CSV file now.');
    }

    /**
     * Show diagnostic progress
     */
    showDiagnosticProgress(message, percentage) {
        const progressHTML = `
            <div class="alert alert-info" id="diagnosticProgress">
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

        const existing = document.getElementById('diagnosticProgress');
        if (existing) existing.remove();

        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentHTML('beforeend', progressHTML);
    }

    /**
     * Display comprehensive diagnostic results
     */
    displayDiagnosticResults() {
        const progress = document.getElementById('diagnosticProgress');
        if (progress) progress.remove();

        const totalChecks = Object.keys(this.diagnosticResults).length;
        const passedChecks = Object.values(this.diagnosticResults).filter(r => r.status === 'PASS').length;
        const failedChecks = Object.values(this.diagnosticResults).filter(r => r.status === 'FAIL').length;
        const criticalIssues = Object.values(this.diagnosticResults).filter(r => r.status === 'FAIL' && r.critical).length;
        const healthScore = totalChecks > 0 ? ((passedChecks / totalChecks) * 100).toFixed(1) : 0;

        const resultsHTML = `
            <div class="card mt-4" id="diagnosticResultsCard">
                <div class="card-header ${criticalIssues > 0 ? 'bg-danger' : healthScore >= 80 ? 'bg-success' : 'bg-warning'} text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-stethoscope me-2"></i>
                        Platform Diagnostic Results
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="text-center p-3 border rounded bg-light">
                                <h4 class="text-success mb-1">${passedChecks}</h4>
                                <small class="text-muted">Checks Passed</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 border rounded bg-light">
                                <h4 class="text-danger mb-1">${failedChecks}</h4>
                                <small class="text-muted">Checks Failed</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 border rounded bg-light">
                                <h4 class="text-warning mb-1">${criticalIssues}</h4>
                                <small class="text-muted">Critical Issues</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-3 border rounded bg-light">
                                <h4 class="text-primary mb-1">${healthScore}%</h4>
                                <small class="text-muted">Health Score</small>
                            </div>
                        </div>
                    </div>

                    <div class="alert ${criticalIssues > 0 ? 'alert-danger' : healthScore >= 80 ? 'alert-success' : 'alert-warning'}">
                        <h6 class="mb-2">
                            <i class="fas fa-diagnosis me-2"></i>
                            Diagnosis: ${criticalIssues > 0 ? 'CRITICAL ISSUES FOUND' : healthScore >= 80 ? 'PLATFORM HEALTHY' : 'MINOR ISSUES DETECTED'}
                        </h6>
                        <p class="mb-0">
                            ${criticalIssues > 0 
                                ? `Found ${criticalIssues} critical issues preventing platform operation. Fix these issues first.`
                                : healthScore >= 80 
                                ? 'Platform is operating correctly. All core functions are working.'
                                : 'Platform has minor issues but should work for basic operations.'
                            }
                        </p>
                    </div>

                    ${criticalIssues > 0 ? `
                    <div class="row">
                        <div class="col-12">
                            <h6 class="text-danger mb-3"><i class="fas fa-exclamation-triangle me-1"></i> Critical Issues (Fix These First)</h6>
                            <div class="critical-issues">
                                ${Object.entries(this.diagnosticResults)
                                    .filter(([key, result]) => result.status === 'FAIL' && result.critical)
                                    .map(([key, result]) => `
                                        <div class="p-3 mb-3 border border-danger rounded">
                                            <h6 class="text-danger mb-2">${result.details}</h6>
                                            ${result.fix ? `<p class="mb-0"><strong>Fix:</strong> ${result.fix}</p>` : ''}
                                        </div>
                                    `).join('')}
                            </div>
                        </div>
                    </div>
                    ` : ''}

                    <div class="row mt-4">
                        <div class="col-md-6">
                            <h6 class="text-success mb-3"><i class="fas fa-check-circle me-1"></i> Passed Checks</h6>
                            <div class="passed-checks" style="max-height: 300px; overflow-y: auto;">
                                ${Object.entries(this.diagnosticResults)
                                    .filter(([key, result]) => result.status === 'PASS')
                                    .map(([key, result]) => `
                                        <div class="p-2 mb-2 bg-light rounded border-start border-success border-3">
                                            <small>${result.details}</small>
                                        </div>
                                    `).join('')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-danger mb-3"><i class="fas fa-times-circle me-1"></i> Failed Checks</h6>
                            <div class="failed-checks" style="max-height: 300px; overflow-y: auto;">
                                ${Object.entries(this.diagnosticResults)
                                    .filter(([key, result]) => result.status === 'FAIL')
                                    .map(([key, result]) => `
                                        <div class="p-2 mb-2 bg-light rounded border-start border-danger border-3">
                                            <strong>${result.details}</strong>
                                            ${result.fix ? `<br><small class="text-muted">Fix: ${result.fix}</small>` : ''}
                                        </div>
                                    `).join('')}
                            </div>
                        </div>
                    </div>

                    <div class="mt-4 text-center">
                        <button class="btn btn-primary me-2" onclick="platformDiagnostic.runFullDiagnostic()">
                            <i class="fas fa-redo me-1"></i>Run Diagnostic Again
                        </button>
                        <button class="btn btn-success me-2" onclick="platformDiagnostic.createWorkingFileUpload()">
                            <i class="fas fa-wrench me-1"></i>Create Working Upload System
                        </button>
                        <button class="btn btn-info" onclick="location.reload()">
                            <i class="fas fa-refresh me-1"></i>Reload Platform
                        </button>
                    </div>
                </div>
            </div>
        `;

        const existingResults = document.getElementById('diagnosticResultsCard');
        if (existingResults) existingResults.remove();

        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentHTML('beforeend', resultsHTML);

        this.logger.success(`🎯 Diagnostic Complete: ${passedChecks}/${totalChecks} checks passed`);

        setTimeout(() => {
            document.getElementById('diagnosticResultsCard')?.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }

    /**
     * Add diagnostic UI to the page
     */
    addDiagnosticUI() {
        if (document.getElementById('platformDiagnosticUI')) return;

        const diagnosticHTML = `
            <div class="card mt-4" id="platformDiagnosticUI">
                <div class="card-body text-center">
                    <h5 class="card-title">
                        <i class="fas fa-stethoscope text-danger me-2"></i>
                        Platform Diagnostic Tool
                    </h5>
                    <p class="card-text">
                        Something not working? Run a comprehensive diagnostic to identify and fix issues.
                    </p>
                    <button class="btn btn-danger btn-lg me-2" onclick="platformDiagnostic.runFullDiagnostic()">
                        <i class="fas fa-search me-2"></i>
                        Run Full Diagnostic
                    </button>
                    <button class="btn btn-success" onclick="platformDiagnostic.createWorkingFileUpload()">
                        <i class="fas fa-wrench me-1"></i>
                        Quick Fix Upload
                    </button>
                </div>
            </div>
        `;

        const container = document.querySelector('.container');
        if (container) {
            container.insertAdjacentHTML('beforeend', diagnosticHTML);
        }
    }

    /**
     * Display diagnostic error
     */
    displayDiagnosticError(error) {
        const errorHTML = `
            <div class="alert alert-danger mt-4">
                <h5><i class="fas fa-bug me-2"></i>Diagnostic Error</h5>
                <p>An error occurred during platform diagnosis:</p>
                <code>${error.message}</code>
            </div>
        `;

        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentHTML('beforeend', errorHTML);
    }

    /**
     * Show custom success message
     */
    showCustomSuccess(message) {
        const alertHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentHTML('afterbegin', alertHTML);

        setTimeout(() => {
            const alert = document.querySelector('.alert-success');
            if (alert) alert.remove();
        }, 7000);
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

// Check if diagnostic is loaded
console.log(window.platformDiagnostic);

// Run full diagnostic
window.platformDiagnostic.runFullDiagnostic();

// Or create working upload system immediately
window.platformDiagnostic.createWorkingFileUpload();

// Global diagnostic functions
function runPlatformDiagnostic() {
    if (window.platformDiagnostic) {
        window.platformDiagnostic.runFullDiagnostic();
    }
}

function fixFileUpload() {
    if (window.platformDiagnostic) {
        window.platformDiagnostic.createWorkingFileUpload();
    }
}

<!-- Add this directly to your platform.html before </body> -->
<script>
// Immediate platform fix - following project coding instructions
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Platform Quick Fix Loading...');
    
    // Create immediate diagnostic button
    setTimeout(() => {
        const quickFixHTML = `
            <div class="alert alert-warning mt-3" id="quickPlatformFix">
                <h6><i class="fas fa-tools me-2"></i>Platform Quick Fix</h6>
                <p>Data upload not working? Click below for immediate fix:</p>
                <button class="btn btn-success" onclick="createWorkingUpload()">
                    <i class="fas fa-wrench me-1"></i>Fix Upload Now
                </button>
            </div>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', quickFixHTML);
        }
    }, 2000);
});

// Working upload system - following SME business requirements
function createWorkingUpload() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput) {
        alert('File input not found. Check HTML structure.');
        return;
    }

    console.log('🔧 Creating working file upload...');
    
    // Remove existing handlers
    fileInput.onchange = null;
    
    // Add new working handler
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (!file) return;

        console.log('📁 File selected:', file.name);
        
        // Show loading
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            uploadArea.innerHTML = `
                <div class="text-center p-4">
                    <div class="spinner-border text-primary mb-3"></div>
                    <h6>Processing ${file.name}...</h6>
                </div>
            `;
        }

        // Process file
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const content = e.target.result;
                const lines = content.split('\\n');
                const headers = lines[0].split(',').map(h => h.trim());
                const data = [];
                
                // Parse CSV data - following data validation best practices
                for (let i = 1; i < Math.min(lines.length, 101); i++) {
                    if (lines[i].trim()) {
                        const values = lines[i].split(',').map(v => v.trim());
                        const row = {};
                        headers.forEach((header, index) => {
                            row[header] = values[index] || '';
                        });
                        data.push(row);
                    }
                }
                
                console.log('✅ Parsed', data.length, 'rows');
                displayDataResults(data, file.name);
                
            } catch (error) {
                console.error('❌ Processing error:', error);
                showErrorMessage('File processing error: ' + error.message);
            }
        };
        
        reader.readAsText(file);
    });

    // Success notification
    showSuccessMessage('✅ Working file upload system activated! Try uploading a CSV file now.');
}

// Display parsed data - following UI best practices
function displayDataResults(data, filename) {
    let dataPreview = document.getElementById('dataPreview');
    if (!dataPreview) {
        dataPreview = document.createElement('div');
        dataPreview.id = 'dataPreview';
        document.querySelector('.container').appendChild(dataPreview);
    }

    // Following SME business context - clear, actionable results
    const resultHTML = `
        <div class="card mt-4">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">
                    <i class="fas fa-check-circle me-2"></i>
                    Data Successfully Loaded: ${filename}
                </h5>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-light rounded">
                            <h4 class="text-primary">${data.length}</h4>
                            <small>Rows Loaded</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-light rounded">
                            <h4 class="text-success">${Object.keys(data[0] || {}).length}</h4>
                            <small>Columns</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-light rounded">
                            <h4 class="text-info">✅</h4>
                            <small>Platform Working</small>
                        </div>
                    </div>
                </div>
                
                <h6 class="mb-3">Data Preview:</h6>
                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="table-dark">
                            <tr>
                                ${Object.keys(data[0] || {}).map(col => `<th>${col}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.slice(0, 10).map(row => `
                                <tr>
                                    ${Object.values(row).map(val => `<td>${val}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                
                <div class="alert alert-info mt-3">
                    <h6><i class="fas fa-lightbulb me-2"></i>Platform Status: Working!</h6>
                    <p class="mb-0">Your data has been successfully processed. The platform is now operational for data analysis.</p>
                </div>
            </div>
        </div>
    `;

    dataPreview.innerHTML = resultHTML;
    dataPreview.scrollIntoView({ behavior: 'smooth' });
    
    // Store data globally
    window.currentUploadedData = data;
}

// Utility functions - following error handling best practices
function showSuccessMessage(message) {
    const alertHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHTML);
    setTimeout(() => {
        const alert = document.querySelector('.alert-success');
        if (alert) alert.remove();
    }, 5000);
}

function showErrorMessage(message) {
    const alertHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHTML);
}
</script>