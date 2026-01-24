"""Vedic Astrology Agent - Streamlit Application."""

import streamlit as st
from datetime import datetime

from src.pdf_parser import extract_text_from_pdf
from src.agent import AstrologyAgent

# Page configuration
st.set_page_config(
    page_title="Vedic Astrology Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Mobile Friendly + Chat UI
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Root variables - Clean professional theme */
    :root {
        --primary: #4a5568;
        --primary-hover: #2d3748;
        --primary-light: #718096;
        --primary-bg: #f7fafc;
        --background: #ffffff;
        --surface: #ffffff;
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --border: #e2e8f0;
        --border-light: #edf2f7;
        --accent: #2d3748;
        --success: #48bb78;
        --success-bg: #f0fff4;
    }

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main app background - force light theme */
    .stApp {
        background: var(--background) !important;
        color: var(--text-primary) !important;
    }

    /* Override dark mode text colors */
    .stApp p, .stApp li, .stApp td, .stApp th, .stApp span, .stApp div, .stApp label {
        color: var(--text-primary);
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp strong {
        color: #000000 !important;
    }

    .stMarkdown {
        color: var(--text-primary) !important;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main container */
    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }

    /* Mobile responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem !important;
        }

        .desktop-only {
            display: none !important;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        .stButton > button {
            padding: 0.75rem 1rem !important;
            font-size: 0.9rem !important;
        }
    }

    /* Header bar */
    .header-bar {
        background: var(--surface);
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-light);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -1rem -1rem 1rem -1rem;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .header-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Config panel */
    .config-panel {
        background: var(--surface);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid var(--border-light);
        margin-bottom: 1rem;
    }

    .config-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: end;
    }

    /* Input styling - force light theme */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1.5px solid var(--border) !important;
        font-size: 0.9rem !important;
        background-color: #FFFFFF !important;
        color: #1a202c !important;
    }

    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1a202c !important;
    }

    .stSelectbox [data-baseweb="select"] span {
        color: #1a202c !important;
    }

    /* Number input - force light theme */
    .stNumberInput > div,
    .stNumberInput > div > div,
    .stNumberInput [data-baseweb="input"],
    .stNumberInput [data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #1a202c !important;
    }

    .stNumberInput button {
        background-color: #f7fafc !important;
        color: #1a202c !important;
        border-color: var(--border) !important;
    }

    .stNumberInput button:hover {
        background-color: #edf2f7 !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #9CA3AF !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(74, 85, 104, 0.1) !important;
    }

    /* Dropdown menu styling - force light theme */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [data-baseweb="select"] [data-baseweb="popover"],
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="menu"],
    [data-baseweb="menu"] ul,
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="menu"] li,
    ul[role="listbox"] li,
    li[role="option"] {
        color: #1a202c !important;
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #f7fafc !important;
        background: #f7fafc !important;
    }

    /* Dropdown arrow visibility */
    .stSelectbox svg {
        fill: #4a5568 !important;
        color: #4a5568 !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
    }

    /* Button styling - Clean dark buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.25rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }

    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background: var(--primary-hover) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    .stButton > button:disabled {
        background: #cbd5e0 !important;
        color: #718096 !important;
        box-shadow: none !important;
    }

    .stButton > button:disabled p,
    .stButton > button:disabled span {
        color: #718096 !important;
    }

    /* Chat container */
    .chat-container {
        background: var(--surface);
        border-radius: 12px;
        border: 1px solid var(--border-light);
        height: calc(100vh - 280px);
        min-height: 400px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
    }

    .chat-input-area {
        border-top: 1px solid var(--border-light);
        padding: 1rem;
        background: var(--background);
    }

    /* Message styling */
    .stChatMessage {
        background: transparent !important;
        padding: 0.5rem 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        background: var(--surface) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: var(--text-primary) !important;
    }

    /* Force dark text on light backgrounds */
    [data-testid="stChatMessageContent"],
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li,
    [data-testid="stChatMessageContent"] td,
    [data-testid="stChatMessageContent"] th,
    [data-testid="stChatMessageContent"] span,
    [data-testid="stChatMessageContent"] div,
    [data-testid="stChatMessageContent"] ul,
    [data-testid="stChatMessageContent"] ol {
        color: #1a202c !important;
    }

    [data-testid="stChatMessageContent"] h1,
    [data-testid="stChatMessageContent"] h2,
    [data-testid="stChatMessageContent"] h3,
    [data-testid="stChatMessageContent"] h4,
    [data-testid="stChatMessageContent"] h5,
    [data-testid="stChatMessageContent"] strong,
    [data-testid="stChatMessageContent"] b {
        color: #000000 !important;
    }

    /* Streaming text fix */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #1a202c !important;
    }

    /* User message */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
        background: #f8fafc !important;
        border-color: var(--border) !important;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 6px !important;
    }

    .stChatInput > div {
        border-radius: 6px !important;
        border: 1px solid var(--border) !important;
    }

    .stChatInput > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(26, 26, 46, 0.1) !important;
    }

    /* File uploader - clean light style */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border-radius: 8px !important;
        border: 1px dashed #cbd5e0 !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary) !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 1rem !important;
        background: #ffffff !important;
    }

    [data-testid="stFileUploader"] section > div {
        background: #f7fafc !important;
        border-radius: 6px !important;
        padding: 1rem !important;
    }

    [data-testid="stFileUploader"] section > div > div {
        background: transparent !important;
    }

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: var(--text-secondary) !important;
    }

    [data-testid="stFileUploader"] button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
    }

    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button p {
        color: #ffffff !important;
    }

    /* Success alert override */
    .stAlert {
        border-radius: 6px !important;
    }

    /* Welcome card */
    .welcome-card {
        background: var(--surface);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        border: 1px solid var(--border-light);
    }

    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 0.75rem;
    }

    .welcome-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }

    /* Landing page */
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 2rem 1rem;
    }

    .landing-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 2rem;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-light);
        margin-top: 1rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--background) !important;
        border-radius: 8px !important;
    }

    /* Selectbox label hide */
    .stSelectbox > label, .stFileUploader > label {
        font-size: 0.75rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
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
if "last_query" not in st.session_state:
    st.session_state.last_query = None
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None


def show_landing_page():
    """Display the landing page with API key input."""

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="landing-container">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">✨</div>
                <h1 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem;">
                    <span style="color: #1a202c; font-weight: 700;">Vedic Astrology Agent</span>
                </h1>
                <p style="color: #6B7280; margin-bottom: 0;">AI-powered birth chart readings</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("**Enter your Gemini API Key**")
        st.caption("Your key is stored only in this session")

        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Paste your API key...",
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
                        st.session_state.gemini_model = agent.model
                        st.rerun()
                    else:
                        st.error(error_msg)

        st.markdown("""
            <p style="text-align: center; margin-top: 1rem; font-size: 0.8rem; color: #6B7280;">
                <a href="https://aistudio.google.com/apikey" target="_blank" style="color: #2d3748; text-decoration: underline;">Get a free API key</a>
            </p>
        """, unsafe_allow_html=True)


def stream_chat_response(user_message: str):
    """Stream response from the astrology agent for chat."""
    agent = AstrologyAgent(
        st.session_state.api_key,
        model=st.session_state.gemini_model
    )

    # Build context from last response if available
    context = ""
    if st.session_state.last_response:
        context = f"Previous reading:\n{st.session_state.last_response[:2000]}...\n\n"

    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""**ROLE:** You are an expert Vedic Astrologer having a conversation about the user's birth chart.

**TODAY'S DATE:** {today}

**CHART DATA:**
{st.session_state.pdf_content}

{context}**USER'S QUESTION:** {user_message}

**INSTRUCTIONS:**
- Answer based strictly on the chart data provided
- Be conversational but precise
- Reference specific planetary positions when relevant
- Keep responses focused and not too long unless detail is requested
- Use today's date to determine current dasha periods"""

    try:
        for chunk in agent.stream_chat(prompt):
            yield chunk
    except Exception as e:
        yield f"Error: {str(e)}"


def show_main_app():
    """Display the main application with chat interface."""

    # Centered container
    col_left, col_main, col_right = st.columns([1, 3, 1])

    with col_main:
        # Header row
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.markdown("### ✨ Vedic Astrology Agent")
        with header_col2:
            if st.button("🔄 New Session", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("")  # Spacing

        # Upload section
        uploaded_file = st.file_uploader(
            "Upload your birth chart",
            type=["pdf"],
            help="Complete PDF reports work best"
        )
        st.caption("Supports PDF from Astro-Sage, Jagannatha Hora, or other Vedic astrology software.")

        if uploaded_file:
            if uploaded_file.name != st.session_state.pdf_name:
                with st.spinner("Processing..."):
                    try:
                        content = extract_text_from_pdf(uploaded_file)
                        st.session_state.pdf_content = content
                        st.session_state.pdf_name = uploaded_file.name
                        st.session_state.last_query = None
                        st.session_state.last_response = None
                    except ValueError as e:
                        st.error(str(e))

            if st.session_state.pdf_content:
                st.success(f"Chart loaded: {uploaded_file.name}")

        st.markdown("")  # Spacing

        # Reading options row
        opt_col1, opt_col2, opt_col3 = st.columns([2, 2, 1.5])

        with opt_col1:
            reading_type = st.selectbox(
                "Reading Type",
                options=["General", "Relationship", "Career", "Health", "Wealth", "Dasha", "Annual"]
            )

        with opt_col2:
            current_year = datetime.now().year
            year_input = current_year
            dasha_lord = None

            if reading_type == "Annual":
                year_input = st.number_input(
                    "Year",
                    min_value=current_year - 10,
                    max_value=current_year + 10,
                    value=current_year,
                    key="annual_year"
                )
            elif reading_type == "Dasha":
                dasha_lord = st.selectbox(
                    "Dasha Lord",
                    options=["Auto-detect", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
                    key="dasha_lord_select"
                )
            else:
                st.markdown("<div style='height: 76px'></div>", unsafe_allow_html=True)

        with opt_col3:
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            get_reading_disabled = st.session_state.pdf_content is None
            get_reading = st.button("✨ Get Reading", use_container_width=True, disabled=get_reading_disabled)

        # Chat input for follow-up questions (always visible when PDF loaded)
        if st.session_state.pdf_content:
            st.markdown("**Ask a follow-up question**")
            input_col1, input_col2 = st.columns([4, 1])
            with input_col1:
                user_input = st.text_input(
                    "Question",
                    placeholder="Ask about your chart...",
                    label_visibility="collapsed",
                    key="chat_input"
                )
            with input_col2:
                send_clicked = st.button("Send", use_container_width=True, type="primary")

        st.markdown("---")

        # Response area
        if st.session_state.pdf_content:
            # Handle "Get Reading" button with streaming
            if get_reading:
                category = reading_type.lower()
                user_msg = f"Give me a {reading_type} reading" + (f" for {year_input}" if reading_type == "Annual" else "")

                # Clear previous and store new query
                st.session_state.last_query = user_msg
                st.session_state.last_response = None

                with st.chat_message("user"):
                    st.markdown(user_msg)

                with st.chat_message("assistant"):
                    try:
                        agent = AstrologyAgent(
                            st.session_state.api_key,
                            model=st.session_state.gemini_model
                        )
                        year = year_input if reading_type == "Annual" else None
                        dasha = dasha_lord if reading_type == "Dasha" else None

                        with st.spinner("Generating reading..."):
                            response = st.write_stream(
                                agent.stream_reading(
                                    category=category,
                                    chart_content=st.session_state.pdf_content,
                                    year=year,
                                    dasha_lord=dasha
                                )
                            )
                        st.session_state.last_response = response
                    except Exception as e:
                        st.error(str(e))

            # Handle chat input with streaming
            elif send_clicked and user_input:
                # Clear previous and store new query
                st.session_state.last_query = user_input
                st.session_state.last_response = None

                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.write_stream(stream_chat_response(user_input))
                    st.session_state.last_response = response

            # Display last response (if exists and not currently streaming)
            elif st.session_state.get("last_response"):
                with st.chat_message("user"):
                    st.markdown(st.session_state.last_query)
                with st.chat_message("assistant"):
                    st.markdown(st.session_state.last_response)

            # Welcome message when no response yet
            elif not st.session_state.get("last_response"):
                st.markdown("""
                    <div class="welcome-card">
                        <div class="welcome-icon">🌟</div>
                        <p class="welcome-title">Chart Ready</p>
                        <p class="welcome-text">Select a reading type above, or ask a question.</p>
                    </div>
                """, unsafe_allow_html=True)

        else:
            pass  # Upload instructions shown above


def main():
    """Main application entry point."""
    if not st.session_state.api_key_valid:
        show_landing_page()
    else:
        show_main_app()


if __name__ == "__main__":
    main()
