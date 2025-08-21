import os
import json
import shutil
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi

class FileUploadHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'running',
                'service': 'DataSight AI File Upload Handler',
                'timestamp': datetime.now().isoformat(),
                'endpoints': ['/api/trial/submit-with-file']
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/trial/submit-with-file':
            try:
                content_type = self.headers.get('Content-Type', '')
                
                if 'multipart/form-data' in content_type:
                    # Parse multipart form data
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={
                            'REQUEST_METHOD': 'POST',
                            'CONTENT_TYPE': content_type
                        }
                    )
                    
                    # Extract form data
                    form_data = {}
                    file_data = None
                    
                    for field_name in form.keys():
                        field = form[field_name]
                        if field.filename:
                            # This is a file upload
                            file_data = {
                                'field_name': field_name,
                                'filename': field.filename,
                                'content_type': field.type,
                                'content': field.file.read()
                            }
                        else:
                            # Regular form field
                            form_data[field_name] = field.value
                    
                    # Generate customer ID
                    email = form_data.get('email', 'unknown')
                    customer_id = f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{abs(hash(email)) % 10000:04d}"
                    
                    # Save file if uploaded
                    file_info = None
                    if file_data:
                        # Create uploads directory
                        upload_dir = 'uploads'
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        # Save file with customer ID prefix
                        safe_filename = f"{customer_id}_{file_data['filename']}"
                        file_path = os.path.join(upload_dir, safe_filename)
                        
                        with open(file_path, 'wb') as f:
                            f.write(file_data['content'])
                        
                        file_info = {
                            'filename': file_data['filename'],
                            'saved_as': safe_filename,
                            'size': len(file_data['content']),
                            'path': file_path,
                            'content_type': file_data['content_type']
                        }
                        
                        print(f"✅ File saved: {file_path} ({file_info['size']} bytes)")
                    
                    # Log submission
                    print(f"🎯 Trial submission: {customer_id}")
                    print(f"👤 Customer: {form_data.get('firstName', '')} {form_data.get('lastName', '')}")
                    print(f"🏢 Company: {form_data.get('company', '')}")
                    print(f"📧 Email: {form_data.get('email', '')}")
                    print(f"📁 File: {file_info['filename'] if file_info else 'None'}")
                    
                    # Save submission data
                    submission_record = {
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat(),
                        'form_data': form_data,
                        'file_info': file_info,
                        'status': 'received'
                    }
                    
                    # Save to JSON file for tracking
                    submissions_dir = 'submissions'
                    os.makedirs(submissions_dir, exist_ok=True)
                    submission_file = os.path.join(submissions_dir, f"{customer_id}.json")
                    
                    with open(submission_file, 'w') as f:
                        json.dump(submission_record, f, indent=2)
                    
                    print(f"📝 Submission saved: {submission_file}")
                    
                    # Prepare response
                    response = {
                        'success': True,
                        'customer_id': customer_id,
                        'message': f"Trial request received successfully! {'Priority processing for your uploaded dataset.' if file_info else 'Standard processing.'} You'll receive your report within {'2 hours' if file_info else '24 hours'}.",
                        'file_received': bool(file_info),
                        'file_info': file_info,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
                else:
                    raise ValueError("Invalid content type - expecting multipart/form-data")
                    
            except Exception as e:
                print(f"❌ Error processing upload: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    'success': False,
                    'error': 'Failed to process upload',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FileUploadHandler)
    
    print(f"🚀 DataSight AI File Upload Server")
    print(f"📡 Running on http://localhost:{port}")
    print(f"📁 Files will be saved to: uploads/")
    print(f"📝 Submissions tracked in: submissions/")
    print(f"🔗 Upload endpoint: /api/trial/submit-with-file")
    print(f"✨ Ready to receive file uploads!")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
