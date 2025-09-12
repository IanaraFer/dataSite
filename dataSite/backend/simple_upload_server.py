import http.server
import socketserver
import json
import cgi
import os
from datetime import datetime
from urllib.parse import parse_qs

class TrialHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle file upload POST requests"""
        if self.path == '/api/trial/submit-with-file':
            try:
                # Parse the multipart form data
                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' in content_type:
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST'}
                    )
                    
                    # Extract form fields
                    data = {}
                    file_info = {}
                    
                    for field in form.keys():
                        field_item = form[field]
                        if field_item.filename:  # This is a file
                            # Save the uploaded file
                            customer_id = f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{abs(hash(str(datetime.now()))) % 10000:04d}"
                            
                            # Create uploads directory
                            os.makedirs('uploads', exist_ok=True)
                            
                            # Save file
                            filename = f"{customer_id}_{field_item.filename}"
                            filepath = os.path.join('uploads', filename)
                            
                            with open(filepath, 'wb') as f:
                                f.write(field_item.file.read())
                            
                            file_info = {
                                'filename': field_item.filename,
                                'saved_as': filename,
                                'size': os.path.getsize(filepath),
                                'path': filepath
                            }
                            
                            print(f"✅ File uploaded: {field_item.filename} ({file_info['size']} bytes)")
                            
                        else:  # Regular form field
                            data[field] = field_item.value
                    
                    # Generate response
                    customer_id = customer_id if file_info else f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{abs(hash(data.get('email', 'unknown'))) % 10000:04d}"
                    
                    response = {
                        'success': True,
                        'customer_id': customer_id,
                        'message': f"Trial request received! {'Priority processing for your dataset.' if file_info else 'Standard processing.'} You'll receive your report within {'2 hours' if file_info else '24 hours'}.",
                        'file_received': bool(file_info),
                        'file_info': file_info if file_info else None,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Log submission
                    print(f"🎯 Trial submission: {customer_id}")
                    print(f"👤 Customer: {data.get('firstName', '')} {data.get('lastName', '')}")
                    print(f"🏢 Company: {data.get('company', '')}")
                    print(f"📧 Email: {data.get('email', '')}")
                    
                    # Send JSON response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
                else:
                    raise Exception("Invalid content type")
                    
            except Exception as e:
                print(f"❌ Error processing upload: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    'success': False,
                    'error': 'Failed to process upload',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'running',
                'service': 'DataSight AI Trial Handler',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    PORT = 8001
    print(f"🚀 Starting DataSight AI Trial Handler on port {PORT}")
    print(f"📁 File uploads will be saved to: uploads/")
    print(f"🔗 Endpoint: http://localhost:{PORT}/api/trial/submit-with-file")
    
    with socketserver.TCPServer(("", PORT), TrialHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        httpd.serve_forever()
