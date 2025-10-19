#!/usr/bin/env python3
"""
Automated setup script for Delhi Courts Scraper
Handles initial configuration and setup
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    else:
        print("✅ Python version is compatible")

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    dirs = [
        "downloads",
        "downloads/pdfs",
        "downloads/json",
        "downloads/captchas"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
        
        # Create .gitkeep files
        gitkeep_path = os.path.join(dir_path, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            f.write('')

def install_requirements():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ All Python packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing packages: {e}")
        print("   Please run manually: pip install -r requirements.txt")
        sys.exit(1)

def check_system_dependencies():
    """Check for system dependencies"""
    print_header("Checking System Dependencies")
    
    system = platform.system()
    
    # Check Tesseract
    print("Checking for Tesseract OCR...")
    try:
        subprocess.run(['tesseract', '--version'], 
                      capture_output=True, check=True)
        print("✅ Tesseract OCR is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Tesseract OCR not found")
        print("\nPlease install Tesseract:")
        if system == "Windows":
            print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        elif system == "Linux":
            print("   Run: sudo apt install tesseract-ocr")
        elif system == "Darwin":  # macOS
            print("   Run: brew install tesseract")
    
    # Check wkhtmltopdf
    print("\nChecking for wkhtmltopdf...")
    try:
        subprocess.run(['wkhtmltopdf', '--version'], 
                      capture_output=True, check=True)
        print("✅ wkhtmltopdf is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  wkhtmltopdf not found")
        print("\nPlease install wkhtmltopdf:")
        if system == "Windows":
            print("   Download from: https://wkhtmltopdf.org/downloads.html")
        elif system == "Linux":
            print("   Run: sudo apt install wkhtmltopdf")
        elif system == "Darwin":  # macOS
            print("   Run: brew install wkhtmltopdf")
        print("\n   Note: The scraper will save as HTML if wkhtmltopdf is not available")

def create_config_template():
    """Create configuration template file"""
    print_header("Creating Configuration Template")
    
    config_content = """# Delhi Courts Scraper Configuration
# Edit this file to customize paths and settings

[Paths]
# Tesseract OCR path (Windows only, uncomment and set if needed)
# tesseract_cmd = C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# wkhtmltopdf path (Windows only, uncomment and set if needed)
# wkhtmltopdf_path = C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe

[Settings]
# Default headless mode (true/false)
headless = false

# Default case type (civil/criminal)
default_case_type = civil

# Maximum retry attempts for failed courts
max_retries = 3

# Delay between requests (seconds)
request_delay = 2
"""
    
    config_path = "config.ini"
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(config_content)
        print(f"✅ Created configuration file: {config_path}")
    else:
        print(f"⚠️  Configuration file already exists: {config_path}")

def run_tests():
    """Run test script to verify setup"""
    print_header("Running Setup Tests")
    
    print("Running test_scraper.py to verify installation...\n")
    
    try:
        result = subprocess.run([sys.executable, 'test_scraper.py'], 
                              capture_output=False)
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n⚠️  Some tests failed. Please check the output above.")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("""
🎉 Setup is complete! Here's what to do next:

1. If you haven't already, install system dependencies:
   • Tesseract OCR (required for CAPTCHA solving)
   • wkhtmltopdf (required for PDF generation)
   
2. Configure paths (Windows only):
   • Edit config.ini if Tesseract/wkhtmltopdf are not in PATH
   • Or edit captcha_solver.py and pdf_generator.py directly

3. Run the scraper:
   
   Option A - Web Interface (Recommended):
   $ streamlit run app.py
   
   Option B - Command Line:
   $ python run_scraper_cli.py --complex 1 --date today --type civil
   
   Option C - Python Script:
   $ python scraper.py

4. Check the QUICKSTART.md for detailed usage instructions

5. Record a demo video for your submission

6. Submit via: https://wkf.ms/46R6rhH

Need help? Check README.md for detailed documentation.

Good luck with your internship! 🚀
    """)

def main():
    """Main setup function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     DELHI DISTRICT COURTS - CAUSE LIST SCRAPER           ║
    ║                   Setup Wizard                            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("This script will set up your environment for the Delhi Courts Scraper.")
    print("It will create directories, install dependencies, and run tests.\n")
    
    response = input("Continue with setup? (y/n): ").strip().lower()
    if response != 'y':
        print("\nSetup cancelled.\n")
        sys.exit(0)
    
    try:
        # Run setup steps
        check_python_version()
        create_directories()
        install_requirements()
        check_system_dependencies()
        create_config_template()
        run_tests()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()