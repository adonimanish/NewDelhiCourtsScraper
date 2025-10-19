"""
Simple test script to verify the scraper setup
Run this before the main scraper to check if everything is configured correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing Python package imports...")
    
    packages = {
        'selenium': 'Selenium',
        'cv2': 'OpenCV',
        'pytesseract': 'Pytesseract',
        'PIL': 'Pillow',
        'pdfkit': 'PDFKit',
        'bs4': 'BeautifulSoup4',
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
    }
    
    failed = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Not installed!")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed!\n")
        return True

def test_tesseract():
    """Test if Tesseract OCR is accessible"""
    print("🔍 Testing Tesseract OCR...")
    
    try:
        import pytesseract
        from PIL import Image
        import numpy as np

        # 🔹 Add this line to tell pytesseract where Tesseract is installed
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"  ✅ Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"  ❌ Tesseract not found or not configured!")
        print(f"  Error: {e}")
        print("\n  Solutions:")
        print("  1. Install Tesseract: https://github.com/tesseract-ocr/tesseract")
        print("  2. Set path in captcha_solver.py:")
        print("     pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        return False


def test_wkhtmltopdf():
    """Test if wkhtmltopdf is accessible"""
    print("🔍 Testing wkhtmltopdf...")
    
    try:
        import pdfkit
        
        # 🔹 Explicitly set path to wkhtmltopdf executable
        path_wkhtmltopdf = r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        
        # Try a dummy call to see if config works
        # You can comment this out if you don't want to generate a file
        # pdfkit.from_string("Test", "test.pdf", configuration=config)

        print(f"  ✅ wkhtmltopdf found at: {path_wkhtmltopdf}")
        return True
    except Exception as e:
        print(f"  ⚠️  wkhtmltopdf might not be configured")
        print(f"  Error: {e}")
        print("\n  Solutions:")
        print("  1. Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        print("  2. Set path in pdf_generator.py if needed")
        print("  Note: System will fall back to HTML if PDF generation fails")
        return False


def test_selenium():
    """Test if Selenium and WebDriver work"""
    print("🔍 Testing Selenium WebDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("  ⏳ Downloading/updating ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"  ✅ ChromeDriver ready at: {driver_path}")
        
        # Try to initialize driver (don't actually open browser)
        print("  ✅ Selenium configuration OK")
        return True
    except Exception as e:
        print(f"  ❌ Selenium setup failed!")
        print(f"  Error: {e}")
        return False

def test_directories():
    """Create necessary directories"""
    print("🔍 Creating output directories...")
    
    dirs = [
        "downloads",
        "downloads/pdfs",
        "downloads/json",
        "downloads/captchas"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"  ✅ {dir_path}")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("  DELHI COURTS SCRAPER - SETUP VERIFICATION")
    print("="*60)
    print()
    
    results = {
        'Python Packages': test_imports(),
        'Tesseract OCR': test_tesseract(),
        'wkhtmltopdf': test_wkhtmltopdf(),
        'Selenium WebDriver': test_selenium(),
        'Directories': test_directories()
    }
    
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the scraper.")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Or run: python scraper.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the scraper.")
        print("\nCritical issues (must fix):")
        print("  - Python Packages")
        print("  - Selenium WebDriver")
        print("\nOptional issues (has fallbacks):")
        print("  - Tesseract OCR (will ask for manual CAPTCHA input)")
        print("  - wkhtmltopdf (will save as HTML instead of PDF)")
    
    print()
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)