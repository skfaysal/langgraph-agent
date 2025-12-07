# Omni Assistant

A conversational AI assistant built with LangGraph and Streamlit.

## Overview

This project provides a chatbot interface that uses LangGraph for managing conversation flows and Streamlit for the user interface. The application consists of two main components:

1. **LangGraph Server** - Backend service that handles the AI agent logic
2. **Streamlit Frontend** - Web-based chat interface

## Prerequisites

- Python 3.10 or higher
- UV package manager (or Poetry)
- Required dependencies installed

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd omni-assistant
```

2. Install dependencies:
```bash
uv sync
```

Or if using Poetry:
```bash
poetry install
```

3. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

4. Configure LLM settings:
Edit `LLM_CONFIG.yaml` to enable your preferred LLM provider:
```yaml
llms:
  anthropic:
    enabled: true  # Set to true to use Anthropic
    model_name: claude-3-7-sonnet-20250219
    max_tokens: 512
    temperature: 0
  openai:
    enabled: false  # Set to true to use OpenAI
    model_name: gpt-4o
    max_tokens: 512
    temperature: 0
```

## Running the Application

### Step 1: Start the LangGraph Server

The LangGraph server runs the AI agent and exposes it via HTTP API.

1. Navigate to the directory containing `langgraph.json`:
```bash
cd omniassistant
```

2. Start the LangGraph development server:
```bash
langgraph dev
```

The server will start and be available at:
```
http://localhost:2024
```

You should see output indicating the server is running. The API documentation will be available at `http://localhost:2024/docs`.

**Keep this terminal window open** - the server needs to run continuously.

### Step 2: Start the Streamlit Frontend

In a **new terminal window**, start the Streamlit UI.

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

The Streamlit interface will open automatically in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, navigate to the URL shown in the terminal.

## Usage

1. Once both servers are running, open the Streamlit interface in your browser
2. You'll see a chat interface with a sidebar showing conversations
3. Type your message in the chat input at the bottom
4. The assistant will respond in real-time
5. Use the sidebar to:
   - Create new conversations (➕ New Conversation button)
   - Switch between existing conversations (click on thread IDs)
   - Delete conversations (🗑️ button)

## Project Structure

```
omni-assistant/
├── omniassistant/          # Main package
│   ├── langgraph.json      # LangGraph configuration
│   ├── graph.py            # Graph definition
│   ├── state.py            # State management
│   ├── nodes/              # Graph nodes
│   └── chains/             # LLM chains
├── frontend/               # Streamlit UI
│   ├── app.py             # Main Streamlit app
│   └── api.py             # LangGraph client functions
├── LLM_CONFIG.yaml        # LLM configuration
└── .env                   # Environment variables (not in git)
```