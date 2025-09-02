"""
Python Installation Diagnostic Script
Following project coding guidelines for comprehensive error handling
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_installation() -> dict:
    """
    Check Python and pip installation status
    Following project guidelines for comprehensive error handling
    """
    results = {
        'python_found': False,
        'pip_found': False,
        'python_version': None,
        'python_path': None,
        'pip_path': None,
        'errors': [],
        'recommendations': []
    }
    
    try:
        # Check Python
        python_version = sys.version_info
        results['python_found'] = True
        results['python_version'] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        results['python_path'] = sys.executable
        
        print(f"✅ Python {results['python_version']} found at: {results['python_path']}")
        
        # Check if Python version meets requirements
        if python_version < (3, 11):
            results['errors'].append(f"Python version {results['python_version']} is below required 3.11+")
            results['recommendations'].append("Upgrade to Python 3.11 or higher")
        
    except Exception as e:
        results['errors'].append(f"Python check failed: {str(e)}")
        results['recommendations'].append("Install Python 3.11+ from https://python.org")
    
    # Check pip using different methods
    pip_commands = ['pip', 'pip3', 'python -m pip', 'py -m pip']
    
    for cmd in pip_commands:
        try:
            if cmd.startswith('python') or cmd.startswith('py'):
                # Use subprocess for module calls
                result = subprocess.run(
                    cmd.split() + ['--version'], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
            else:
                # Direct command
                result = subprocess.run(
                    [cmd, '--version'], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
            
            if result.returncode == 0:
                results['pip_found'] = True
                results['pip_path'] = cmd
                print(f"✅ Pip found using command: {cmd}")
                print(f"   Version: {result.stdout.strip()}")
                break
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
            continue
    
    if not results['pip_found']:
        results['errors'].append("Pip not found with any command")
        results['recommendations'].extend([
            "Try: python -m ensurepip --upgrade",
            "Or reinstall Python with 'Add to PATH' option enabled"
        ])
    
    return results

def main():
    """Main diagnostic function"""
    print("🔍 DataSight AI - Python Installation Diagnostic")
    print("=" * 50)
    
    results = check_python_installation()
    
    print("\n📊 Diagnostic Results:")
    print("-" * 30)
    
    if results['python_found']:
        print(f"✅ Python: {results['python_version']}")
    else:
        print("❌ Python: Not found")
    
    if results['pip_found']:
        print(f"✅ Pip: Available via '{results['pip_path']}'")
    else:
        print("❌ Pip: Not found")
    
    if results['errors']:
        print("\n⚠️ Issues Found:")
        for error in results['errors']:
            print(f"   - {error}")
    
    if results['recommendations']:
        print("\n🔧 Recommended Actions:")
        for rec in results['recommendations']:
            print(f"   - {rec}")
    
    print("\n" + "=" * 50)
    
    # Provide specific solutions based on findings
    if not results['pip_found'] and results['python_found']:
        print("\n🛠️ Quick Fix Commands:")
        print("Try these commands in order:")
        print("1. python -m ensurepip --upgrade")
        print("2. python -m pip install --upgrade pip")
        print("3. python -m pip install streamlit pandas numpy")
    
    # Batch script content as a multi-line string
    batch_script = r"""
@echo off
echo ========================================
echo DataSight AI - Python Installation Fix
echo Company: AnalyticaCore AI
echo Contact: analyticacoreai@outlook.com
echo ========================================

echo.
echo 🔍 Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo.
    echo 🔧 Trying alternative Python commands...
    py --version
    if %errorlevel% neq 0 (
        echo ❌ No Python installation found
        echo.
        echo 💡 Solution: Install Python from https://python.org
        echo    ✅ Make sure to check "Add Python to PATH" during installation
        pause
        exit /b 1
    ) else (
        echo ✅ Python found via 'py' command
        set PYTHON_CMD=py
    )
) else (
    echo ✅ Python found via 'python' command
    set PYTHON_CMD=python
)

echo.
echo 🔍 Step 2: Checking pip availability...
%PYTHON_CMD% -m pip --version
if %errorlevel% neq 0 (
    echo ❌ Pip not available
    echo.
    echo 🔧 Installing pip...
    %PYTHON_CMD% -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pip
        pause
        exit /b 1
    )
) else (
    echo ✅ Pip is available
)

echo.
echo 🔍 Step 3: Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip

echo.
echo 🔍 Step 4: Creating virtual environment...
if exist venv rmdir /s /q venv
%PYTHON_CMD% -m venv venv

echo.
echo 🔍 Step 5: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 🔍 Step 6: Installing DataSight AI dependencies...
echo Installing core packages...
python -m pip install streamlit
if %errorlevel% neq 0 (
    echo ❌ Failed to install Streamlit
    pause
    exit /b 1
)

python -m pip install pandas
if %errorlevel% neq 0 (
    echo ❌ Failed to install Pandas
    pause
    exit /b 1
)

python -m pip install numpy
if %errorlevel% neq 0 (
    echo ❌ Failed to install NumPy
    pause
    exit /b 1
)

echo.
echo 🔍 Step 7: Testing installation...
python -c "import streamlit, pandas, numpy; print('✅ All packages installed successfully!')"
if %errorlevel% neq 0 (
    echo ❌ Package import test failed
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed successfully!
echo.
echo 🚀 To run DataSight AI:
echo 1. venv\Scripts\activate
echo 2. streamlit run app_test.py
echo.
echo 🌐 The application will open at: http://localhost:8501
echo 📧 Support: analyticacoreai@outlook.com
echo.
pause
"""
    # Save the batch script to a file
    bat_file = Path("install_diagnostics_fix.bat")
    bat_file.write_text(batch_script.strip())
    print(f"📝 Batch script saved as: {bat_file.resolve()}")
    
    return results

if __name__ == "__main__":
    main()