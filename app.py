"""Vedic Astrology Agent - Streamlit Application."""

import streamlit as st
from datetime import datetime

from src.pdf_parser import extract_text_from_pdf
from src.agent import AstrologyAgent

# Page configuration
st.set_page_config(
    page_title="Vedic Astrology Agent",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cosmic Indigo theme - Clean Modern Design
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --primary: #4F46E5;
        --primary-hover: #4338CA;
        --primary-light: #818CF8;
        --primary-bg: #EEF2FF;
        --background: #FAFBFC;
        --surface: #FFFFFF;
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --text-muted: #9CA3AF;
        --border: #E5E7EB;
        --border-light: #F3F4F6;
    }

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main app background */
    .stApp {
        background: linear-gradient(180deg, #FAFBFC 0%, #F3F4F6 100%);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Remove default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 800px !important;
    }

    /* Landing page container */
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
        padding: 2rem;
    }

    /* Logo/Icon */
    .logo-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 6px rgba(79, 70, 229, 0.2));
    }

    /* Main title */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .main-title span {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Subtitle */
    .subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* API Key Card */
    .api-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 2.5rem;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05),
                    0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-light);
    }

    .api-card-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .api-card-desc {
        font-size: 0.875rem;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid var(--border) !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
        background: var(--surface) !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }

    /* Hide input label */
    .stTextInput > label {
        display: none !important;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin-top: 0.5rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Link styling */
    .help-link {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 1rem;
    }

    .help-link a {
        color: var(--primary);
        text-decoration: none;
        font-weight: 500;
    }

    .help-link a:hover {
        text-decoration: underline;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border-light) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    /* Sidebar section titles */
    .sidebar-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--background) !important;
        border-radius: 12px !important;
        border: 2px dashed var(--border) !important;
        padding: 1rem !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-light) !important;
        background: var(--primary-bg) !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }

    [data-testid="stFileUploader"] section > button {
        display: none !important;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 0.5rem !important;
    }

    .stRadio > div > label {
        background: var(--background) !important;
        border-radius: 8px !important;
        padding: 0.625rem 1rem !important;
        border: 1px solid var(--border-light) !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }

    .stRadio > div > label:hover {
        background: var(--primary-bg) !important;
        border-color: var(--primary-light) !important;
    }

    .stRadio > div > label[data-checked="true"] {
        background: var(--primary-bg) !important;
        border-color: var(--primary) !important;
    }

    /* Success message */
    .success-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #ECFDF5;
        color: #059669;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    /* Main content area */
    .content-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid var(--border-light);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .content-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--primary-bg);
    }

    /* Reading content */
    .reading-content {
        line-height: 1.8;
        color: var(--text-primary);
    }

    .reading-content h3 {
        color: var(--primary);
        font-size: 1.125rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    /* Info boxes */
    .info-box {
        background: var(--primary-bg);
        border-radius: 12px;
        padding: 1.25rem;
        border-left: 4px solid var(--primary);
    }

    .info-box-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .info-box-text {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0;
    }

    /* Welcome state */
    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .welcome-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: var(--border-light);
        margin: 1.5rem 0;
    }

    /* Spinner override */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }

    /* Alerts */
    .stAlert {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "current_reading" not in st.session_state:
    st.session_state.current_reading = None
if "reading_category" not in st.session_state:
    st.session_state.reading_category = None


def show_landing_page():
    """Display the landing page with API key input."""

    # Add spacing at top
    st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)

    # Logo and title
    st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">✨</div>
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em;">
                <span style="background: linear-gradient(135deg, #4F46E5 0%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Vedic Astrology Agent</span>
            </h1>
            <p style="font-size: 1.125rem; color: #6B7280; margin-bottom: 3rem;">AI-powered personalized birth chart readings</p>
        </div>
    """, unsafe_allow_html=True)

    # Center the input card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Card container
        st.markdown("""
            <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 10px 15px -3px rgba(0,0,0,0.05); border: 1px solid #F3F4F6; margin-bottom: 1.5rem;">
                <p style="font-size: 1.125rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem; text-align: center;">Enter your Gemini API Key</p>
                <p style="font-size: 0.875rem; color: #9CA3AF; margin-bottom: 1.5rem; text-align: center;">Your key is stored only in this session</p>
            </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Paste your API key here...",
            label_visibility="collapsed"
        )

        if st.button("Get Started", use_container_width=True):
            if not api_key:
                st.error("Please enter your API key")
            else:
                with st.spinner("Validating..."):
                    agent = AstrologyAgent(api_key)
                    is_valid, error_msg = agent.validate_api_key()

                    if is_valid:
                        st.session_state.api_key = api_key
                        st.session_state.api_key_valid = True
                        st.session_state.gemini_model = agent.model  # Store working model
                        st.rerun()
                    else:
                        st.error(error_msg)

        st.markdown("""
            <p style="text-align: center; margin-top: 1.5rem; font-size: 0.875rem; color: #6B7280;">
                Don't have a key? <a href="https://ai.google.dev" target="_blank" style="color: #4F46E5; text-decoration: none; font-weight: 500;">Get one free at ai.google.dev</a>
            </p>
        """, unsafe_allow_html=True)


