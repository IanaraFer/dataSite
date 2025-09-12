"""
Application launcher for DataSight AI platform
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    try:
        print("🚀 Starting DataSight AI Platform...")
        print("📊 Opening at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop")
        
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()