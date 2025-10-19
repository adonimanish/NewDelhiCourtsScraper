import streamlit as st
from scraper import DelhiCourtsScraper
from datetime import datetime, timedelta
import json
import os
import pandas as pd

# Page config
st.set_page_config(
    page_title="Delhi Courts Scraper",
    page_icon="⚖️",
    layout="wide"
)

# Title
st.title("⚖️ Delhi District Courts - Cause List Scraper")
st.markdown("### Patiala House Court Complex")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.info("""
    This tool scrapes cause lists from Delhi District Courts website.
    
    **How it works:**
    1. Fetch available courts/judges
    2. Select ONE court
    3. Download cause list as PDF
    
    **Features:**
    - Smart court selection
    - OCR-based CAPTCHA solving
    - PDF generation
    - Fast & simple
    """)
    
    st.header("🔧 Settings")
    headless_mode = st.checkbox("Run browser in headless mode", value=False)

# Initialize session state
if 'available_courts' not in st.session_state:
    st.session_state['available_courts'] = None
if 'courts_fetched' not in st.session_state:
    st.session_state['courts_fetched'] = False

# Step 1: Fetch Available Courts
st.subheader("1️⃣ Fetch Available Courts")

col_fetch1, col_fetch2 = st.columns([1, 3])

with col_fetch1:
    fetch_courts_btn = st.button("🔄 Fetch Courts", type="secondary", use_container_width=True)

with col_fetch2:
    if st.session_state['courts_fetched']:
        st.success(f"✅ {len(st.session_state['available_courts'])} courts available")
    else:
        st.info("Click 'Fetch Courts' to load available court numbers")

# Fetch courts logic
if fetch_courts_btn:
    with st.spinner("Fetching available courts from website... (This will take ~10 seconds)"):
        scraper = DelhiCourtsScraper(headless=True)
        courts = scraper.fetch_available_courts()
        
        if courts:
            st.session_state['available_courts'] = courts
            st.session_state['courts_fetched'] = True
            st.success(f"✅ Successfully fetched {len(courts)} courts!")
            st.rerun()
        else:
            st.error("❌ Failed to fetch courts. Please try again.")

st.markdown("---")

