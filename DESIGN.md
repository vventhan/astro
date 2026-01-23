# Vedic Astrology Agent - Design Document

## Overview

A Streamlit-based web application that provides Vedic astrology readings using an AI agent. The app accepts a PDF containing astrological calculations (birth chart, planetary positions, dashas, etc.) and provides personalized predictions across various life domains.

**Key Design Decision**: Users provide their own Google Gemini API key, enabling free public access with zero cost to the app owner.

---

## Features

### Core Functionality

1. **PDF Upload & Parsing**
   - Accept PDF files containing Vedic astrology calculations
   - Extract text content including planetary positions, house placements, dashas, etc.
   - Cache parsed content for the session

2. **Prediction Categories**
   - **General Overview**: Overall life path, strengths, challenges
   - **Relationships**: Marriage, partnerships, family dynamics
   - **Career**: Professional growth, suitable fields, timing for changes
   - **Health**: Physical constitution, potential health concerns, remedies
   - **Wealth**: Financial prospects, investment timing, sources of income
   - **Annual Reading**: Year-specific predictions based on transits and dashas

3. **BYOK (Bring Your Own Key)**
   - Users provide their own Gemini API key
   - No cost to app owner
   - Key stored only in session memory

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────────────────────┐   │
│  │  API Key Input  │  │       Prediction Panel          │   │
│  │  + PDF Upload   │  │     (Category Selection)        │   │
│  └─────────────────┘  └─────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      Session State                           │
│         (api_key, pdf_content, current_reading)              │
├─────────────────────────────────────────────────────────────┤
│                     Business Logic                           │
│  ┌─────────────────┐  ┌─────────────────────────────────┐   │
│  │   PDF Parser    │  │       Astrology Agent           │   │
│  │     Module      │  │         (Gemini)                │   │
│  └─────────────────┘  └─────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    External Services                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           Google Gemini API (User's Key)                 ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | Streamlit | Rapid prototyping, built-in components |
| PDF Parsing | PyMuPDF (fitz) | Fast, reliable text extraction |
| LLM | Google Gemini | Free tier available, user provides own key |
| Config | python-dotenv | Local development support |

---

## File Structure

```
astro/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── DESIGN.md             # This design document
└── src/
    ├── __init__.py
    ├── pdf_parser.py     # PDF text extraction
    ├── agent.py          # Astrology agent with Gemini
    └── prompts.py        # System prompts for different categories
```

---

## Component Details

### 1. PDF Parser (`src/pdf_parser.py`)

```python
# Responsibilities:
# - Accept uploaded PDF file
# - Extract all text content
# - Return text for agent consumption
```

**Extracted Data Points:**
- Birth details (date, time, place)
- Planetary positions (Rashi chart)
- House placements
- Nakshatra details
- Dasha periods (Vimshottari)
- Divisional charts (if present)

### 2. Astrology Agent (`src/agent.py`)

```python
# Responsibilities:
# - Initialize Gemini client with user's API key
# - Route requests to appropriate prediction category
# - Format responses for display
```

**Agent Behavior:**
- Uses PDF content as context
- Applies Vedic astrology principles
- Provides specific, actionable insights
- Cites planetary positions when making predictions
- For annual readings, considers:
  - Current dasha/antardasha
  - Transit positions for the requested year
  - Annual chart (Varshaphal) principles

### 3. Prompts (`src/prompts.py`)

System prompts tailored for each prediction category:

| Category | Focus Areas |
|----------|-------------|
| General | Life purpose, overall trends, key strengths/challenges |
| Relationships | 7th house, Venus, Jupiter, navamsa analysis |
| Career | 10th house, Saturn, Mercury, Sun analysis |
| Health | 6th house, ascendant lord, Moon, Mars analysis |
| Wealth | 2nd/11th houses, Jupiter, Venus, dhana yogas |
| Annual | Transits, dasha periods, varshaphal for specific year |

---

## User Interface Design

### Screen 1: Landing (No API Key)
```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                   Vedic Astrology Agent                    │
│                                                            │
│   Get personalized Vedic astrology readings powered by AI  │
│                                                            │
│   ┌────────────────────────────────────────────────────┐   │
│   │  Enter your Gemini API Key                         │   │
│   │  ************************************************  │   │
│   └────────────────────────────────────────────────────┘   │
│                                                            │
│   Don't have a key? Get one free at ai.google.dev          │
│                                                            │
│                      [ Get Started ]                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Screen 2: Main Application
```
┌──────────────┬─────────────────────────────────────┐
│   SIDEBAR    │           MAIN CONTENT              │
├──────────────┼─────────────────────────────────────┤
│              │                                     │
│ Upload Your  │  Welcome! Upload your birth chart   │
│ Birth Chart  │  PDF to get started.                │
│              │                                     │
│ [Browse...]  │  ┌─────────────────────────────┐    │
│              │  │                             │    │
│ ───────────  │  │    Drag & Drop PDF Here     │    │
│              │  │    or click to browse       │    │
│ Reading Type │  │                             │    │
│              │  └─────────────────────────────┘    │
│ ○ General    │                                     │
│ ○ Relationship│  Supported formats:                │
│ ○ Career     │  Jagannatha Hora, Parashara's      │
│ ○ Health     │  Light, or any PDF with birth      │
│ ○ Wealth     │  chart calculations.               │
│ ○ Annual     │                                     │
│   Year: [__] │                                     │
│              │                                     │
│ ───────────  │                                     │
│              │                                     │
│ [Get Reading]│                                     │
│              │                                     │
└──────────────┴─────────────────────────────────────┘
```

### Screen 3: Reading Display
```
┌──────────────┬─────────────────────────────────────┐
│   SIDEBAR    │           MAIN CONTENT              │
├──────────────┼─────────────────────────────────────┤
│              │                                     │
│ chart.pdf    │  ## Career Reading                  │
│ ✓ Uploaded   │                                     │
│              │  Based on your birth chart...       │
│ ───────────  │                                     │
│              │  ### 10th House Analysis            │
│ Reading Type │  Your 10th house is ruled by...     │
│              │                                     │
│ ● Career     │  ### Career Strengths               │
│              │  - Strong Saturn placement...       │
│ ───────────  │  - Mercury in 10th gives...         │
│              │                                     │
│ [Get Reading]│  ### Favorable Periods              │
│              │  Current Jupiter transit...         │
│ [Clear]      │                                     │
│              │  ### Recommendations                │
│              │  Consider fields related to...      │
└──────────────┴─────────────────────────────────────┘
```

---

## Security Considerations

1. **User API Key Handling**
   - Stored only in session state (memory)
   - Never logged or persisted to disk
   - Cleared on browser close/refresh
   - Each user responsible for their own key

2. **File Handling**
   - PDF processed in memory only
   - No permanent storage of uploaded files
   - Session-based content caching only

3. **No Server-Side Secrets**
   - No API keys stored on server
   - No environment variables needed for deployment

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid API Key | "Invalid Gemini API key. Please check and try again." |
| API Quota Exceeded | "API quota exceeded. Please check your Gemini account." |
| Invalid PDF | "Unable to extract text. Please upload a valid astrology chart PDF." |
| Empty PDF | "No content found in PDF. Please check the file." |
| API Error | "Service temporarily unavailable. Please try again." |

---

## Gemini API Key Instructions (Shown in App)

1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Sign in with Google account
4. Create a new API key
5. Copy and paste into the app

**Free Tier Limits** (as of 2024):
- 60 requests per minute
- 1 million tokens per month
- More than sufficient for personal use

---

## Future Enhancements (Out of Scope for v1)

- [ ] Chat-style follow-up questions
- [ ] Multiple chart comparison (compatibility)
- [ ] Export readings as PDF
- [ ] Remedial suggestions database
- [ ] Support for multiple LLM providers (OpenAI, Claude)

---

## Development Phases

### Phase 1: Foundation
- Project setup (requirements, .gitignore, README)
- Basic Streamlit app structure
- API key input handling

### Phase 2: Core Features
- PDF upload and parsing
- Gemini agent integration
- All prediction categories

### Phase 3: Polish
- UI refinements
- Error handling
- Deployment to Streamlit Cloud

---

## Approval Checklist

- [ ] Architecture approved
- [ ] UI design approved
- [ ] BYOK approach approved
- [ ] Tech stack approved

**Ready to proceed with implementation?**
