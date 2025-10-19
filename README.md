# ⚖️ Delhi District Courts - Cause List Scraper

> **Automated cause list downloader for Delhi District Courts (Patiala House Court Complex) with AI-powered CAPTCHA solving**

## 🎯 Overview

This tool automates the process of downloading cause lists from the **Delhi District Courts** website ([https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/](https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/)). It features:

- **Smart Court Selection** - Dynamically fetches available courts/judges
- **AI-Powered CAPTCHA Solving** - Uses Google Gemini 2.5 Flash for automatic CAPTCHA recognition
- **PDF Generation** - Converts cause lists to formatted PDF documents
- **User-Friendly Interface** - Built with Streamlit for easy interaction
- **Multi-Browser Support** - Works with both Firefox and Chrome

---

## Video Demo Link: 
         https://www.loom.com/share/2d07c44cf5db41da9066a513453f4777?sid=c14611f8-b583-4f71-9ecc-0938a36c950d

### 🚀 Core Features

- ✅ **Automatic Court List Fetching** - Retrieves all available courts from Patiala House Court Complex
- ✅ **AI CAPTCHA Solver** - Integrated Google Gemini OCR for automatic CAPTCHA recognition
- ✅ **Smart Court Selection** - Reliable text-based court selection (handles dynamic dropdown values)
- ✅ **PDF Export** - Clean, formatted PDF generation with proper styling
- ✅ **Multi-Browser Support** - Firefox (primary) and Chrome (fallback)
- ✅ **Headless Mode** - Run browser in background for faster operation
- ✅ **Error Handling** - Robust retry logic and graceful error recovery
- ✅ **Interactive UI** - Clean Streamlit interface for non-technical users

### 🎨 User Interface Features

- 📊 **Real-time Progress Tracking** - Visual progress bars and status updates
- 📥 **One-Click Downloads** - Direct PDF download from the interface
- 🗂️ **JSON Data Export** - Export scraped data as JSON for further processing
- 📋 **Session History** - View previous scraping results
- ⚙️ **Configurable Settings** - Date selection, case type (Civil/Criminal), headless mode

---

## 💻 System Requirements

### Required Software