# Only show rest of UI if courts are fetched
if st.session_state['courts_fetched'] and st.session_state['available_courts']:
    
    available_courts = st.session_state['available_courts']
    
    # Step 2: Select ONE Court
    st.subheader("2️⃣ Select ONE Court to Scrape")
    
    # Create options for selectbox (dropdown - single selection)
    court_options = {court['text']: court for court in available_courts}
    
    selected_court_name = st.selectbox(
        "Choose a court/judge:",
        options=["-- Select a Court --"] + list(court_options.keys()),
        help="Select ONE court to scrape its cause list"
    )
    
    # Show selection
    if selected_court_name != "-- Select a Court --":
        st.info(f"📊 **Selected:** {selected_court_name}")
    
    st.markdown("---")
    
    # Step 3: Configuration
    st.subheader("3️⃣ Configure Scraping")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        date_input = st.date_input(
            "Cause List Date",
            value=datetime.now(),
            min_value=datetime.now() - timedelta(days=30),
            max_value=datetime.now() + timedelta(days=30)
        )
        date_str = date_input.strftime("%m/%d/%Y")
    
    with col_config2:
        case_type = st.radio(
            "Case Type",
            options=["Civil", "Criminal"],
            horizontal=True
        )
    
    st.markdown("---")
    
    # Step 4: Start Scraping
    st.subheader("4️⃣ Start Scraping")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        start_scraping = st.button(
            "🚀 Start Scraping",
            type="primary",
            use_container_width=True,
            disabled=(selected_court_name == "-- Select a Court --")
        )
    
    with col_btn2:
        clear_results = st.button("🗑️ Clear Results", use_container_width=True)
    
    with col_btn3:
        if selected_court_name == "-- Select a Court --":
            st.warning("⚠️ Please select a court first")
    
    # Clear results
    if clear_results:
        if 'scraping_results' in st.session_state:
            del st.session_state['scraping_results']
        st.success("Results cleared!")
    
    # Main scraping logic
    if start_scraping and selected_court_name != "-- Select a Court --":
        st.markdown("---")
        st.subheader("📊 Scraping Progress")
        
        # Get selected court object
        selected_court = court_options[selected_court_name]
        
        # Create progress containers
        status_container = st.container()
        progress_bar = st.progress(0)
        progress_text = st.empty()
        results_container = st.container()
        
        with status_container:
            st.info(f"""
            **Configuration:**
            - Court: {selected_court_name}
            - Date: {date_str}
            - Case Type: {case_type.lower()}
            - Headless Mode: {headless_mode}
            """)
            
            st.warning("""
            ⚠️ **Important:**
            - Browser window will open (unless headless mode is on)
            - OCR will attempt to solve CAPTCHA automatically
            - You may need to enter CAPTCHA manually if OCR fails
            - Estimated time: ~2-3 minutes
            """)
        
        # Initialize scraper
        try:
            progress_text.text("Initializing scraper...")
            scraper = DelhiCourtsScraper(headless=headless_mode)
            progress_bar.progress(20)
            
            st.success("✅ Scraper initialized!")
            
            # Start scraping (just ONE court)
            progress_text.text(f"Scraping: {selected_court_name}...")
            progress_bar.progress(40)
            
            results = scraper.scrape_selected_courts(
                selected_courts=[selected_court],  # Only ONE court
                date_str=date_str,
                case_type=case_type.lower()
            )
            
            # Store results
            st.session_state['scraping_results'] = results
            st.session_state['last_scrape_time'] = datetime.now()
            
            # Complete
            progress_bar.progress(100)
            progress_text.text("✅ Scraping complete!")
            
            # Display results
            with results_container:
                st.markdown("---")
                st.subheader("✅ Scraping Complete!")
                
                if results and len(results) > 0:
                    result = results[0]  # Only one result
                    
                    # Status check
                    if result.get('status') == 'success':
                        st.success(f"✅ **Successfully scraped:** {result['court']}")
                        
                        # Show PDF
                        pdf_path = result.get('pdf_path')
                        if pdf_path and os.path.exists(pdf_path):
                            st.markdown("---")
                            st.subheader("📄 Download PDF")
                            
                            col_pdf1, col_pdf2 = st.columns([2, 1])
                            
                            with col_pdf1:
                                st.info(f"**File:** {os.path.basename(pdf_path)}")
                            
                            with col_pdf2:
                                with open(pdf_path, 'rb') as f:
                                    st.download_button(
                                        label="⬇️ Download PDF",
                                        data=f,
                                        file_name=os.path.basename(pdf_path),
                                        mime="application/pdf",
                                        type="primary",
                                        use_container_width=True
                                    )
                        
                        # Show details
                        st.markdown("---")
                        st.subheader("📋 Details")
                        
                        col_detail1, col_detail2, col_detail3 = st.columns(3)
                        with col_detail1:
                            st.metric("Court", result['court'][:30] + "...")
                        with col_detail2:
                            st.metric("Date", result['date'])
                        with col_detail3:
                            st.metric("Case Type", result['case_type'].upper())
                        
                        # JSON data
                        with st.expander("🔍 View JSON Data"):
                            st.json(result)
                            
                            # Download JSON
                            json_str = json.dumps(result, indent=2, ensure_ascii=False)
                            st.download_button(
                                label="📥 Download JSON",
                                data=json_str,
                                file_name=f"court_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                    
                    elif result.get('status') == 'no_cases':
                        st.warning(f"⚠️ No cases found for this court on {date_str}")
                        st.info("This might mean there are no scheduled hearings for this date.")
                    
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        st.info("Please try again or select a different court.")
                
                else:
                    st.error("❌ No results were returned.")
        
        except Exception as e:
            st.error(f"❌ Error during scraping: {str(e)}")
            st.exception(e)

# Display previous result
if 'scraping_results' in st.session_state and not start_scraping:
    st.markdown("---")
    st.subheader("📜 Previous Result")
    
    last_scrape = st.session_state.get('last_scrape_time')
    if last_scrape:
        st.info(f"Last scraped: {last_scrape.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = st.session_state['scraping_results']
    if results and len(results) > 0:
        result = results[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Court", result.get('court', 'N/A')[:20] + "...")
        col2.metric("Status", result.get('status', 'N/A').upper())
        col3.metric("PDF", "✅" if result.get('pdf_path') else "❌")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏛️ Delhi District Courts - Cause List Scraper</p>
    <p style='font-size: 12px;'>Simple & Fast - One Court at a Time | Built with Selenium, OCR, and Streamlit</p>
</div>
""", unsafe_allow_html=True)