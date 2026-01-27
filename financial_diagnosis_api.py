"""
Financial Diagnosis API - Integrated with Analytica Core AI
Provides REST API endpoints for personal finance analysis
"""

from flask import Flask, request, jsonify, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
import json
from datetime import datetime
import io
from financial_diagnosis.analytics import analyze_finances
from financial_diagnosis.file_parsers import parse_file
from financial_diagnosis.user_store import UserStore
from financial_diagnosis.diagnostic_engine import run_diagnostics

app = Flask(__name__)
app.secret_key = os.getenv('FINANCE_DIAGNOSIS_SECRET_KEY', 'change-this-in-production')

# Separate database for financial diagnosis users
DIAGNOSIS_DB_PATH = 'financial_diagnosis_users.db'
user_store = UserStore(DIAGNOSIS_DB_PATH)

# Upload configuration
UPLOAD_FOLDER = 'uploads/financial_diagnosis'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator for routes requiring authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'diagnosis_user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/diagnosis/register', methods=['POST'])
def register():
    """Register new financial diagnosis user"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    # Check if user exists
    existing_user = user_store.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409
    
    # Create user
    user_id = user_store.create_user(email, password, name)
    
    return jsonify({
        'message': 'Registration successful',
        'user_id': user_id
    }), 201

@app.route('/api/diagnosis/login', methods=['POST'])
def login():
    """Login to financial diagnosis"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = user_store.verify_user(email, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Set session
    session['diagnosis_user_id'] = user['id']
    session['diagnosis_user_email'] = user['email']
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user.get('name', '')
        }
    }), 200

@app.route('/api/diagnosis/logout', methods=['POST'])
def logout():
    """Logout from financial diagnosis"""
    session.pop('diagnosis_user_id', None)
    session.pop('diagnosis_user_email', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/diagnosis/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    user = user_store.get_user_by_id(session['diagnosis_user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user['id'],
        'email': user['email'],
        'name': user.get('name', ''),
        'created_at': user.get('created_at', '')
    }), 200

# ==================== FILE UPLOAD & ANALYSIS ENDPOINTS ====================

@app.route('/api/diagnosis/upload', methods=['POST'])
@login_required
def upload_file():
    """Upload and parse bank statement or financial data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: CSV, Excel, PDF'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session['diagnosis_user_id']}_{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Parse file
        parsed_data = parse_file(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'records': len(parsed_data) if isinstance(parsed_data, pd.DataFrame) else 0,
            'columns': list(parsed_data.columns) if isinstance(parsed_data, pd.DataFrame) else []
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'File processing error: {str(e)}'}), 500

@app.route('/api/diagnosis/analyze', methods=['POST'])
@login_required
def analyze():
    """
    Comprehensive financial analysis
    Accepts transactions and accounts data
    """
    data = request.get_json()
    
    try:
        # Extract data
        transactions_data = data.get('transactions', [])
        accounts_data = data.get('accounts', [])
        
        # Convert to DataFrames
        if transactions_data:
            transactions_df = pd.DataFrame(transactions_data)
        else:
            return jsonify({'error': 'No transaction data provided'}), 400
        
        accounts_df = pd.DataFrame(accounts_data) if accounts_data else None
        
        # Run analysis
        analysis_result = analyze_finances(transactions_df, accounts_df)
        
        # Run diagnostics
        diagnostics = run_diagnostics(analysis_result)
        
        # Combine results
        result = {
            **analysis_result,
            'diagnostics': diagnostics,
            'analyzed_at': datetime.now().isoformat(),
            'user_id': session['diagnosis_user_id']
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/api/diagnosis/quick-analyze', methods=['POST'])
@login_required
def quick_analyze():
    """
    Quick analysis from uploaded file
    Automatically detects format and runs comprehensive analysis
    """
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Filename required'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Parse file
        parsed_data = parse_file(filepath)
        
        # Assume it's transactions data
        analysis_result = analyze_finances(parsed_data, None)
        
        # Run diagnostics
        diagnostics = run_diagnostics(analysis_result)
        
        result = {
            **analysis_result,
            'diagnostics': diagnostics,
            'analyzed_at': datetime.now().isoformat(),
            'filename': filename
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/api/diagnosis/export-report', methods=['POST'])
@login_required
def export_report():
    """
    Export analysis as PDF report
    """
    data = request.get_json()
    analysis_data = data.get('analysis')
    
    if not analysis_data:
        return jsonify({'error': 'No analysis data provided'}), 400
    
    try:
        # Generate PDF report (simplified version)
        # In production, use reportlab or similar library
        
        report_text = f"""
FINANCIAL DIAGNOSTIC REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: {session['diagnosis_user_email']}

{'='*60}

SUMMARY
{'='*60}
Total Income: €{analysis_data.get('total_income', 0):,.2f}
Total Expenses: €{analysis_data.get('total_expenses', 0):,.2f}
Net Savings: €{analysis_data.get('net_savings', 0):,.2f}
Savings Rate: {analysis_data.get('savings_rate', 0):.1f}%

{'='*60}

DIAGNOSTICS & RECOMMENDATIONS
{'='*60}
"""
        
        diagnostics = analysis_data.get('diagnostics', {})
        for key, value in diagnostics.items():
            report_text += f"\n{key}: {value}\n"
        
        # Return as downloadable text file (upgrade to PDF later)
        output = io.BytesIO()
        output.write(report_text.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'financial_report_{datetime.now().strftime("%Y%m%d")}.txt'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export error: {str(e)}'}), 500

@app.route('/api/diagnosis/history', methods=['GET'])
@login_required
def get_history():
    """Get user's analysis history"""
    # In production, store analysis results in database
    # For now, return empty list
    return jsonify({
        'analyses': [],
        'message': 'Analysis history feature coming soon'
    }), 200

@app.route('/api/diagnosis/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Financial Diagnosis API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
