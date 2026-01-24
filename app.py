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
        background: var(--background);
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

    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 8px !important;
        border: 1.5px solid var(--border) !important;
        font-size: 0.9rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.25rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }

    .stButton > button:disabled {
        background: var(--border) !important;
        transform: none !important;
        box-shadow: none !important;
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
    }

    /* User message */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
        background: var(--primary-bg) !important;
        border-color: var(--primary-light) !important;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 8px !important;
    }

    .stChatInput > div {
        border-radius: 8px !important;
        border: 1.5px solid var(--border) !important;
    }

    .stChatInput > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }

    /* File uploader compact */
    [data-testid="stFileUploader"] {
        background: var(--background) !important;
        border-radius: 8px !important;
        border: 2px dashed var(--border) !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 0.5rem !important;
    }

    /* Success badge */
    .success-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        background: #ECFDF5;
        color: #059669;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
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
        justify-content: center;
        min-height: 80vh;
        text-align: center;
        padding: 1rem;
    }

    .landing-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 2rem;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-light);
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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None


def show_landing_page():
    """Display the landing page with API key input."""

    st.markdown("""
        <div class="landing-container">
            <div style="font-size: 4rem; margin-bottom: 1rem;">✨</div>
            <h1 style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">
                <span style="background: linear-gradient(135deg, #4F46E5 0%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Vedic Astrology Agent</span>
            </h1>
            <p style="color: #6B7280; margin-bottom: 2rem;">AI-powered birth chart readings</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="landing-card">', unsafe_allow_html=True)
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
                <a href="https://aistudio.google.com/apikey" target="_blank" style="color: #4F46E5;">Get a free API key</a>
            </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def get_chat_response(user_message: str) -> str:
    """Get response from the astrology agent for chat."""
    agent = AstrologyAgent(
        st.session_state.api_key,
        model=st.session_state.gemini_model
    )

    # Build context from chat history
    history_context = ""
    for msg in st.session_state.chat_history[-6:]:  # Last 6 messages for context
        role = "User" if msg["role"] == "user" else "Astrologer"
        history_context += f"{role}: {msg['content']}\n\n"

    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""**ROLE:** You are an expert Vedic Astrologer having a conversation about the user's birth chart.

**TODAY'S DATE:** {today}

**CHART DATA:**
{st.session_state.pdf_content}

**CONVERSATION HISTORY:**
{history_context}

**USER'S QUESTION:** {user_message}

**INSTRUCTIONS:**
- Answer based strictly on the chart data provided
- Be conversational but precise
- Reference specific planetary positions when relevant
- Keep responses focused and not too long unless detail is requested
- Use today's date to determine current dasha periods"""

    try:
        from google.genai import types
        response = agent.client.models.generate_content(
            model=agent.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=2048,
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def show_main_app():
    """Display the main application with chat interface."""

    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### ✨ Vedic Astrology Agent")
    with col3:
        if st.button("🔄 New Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Config panel
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "Birth Chart PDF",
                type=["pdf"],
                label_visibility="collapsed"
            )

            if uploaded_file:
                if uploaded_file.name != st.session_state.pdf_name:
                    with st.spinner("Processing..."):
                        try:
                            content = extract_text_from_pdf(uploaded_file)
                            st.session_state.pdf_content = content
                            st.session_state.pdf_name = uploaded_file.name
                            st.session_state.chat_history = []  # Clear chat on new upload
                        except ValueError as e:
                            st.error(str(e))

                if st.session_state.pdf_content:
                    st.markdown(f'<span class="success-badge">✓ {uploaded_file.name}</span>', unsafe_allow_html=True)

        with col2:
            reading_type = st.selectbox(
                "Reading Type",
                options=["General", "Relationship", "Career", "Health", "Wealth", "Dasha", "Annual"],
                label_visibility="visible"
            )

        with col3:
            # Conditional inputs
            if reading_type == "Annual":
                current_year = datetime.now().year
                year_input = st.number_input(
                    "Year",
                    min_value=current_year - 10,
                    max_value=current_year + 10,
                    value=current_year,
                    label_visibility="visible"
                )
            elif reading_type == "Dasha":
                dasha_lord = st.selectbox(
                    "Dasha Lord",
                    options=["Auto-detect", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
                    label_visibility="visible"
                )
            else:
                st.markdown("<div style='height: 52px'></div>", unsafe_allow_html=True)

        with col4:
            get_reading_disabled = st.session_state.pdf_content is None
            if st.button("✨ Get Reading", use_container_width=True, disabled=get_reading_disabled):
                if st.session_state.pdf_content:
                    category = reading_type.lower()

                    with st.spinner(f"Generating {reading_type} reading..."):
                        try:
                            agent = AstrologyAgent(
                                st.session_state.api_key,
                                model=st.session_state.gemini_model
                            )

                            year = year_input if reading_type == "Annual" else None
                            dasha = dasha_lord if reading_type == "Dasha" else None

                            reading = agent.get_reading(
                                category=category,
                                chart_content=st.session_state.pdf_content,
                                year=year,
                                dasha_lord=dasha
                            )

                            # Add to chat history
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": f"Give me a {reading_type} reading" + (f" for {year_input}" if reading_type == "Annual" else "")
                            })
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": reading
                            })
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

    st.markdown("---")

    # Chat interface
    if st.session_state.pdf_content:
        # Display chat messages
        chat_container = st.container()

        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                    <div class="welcome-card">
                        <div class="welcome-icon">🌟</div>
                        <p class="welcome-title">Chart Ready</p>
                        <p class="welcome-text">Select a reading type above, or ask any question about your chart below.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

        # Chat input
        if user_input := st.chat_input("Ask a question about your chart..."):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            # Get response
            with st.spinner("Thinking..."):
                response = get_chat_response(user_input)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

            st.rerun()

    else:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-icon">📄</div>
                <p class="welcome-title">Upload Your Birth Chart</p>
                <p class="welcome-text">Upload a PDF from Jagannatha Hora, Parashara's Light, Astro-Sage, or any Vedic astrology software.</p>
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
