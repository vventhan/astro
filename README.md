# Vedic Astrology Agent

A Streamlit-based web application that provides personalized Vedic astrology readings powered by Google Gemini AI.

## Features

- **PDF Upload**: Upload your birth chart PDF (from Jagannatha Hora, Parashara's Light, etc.)
- **Multiple Reading Types**:
  - General Overview
  - Relationships
  - Career
  - Health
  - Wealth
  - Annual Predictions (for any year)
- **BYOK**: Bring your own Gemini API key (free tier available)

## Setup

### Prerequisites

- Python 3.9+
- A Google Gemini API key ([Get one free](https://ai.google.dev))

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd astro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your Gemini API key
2. Upload a PDF containing your Vedic birth chart calculations
3. Select a reading type (General, Career, Relationships, etc.)
4. For Annual readings, also enter the year
5. Click "Get Reading" to receive your personalized prediction

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy (no secrets needed - users provide their own API key)

### Embedding in Google Sites

Use the Streamlit Cloud URL in an iframe embed on your Google Site.

## Tech Stack

- **Frontend**: Streamlit
- **PDF Parsing**: PyMuPDF
- **LLM**: Google Gemini
- **Language**: Python 3.9+

## License

MIT