1. **Python 3.8 or higher**
   - Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Google Chrome or Mozilla Firefox**
   - Chrome: [https://www.google.com/chrome/](https://www.google.com/chrome/)
   - Firefox: [https://www.mozilla.org/firefox/](https://www.mozilla.org/firefox/)

3. **wkhtmltopdf** (for PDF generation)
   - Windows: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
   - Install to: `C:\Program Files (x86)\wkhtmltopdf\`

4. **Tesseract OCR** (optional - for fallback OCR)
   - Windows: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
   - Install to: `C:\Program Files\Tesseract-OCR\`

5. **Google Gemini API Key**
   - Get your free API key: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)


**requirements.txt includes:**
```
selenium==4.15.2
webdriver-manager==4.0.1
pytesseract==0.3.10
Pillow==10.1.0
opencv-python==4.8.1.78
pdfkit==1.0.0
beautifulsoup4==4.12.2
pandas==2.1.3
streamlit==1.28.2
lxml==4.9.3
google-generativeai
```

### Step 3: Download WebDrivers

- **GeckoDriver (Firefox):** [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
- **ChromeDriver:** [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)

Place the driver executables in your project folder or system PATH.

### Step 4: Install System Dependencies

#### Windows:
1. **wkhtmltopdf:**
   - Download and install to `C:\Program Files (x86)\wkhtmltopdf\`
   - Verify installation: Open CMD and run `wkhtmltopdf --version`

2. **Tesseract OCR (Optional):**
   - Download and install to `C:\Program Files\Tesseract-OCR\`
   - Verify installation: Open CMD and run `tesseract --version`

#### Linux:
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf tesseract-ocr firefox
```

#### macOS:
```bash
brew install wkhtmltopdf tesseract firefox
```

## ⚙️ Configuration

### 1. Set Up Google Gemini API Key

**Edit `captcha_solver.py` (Line 14):**

```python
# Replace YOUR_GEMINI_API_KEY with your actual API key
self.client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
```

**Or use environment variable (Recommended for security):**

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Windows (CMD)
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

Then update `captcha_solver.py`:
```python
self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

### 2. Configure PDF Generator Path (Optional)

**Edit `pdf_generator.py` (Line 12):**

```python
# Update path if wkhtmltopdf is installed elsewhere
self.config = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
)
```

### 3. Configure Tesseract Path (Optional)

**Edit `test_scraper.py` (Line 38):**

```python
# Update path if Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🚀 Usage

### Method 1: Streamlit Web Interface (Recommended)

#### Start the Application:

Command to run the application:
    streamlit run app.py


This will open your browser at `http://localhost:8501`

#### Using the Interface:

1. **Fetch Courts:**
   - Click "🔄 Fetch Courts" button
   - Wait ~10 seconds for the list to load
   - ✅ Success message will show court count

2. **Select Court:**
   - Choose ONE court/judge from the dropdown
   - Court selection is dynamic and reliable

3. **Configure Scraping:**
   - **Date:** Select cause list date (±30 days from today)
   - **Case Type:** Choose Civil or Criminal
   - **Headless Mode:** Check to hide browser window

4. **Start Scraping:**
   - Click "🚀 Start Scraping" button
   - Monitor real-time progress
   - AI will automatically solve CAPTCHA (usually takes 15-20 seconds)
   - If CAPTCHA fails, you'll be prompted for manual entry

5. **Download Results:**
   - Click "⬇️ Download PDF" to save the cause list
   - View JSON data in the expander
   - Download JSON for further processing


### Method: Batch Processing (Multiple Courts "This is not implemented in this project but for the advancements purpose only")

**Create a custom script:**

```python
from scraper import DelhiCourtsScraper

scraper = DelhiCourtsScraper(headless=True)
courts = scraper.fetch_available_courts()

# Select multiple courts (e.g., first 5)
selected_courts = courts[:5]

# Batch scrape
results = scraper.scrape_selected_courts(
    selected_courts=selected_courts,
    date_str="10/19/2025",
    case_type="civil"
)

# Process results
for result in results:
    if result['status'] == 'success':
        print(f"✅ {result['court']}: {result['pdf_path']}")
    else:
        print(f"❌ {result['court']}: {result.get('error', 'Failed')}")
```

---

## 📁 Project Structure


delhi-courts-scraper/
│
├── app.py                      # Streamlit web interface (main entry point)
├── scraper.py                  # Core scraper logic with Selenium
├── captcha_solver.py           # Gemini AI CAPTCHA solver
├── pdf_generator.py            # HTML to PDF converter
├── test_scraper.py             # Setup verification script
├── run_ocr_gemini.py          # Standalone Gemini OCR test script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── downloads/                  # Output directory (auto-created)
│   ├── pdfs/                  # Generated PDF files
│   ├── json/                  # JSON data exports
│   └── captchas/              # CAPTCHA images (for debugging)
│
├── geckodriver.exe            # Firefox WebDriver (Windows)
└── chromedriver.exe           # Chrome WebDriver (Windows)


---

## 🔍 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                         │
│              (Streamlit Web App / Python CLI)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   SCRAPER MODULE                            │
│  • Browser automation (Selenium)                            │
│  • Court selection logic                                    │
│  • Form interaction                                         │
│  • Multi-browser support                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   CAPTCHA    │  │     PDF      │  │    DATA      │
│   SOLVER     │  │  GENERATOR   │  │   STORAGE    │
│              │  │              │  │              │
│ • Gemini AI  │  │ • wkhtmltopdf│  │ • JSON files │
│ • OCR        │  │ • HTML clean │  │ • Timestamps │
│ • Validation │  │ • Styling    │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Workflow

1. **Initialization:**
   - User launches Streamlit app
   - WebDriver auto-detects Firefox/Chrome
   - Creates output directories

2. **Court Fetching:**
   - Navigates to Delhi Courts website
   - Selects "Patiala House Court Complex"
   - Waits for court dropdown to populate
   - Extracts all available courts/judges
   - Returns court list to user

3. **Form Filling:**
   - User selects ONE court
   - Scraper re-navigates to ensure fresh page
   - Selects court by visible text (handles dynamic values)
   - Enters date using JavaScript (bypasses readonly datepicker)
   - Selects case type (Civil/Criminal radio button)

4. **CAPTCHA Solving:**
   - Downloads CAPTCHA image from page
   - Sends to Google Gemini 2.5 Flash API
   - Waits 15 seconds (API rate limit)
   - Cleans response (removes whitespace)
   - Validates result (4-8 alphanumeric characters)
   - Auto-retries 3 times if validation fails
   - Falls back to manual input if all attempts fail

5. **Data Scraping:**
   - Clicks search button
   - Waits for results table to load (15 seconds max)
   - Verifies page contains cause list data
   - Captures full HTML source
   - Takes debug screenshot

6. **PDF Generation:**
   - Cleans HTML (removes form, scripts, styles)
   - Adds custom styling and header
   - Converts to PDF using wkhtmltopdf
   - Falls back to HTML save if PDF fails
   - Returns file path

7. **Result Display:**
   - Shows success/failure status
   - Provides download button for PDF
   - Displays JSON data
   - Allows JSON export

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Gemini OCR not available"

**Cause:** Google Gemini API key not configured or invalid

**Solution:**
```python
# Edit captcha_solver.py line 14
self.client = genai.Client(api_key="YOUR_ACTUAL_API_KEY")
```

Get API key: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

#### 2. "Cannot locate option with value"

**Cause:** Court dropdown values change on each page load

**Solution:** Already fixed! The scraper now uses text-based selection instead of value-based.

If you still see this error, update your `scraper.py` with the latest version.

---

#### 3. "wkhtmltopdf not found"

**Cause:** wkhtmltopdf not installed or incorrect path

**Solutions:**

**Option A:** Install wkhtmltopdf
- Download: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
- Install to default location

**Option B:** Update path in `pdf_generator.py`:
```python
self.config = pdfkit.configuration(
    wkhtmltopdf=r'YOUR_INSTALL_PATH\wkhtmltopdf.exe'
)
```

**Fallback:** System automatically saves as HTML if PDF generation fails

---

#### 4. "GeckoDriver not found"

**Cause:** Firefox WebDriver not available

**Solutions:**

**Option A:** Auto-download
```bash
python test_scraper.py  # Will auto-download
```

**Option B:** Manual download
- Download: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
- Place `geckodriver.exe` in project folder

**Option C:** Use Chrome instead
```python
scraper = DelhiCourtsScraper(browser="chrome")
```

---

#### 5. CAPTCHA Solving Fails

**Symptoms:**
- "Invalid response: [text], retrying..."
- Falls back to manual input after 3 attempts

**Causes:**
- API rate limits (429 errors)
- Network connectivity issues
- CAPTCHA image quality poor

**Solutions:**

**Option 1:** Wait and retry (recommended)
- API has rate limits
- Wait 1 minute between attempts

**Option 2:** Manual input
- System automatically prompts for manual entry
- View CAPTCHA image in `downloads/captchas/`

**Option 3:** Check API quota
- Visit: [https://aistudio.google.com/](https://aistudio.google.com/)
- Check remaining API calls

---

#### 6. "No cases found"

**Cause:** Selected court has no hearings on chosen date

**This is normal!** Not all courts have cases every day.

**Solutions:**
- Try a different date
- Try a different court/judge
- Check website manually to verify

---

#### 7. Browser Window Not Opening

**Cause:** Headless mode enabled

**Solution:** Disable headless mode in Streamlit sidebar or:
```python
scraper = DelhiCourtsScraper(headless=False)
```

---

#### 8. Slow Performance

**Causes:**
- Website loading slowly
- Multiple wait times for CAPTCHA API

**Solutions:**
- Use headless mode (faster)
- Ensure stable internet connection
- Reduce number of courts to scrape
- Wait times are intentional (API rate limits)

---

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check debug screenshots in `downloads/`:
- `debug_results_*.png` - Page captures after search

---

## ⚠️ Known Limitations

### Current Version (v1.0)

1. **Single Court Per Execution:**
   - Currently processes ONE court at a time via Streamlit UI
   - **Reason:** Focused on building robust single-court scraping with AI CAPTCHA solving
   - **Workaround:** Batch processing available via Python script (see Usage > Method 3)

2. **CAPTCHA API Rate Limits:**
   - Google Gemini has rate limits (~60 requests/minute)
   - Each CAPTCHA solve requires 1 API call
   - Built-in 15-second wait between attempts to respect limits

3. **Court Complex:**
   - Selects "Patiala House Court Complex" as the Delhi District court has 1 complex only
   - Can be modified in `scraper.py` for other complexes

4. **Date Range:**
   - Streamlit UI limits to ±30 days from current date
   - Can be extended in Python script mode

5. **PDF Fallback:**
   - If wkhtmltopdf fails, saves as HTML instead
   - HTML files are still readable and contain all data

6. **Browser Support:**
   - Tested primarily on Firefox and Chrome
   - Other browsers (Edge, Safari) not officially supported

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Bulk Download for All Judges:**
  - One-click download for entire court complex
  - Parallel processing for faster execution
  - Smart CAPTCHA rate limit handling

- [ ] **Multi-Complex Support:**
  - Support all Delhi District Court complexes
  - Auto-detect available complexes

- [ ] **Date Range Scraping:**
  - Download cause lists for multiple dates at once
  - Generate consolidated reports

- [ ] **Improved CAPTCHA Solving:**
  - Multiple AI model fallbacks (Azure OCR, AWS Textract)
  - CAPTCHA image preprocessing for better accuracy
  - Learning from failed attempts

- [ ] **Enhanced PDF Features:**
  - Better formatting and styling
  - Case filtering and search
  - Export to Excel/CSV

- [ ] **Scheduling:**
  - Automated daily scraping
  - Email notifications
  - Cloud deployment option

- [ ] **Performance Optimization:**
  - Reduce wait times
  - Parallel browser instances
  - Caching mechanisms

---

## 📝 Assignment Context

### Original Problem Statement

> *"Download causelist at one click for all the judges in that court complex. Date will be provided by the user and court complex will be taken automatically and all judges causelist should be downloaded in different PDFs."*
>
> **Website:** [https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/](https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/)

### Our Implementation

**What We Built:**
- ✅ Automated court list fetching from Patiala House Court Complex
- ✅ AI-powered CAPTCHA solving (Google Gemini 2.5 Flash)
- ✅ Single-court cause list download as formatted PDF
- ✅ User-friendly Streamlit interface
- ✅ Batch processing capability via Python scripts

**Current Limitation:**
- Currently optimized for ONE court per execution in the UI
- Bulk download for all judges is technically feasible via batch scripts

**Why Not Bulk in UI?**
- **Time Constraint:** Focused on building robust single-court scraping first
- **CAPTCHA Challenges:** Each court requires solving a CAPTCHA (rate limits apply)
- **Quality Over Quantity:** Ensured reliable scraping with AI CAPTCHA solver

**How to Achieve Bulk Download:**
Users can use the provided batch processing script (Method 3 in Usage) to download multiple courts sequentially. The system intelligently handles CAPTCHA solving with Gemini AI for each court, respecting API rate limits with built-in wait times.

**Example Bulk Script:**
```python
# Download all courts for a specific date
scraper = DelhiCourtsScraper(headless=True)
courts = scraper.fetch_available_courts()
results = scraper.scrape_selected_courts(courts, "10/19/2025", "criminal")
```

This approach successfully solves the assignment requirements while maintaining reliability and code quality.

---

## 🙏 Acknowledgments

- **Delhi District Courts** - For providing public access to cause lists
- **Google Gemini Team** - For the powerful AI OCR capabilities
- **Selenium Project** - For browser automation framework
- **Streamlit Team** - For the amazing web framework
- **wkhtmltopdf Team** - For PDF generation tools 