def show_main_app():
    """Display the main application."""

    # Sidebar
    with st.sidebar:
        st.markdown('<p class="sidebar-title">Upload Chart</p>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            help="Upload your Vedic birth chart PDF",
            label_visibility="collapsed"
        )

        if uploaded_file:
            if uploaded_file.name != st.session_state.pdf_name:
                with st.spinner("Processing..."):
                    try:
                        content = extract_text_from_pdf(uploaded_file)
                        st.session_state.pdf_content = content
                        st.session_state.pdf_name = uploaded_file.name
                        st.session_state.current_reading = None
                    except ValueError as e:
                        st.error(str(e))
                        st.session_state.pdf_content = None
                        st.session_state.pdf_name = None

            if st.session_state.pdf_content:
                st.markdown(f'<div class="success-badge">✓ {uploaded_file.name}</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-title">Reading Type</p>', unsafe_allow_html=True)

        reading_type = st.selectbox(
            "Select reading type",
            options=["General", "Relationship", "Career", "Health", "Wealth", "Dasha", "Annual"],
            label_visibility="collapsed"
        )

        # Year input for annual readings
        year_input = None
        if reading_type == "Annual":
            current_year = datetime.now().year
            year_input = st.number_input(
                "Year",
                min_value=current_year - 10,
                max_value=current_year + 10,
                value=current_year,
                step=1
            )

        # Dasha lord input for dasha readings
        dasha_lord = None
        if reading_type == "Dasha":
            dasha_lord = st.selectbox(
                "Select Dasha Lord",
                options=[
                    "Current (Auto-detect from chart)",
                    "Sun (Surya)",
                    "Moon (Chandra)",
                    "Mars (Mangal)",
                    "Mercury (Budha)",
                    "Jupiter (Guru)",
                    "Venus (Shukra)",
                    "Saturn (Shani)",
                    "Rahu",
                    "Ketu"
                ],
                index=0,
                key="dasha_lord_select"
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Get Reading button
        get_reading_disabled = st.session_state.pdf_content is None

        if st.button("✨ Get Reading", use_container_width=True, disabled=get_reading_disabled):
            if st.session_state.pdf_content:
                category = reading_type.lower()

                with st.spinner(f"Generating {reading_type} reading..."):
                    try:
                        agent = AstrologyAgent(
                            st.session_state.api_key,
                            model=st.session_state.get("gemini_model")
                        )
                        reading = agent.get_reading(
                            category=category,
                            chart_content=st.session_state.pdf_content,
                            year=year_input if category == "annual" else None,
                            dasha_lord=dasha_lord if category == "dasha" else None
                        )
                        st.session_state.current_reading = reading
                        st.session_state.reading_category = reading_type
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        if get_reading_disabled:
            st.caption("Upload a PDF to get started")

        # Clear button
        if st.session_state.current_reading:
            if st.button("Clear", use_container_width=True):
                st.session_state.current_reading = None
                st.session_state.reading_category = None
                st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if st.button("New Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main content area
    if st.session_state.current_reading:
        st.markdown(f"""
            <div class="content-card">
                <h2 class="content-title">{st.session_state.reading_category} Reading</h2>
                <div class="reading-content">
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.current_reading)

        st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.pdf_content:
        st.markdown("""
            <div class="content-card" style="text-align: center; padding: 3rem 2rem;">
                <div class="welcome-icon">📄</div>
                <p class="welcome-title">Chart Ready</p>
                <p class="welcome-text">Select a reading type and click "Get Reading"</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="info-box">
                    <p class="info-box-title">Available Readings</p>
                    <p class="info-box-text">General • Relationship • Career • Health • Wealth • Annual</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="info-box">
                    <p class="info-box-title">Annual Predictions</p>
                    <p class="info-box-text">Select "Annual" and enter a year for yearly forecasts</p>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="content-card" style="text-align: center; padding: 3rem 2rem;">
                <div class="welcome-icon">🌟</div>
                <p class="welcome-title">Welcome</p>
                <p class="welcome-text">Upload your birth chart PDF to get started</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="info-box">
                    <p class="info-box-title">Supported Formats</p>
                    <p class="info-box-text">Jagannatha Hora, Parashara's Light, Astro-Sage, or any chart PDF</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="info-box">
                    <p class="info-box-title">What's Analyzed</p>
                    <p class="info-box-text">Planets, houses, nakshatras, dashas, and yogas in your chart</p>
                </div>
            """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    if not st.session_state.api_key_valid:
        show_landing_page()
    else:
        show_main_app()


if __name__ == "__main__":
    main()
