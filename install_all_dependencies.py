"""
DataSight AI - Complete Package Installation Script
Following project coding instructions and technology stack requirements
Built for SME business analytics with AI/ML capabilities
"""

import subprocess
import sys
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

# Configure logging following project guidelines
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataSightInstaller:
    """
    Complete dependency installer for DataSight AI platform
    Following project coding instructions and business context
    """
    
    def __init__(self) -> None:
        """Initialize installer with comprehensive package list"""
        self.company_name = "AnalyticaCore AI"
        self.platform_name = "DataSight AI"
    self.contact_email = "information@analyticacoreai.ie"
        
        # Core packages following project technology stack
        self.core_packages = {
            'streamlit': '1.29.0',          # Frontend framework
            'pandas': '2.1.4',             # Data processing
            'numpy': '1.24.4',             # Numerical computing
            'plotly': '5.17.0',            # Visualization
            'scikit-learn': '1.3.2',       # AI/ML algorithms
            'openpyxl': '3.1.2',           # Excel processing
        }
        
        # AI/ML packages following project priorities
        self.ai_ml_packages = {
            'prophet': '1.1.4',            # Time series forecasting
            'xgboost': '2.0.2',            # Gradient boosting
            'scipy': '1.11.4',             # Scientific computing
            'joblib': '1.3.2',             # Model persistence
        }
        
        # Backend packages for FastAPI
        self.backend_packages = {
            'fastapi': '0.104.1',          # REST API framework
            'uvicorn': '0.24.0',           # ASGI server
            'pydantic': '2.5.0',           # Data validation
            'python-multipart': '0.0.6',   # File upload support
        }
        
        # Utility packages
        self.utility_packages = {
            'requests': '2.31.0',          # HTTP requests
            'python-dateutil': '2.8.2',   # Date utilities
            'pytz': '2023.3',              # Timezone support
            'pillow': '10.1.0',            # Image processing
            'xlsxwriter': '3.1.9',         # Excel writing
            'matplotlib': '3.8.2',         # Additional plotting
            'seaborn': '0.13.0',           # Statistical visualization
        }
        
        # Azure deployment packages
        self.azure_packages = {
            'azure-storage-blob': '12.19.0',    # Blob storage
            'azure-identity': '1.15.0',         # Authentication
            'azure-keyvault-secrets': '4.7.0',  # Key Vault
        }
        
        # Development and testing packages
        self.dev_packages = {
            'pytest': '7.4.3',            # Testing framework
            'black': '23.11.0',           # Code formatting
            'flake8': '6.1.0',            # Linting
        }
    
    def check_python_version(self) -> Tuple[bool, str]:
        """
        Check Python version meets project requirements (3.11+)
        Following project guidelines for version validation
        """
        try:
            version_info = sys.version_info
            version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
            
            meets_requirements = version_info >= (3, 11)
            
            if meets_requirements:
                logger.info(f"✅ Python {version_string} meets requirements")
            else:
                logger.warning(f"⚠️ Python {version_string} below recommended 3.11+")
            
            return meets_requirements, version_string
            
        except Exception as e:
            logger.error(f"Error checking Python version: {str(e)}")
            return False, "Unknown"
    
    def upgrade_pip(self) -> bool:
        """Upgrade pip to latest version following best practices"""
        try:
            print("🔄 Upgrading pip to latest version...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Pip upgraded successfully")
                return True
            else:
                print("⚠️ Pip upgrade failed, continuing with current version")
                return False
                
        except Exception as e:
            print(f"⚠️ Pip upgrade error: {str(e)}")
            return False
    
    def install_package_group(self, packages: Dict[str, str], group_name: str) -> Dict[str, bool]:
        """
        Install a group of packages with comprehensive error handling
        Following project guidelines for dependency management
        """
        print(f"\n📦 Installing {group_name} packages...")
        results = {}
        
        for package_name, version in packages.items():
            try:
                package_spec = f"{package_name}=={version}"
                print(f"   Installing {package_spec}...")
                
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package_spec
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"   ✅ {package_name} installed successfully")
                    results[package_name] = True
                else:
                    print(f"   ❌ Failed to install {package_name}")
                    print(f"      Error: {result.stderr.strip()}")
                    results[package_name] = False
                    
            except subprocess.TimeoutExpired:
                print(f"   ❌ Timeout installing {package_name}")
                results[package_name] = False
            except Exception as e:
                print(f"   ❌ Error installing {package_name}: {str(e)}")
                results[package_name] = False
        
        return results
    
    def verify_installation(self, package_name: str) -> bool:
        """
        Verify package installation by importing
        Following project guidelines for validation
        """
        try:
            # Handle special import names
            import_mapping = {
                'scikit-learn': 'sklearn',
                'python-dateutil': 'dateutil',
                'python-multipart': 'multipart',
                'azure-storage-blob': 'azure.storage.blob',
                'azure-identity': 'azure.identity',
                'azure-keyvault-secrets': 'azure.keyvault.secrets',
                'pillow': 'PIL',
                'xgboost': 'xgboost',
                'prophet': 'prophet'
            }
            
            import_name = import_mapping.get(package_name, package_name)
            __import__(import_name)
            return True
            
        except ImportError:
            return False
        except Exception as e:
            logger.error(f"Error verifying {package_name}: {str(e)}")
            return False
    
    def create_requirements_file(self) -> None:
        """
        Create comprehensive requirements.txt file
        Following project guidelines for dependency management
        """
        try:
            all_packages = {
                **self.core_packages,
                **self.ai_ml_packages,
                **self.backend_packages,
                **self.utility_packages,
                **self.azure_packages
            }
            
            requirements_content = f"""# DataSight AI Platform Dependencies
# Following project technology stack requirements and SME business context
# Generated for AI-powered company data analysis platform

# Core Framework - Streamlit for SME business analytics
streamlit=={self.core_packages['streamlit']}

# Data Processing - Following AI/ML best practices
pandas=={self.core_packages['pandas']}
numpy=={self.core_packages['numpy']}

# AI/ML Libraries - Following project priorities for business forecasting
scikit-learn=={self.core_packages['scikit-learn']}
prophet=={self.ai_ml_packages['prophet']}
xgboost=={self.ai_ml_packages['xgboost']}
scipy=={self.ai_ml_packages['scipy']}
joblib=={self.ai_ml_packages['joblib']}

# Visualization - Following business dashboard requirements
plotly=={self.core_packages['plotly']}
matplotlib=={self.utility_packages['matplotlib']}
seaborn=={self.utility_packages['seaborn']}

# Backend API - FastAPI for REST services
fastapi=={self.backend_packages['fastapi']}
uvicorn=={self.backend_packages['uvicorn']}
pydantic=={self.backend_packages['pydantic']}
python-multipart=={self.backend_packages['python-multipart']}

# File Processing - Following data upload requirements
openpyxl=={self.core_packages['openpyxl']}
xlsxwriter=={self.utility_packages['xlsxwriter']}
pillow=={self.utility_packages['pillow']}

# Utilities - Following project requirements
requests=={self.utility_packages['requests']}
python-dateutil=={self.utility_packages['python-dateutil']}
pytz=={self.utility_packages['pytz']}

# Azure Integration - Following deployment requirements
azure-storage-blob=={self.azure_packages['azure-storage-blob']}
azure-identity=={self.azure_packages['azure-identity']}
azure-keyvault-secrets=={self.azure_packages['azure-keyvault-secrets']}
"""
            
            with open('requirements.txt', 'w') as f:
                f.write(requirements_content)
            
            print("✅ requirements.txt file created")
            
        except Exception as e:
            print(f"⚠️ Error creating requirements.txt: {str(e)}")
    
    def run_complete_installation(self) -> Dict[str, Dict[str, bool]]:
        """
        Run complete installation process
        Following project coding instructions and business priorities
        """
        print("=" * 70)
        print(f"🤖 {self.platform_name} - Complete Package Installation")
        print(f"🏢 Company: {self.company_name}")
        print(f"📧 Contact: {self.contact_email}")
        print("=" * 70)
        
        # Check Python version
        python_ok, python_version = self.check_python_version()
        print(f"\n🐍 Python Version: {python_version}")
        
        if not python_ok:
            print("⚠️ Warning: Python version below recommended 3.11+")
            print("   Platform will work but consider upgrading for optimal performance")
        
        # Upgrade pip
        print(f"\n🔧 Preparing installation environment...")
        self.upgrade_pip()
        
        # Install package groups
        all_results = {}
        
        # Core packages (essential)
        all_results['core'] = self.install_package_group(
            self.core_packages, "Core Framework"
        )
        
        # AI/ML packages (business critical)
        all_results['ai_ml'] = self.install_package_group(
            self.ai_ml_packages, "AI/ML Analytics"
        )
        
        # Backend packages (API services)
        all_results['backend'] = self.install_package_group(
            self.backend_packages, "Backend API"
        )
        
        # Utility packages (enhanced functionality)
        all_results['utilities'] = self.install_package_group(
            self.utility_packages, "Utility Libraries"
        )
        
        # Azure packages (deployment)
        all_results['azure'] = self.install_package_group(
            self.azure_packages, "Azure Integration"
        )
        
        # Development packages (optional)
        print(f"\n📦 Installing Development packages (optional)...")
        all_results['development'] = self.install_package_group(
            self.dev_packages, "Development Tools"
        )
        
        # Create requirements file
        print(f"\n📄 Creating requirements.txt file...")
        self.create_requirements_file()
        
        return all_results
    
    def generate_installation_report(self, results: Dict[str, Dict[str, bool]]) -> None:
        """
        Generate comprehensive installation report
        Following project guidelines for user feedback
        """
        print(f"\n" + "=" * 70)
        print(f"📊 DataSight AI Installation Report")
        print(f"=" * 70)
        
        # Calculate totals
        total_packages = 0
        successful_packages = 0
        
        for group_name, group_results in results.items():
            group_success = sum(1 for success in group_results.values() if success)
            group_total = len(group_results)
            total_packages += group_total
            successful_packages += group_success
            
            print(f"\n📦 {group_name.title()} Packages: {group_success}/{group_total}")
            
            # Show successful installations
            for package, success in group_results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {package}")
        
        # Overall success rate
        success_rate = (successful_packages / total_packages) * 100
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({successful_packages}/{total_packages})")
        
        # Core functionality check
        core_required = ['streamlit', 'pandas', 'numpy', 'plotly']
        core_success = all(results.get('core', {}).get(pkg, False) for pkg in core_required)
        
        if core_success:
            print(f"\n🎉 Core Installation Successful!")
            print(f"   DataSight AI platform is ready for SME business analytics")
            
            print(f"\n🚀 Quick Start Commands:")
            print(f"   1. Launch platform: streamlit run install_packages.py")
            print(f"   2. Access at: http://localhost:8501")
            print(f"   3. Load sample SME data to test features")
            
            print(f"\n💼 Available Features:")
            print(f"   • AI-powered revenue forecasting")
            print(f"   • Customer segmentation analysis")
            print(f"   • Business trend detection")
            print(f"   • Growth opportunity identification")
            print(f"   • Real-time business dashboards")
            print(f"   • Executive report generation")
            
        else:
            print(f"\n⚠️ Core Installation Issues Detected")
            print(f"   Some essential packages failed to install")
            print(f"   Platform may not function properly")
        
        # Verification step
        print(f"\n🔍 Running Package Verification...")
        verification_results = {}
        
        for group_name, group_results in results.items():
            for package_name, installed in group_results.items():
                if installed:
                    verified = self.verify_installation(package_name)
                    verification_results[package_name] = verified
                    status = "✅ Verified" if verified else "⚠️ Install OK, Import Failed"
                    print(f"   {package_name}: {status}")
        
        # Final recommendations
        print(f"\n📋 Next Steps:")
        print(f"   1. Test installation: python -c 'import streamlit, pandas, numpy'")
        print(f"   2. Launch DataSight AI: streamlit run install_packages.py")
        print(f"   3. Explore SME business analytics features")
        print(f"   4. Upload your business data for analysis")
        
        print(f"\n📧 Support: {self.contact_email}")
        print(f"🌐 Platform: AI-powered SME business analytics")

def main() -> None:
    """
    Main installation function
    Following project guidelines for comprehensive setup
    """
    try:
        print("🚀 Starting DataSight AI complete installation...")
        
        # Initialize installer
        installer = DataSightInstaller()
        
        # Run installation
        results = installer.run_complete_installation()
        
        # Generate report
        installer.generate_installation_report(results)
        
        print(f"\n🎯 Installation process completed!")
        print(f"Check the report above for detailed results.")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Installation cancelled by user")
    print(f"📧 Contact support if you need assistance: information@analyticacoreai.ie")
    except Exception as e:
        print(f"\n❌ Critical installation error: {str(e)}")
    print(f"📧 Contact support: information@analyticacoreai.ie")
        logger.error(f"Critical installation error: {str(e)}")

if __name__ == "__main__":
    main()