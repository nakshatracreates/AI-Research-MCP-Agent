# AI Research MCP Agent

An AI-powered research assistant built using Python, MCP, and LangChain. It searches the web, reads relevant webpages, summarizes findings, and saves research reports as Markdown files.

## Features
- Web search using Tavily
- Read webpage content
- Save research reports locally
- AI agent powered by OpenAI GPT-5-mini
- MCP tools integration using FastMCP

## Tech Stack
- Python
- FastMCP and MCP
- LangChain
- OpenAI GPT-5-mini
- Tavily Search API
- Requests and BeautifulSoup

## Project Structure
- `server.py` — Defines MCP tools
- `agent.py` — Runs the AI research agent
- `client.py` — Demonstrates manual MCP tool calls
- `research/` — Stores generated reports

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Create a `.env` file with your own API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

5. Start the MCP server in one terminal:

```bash
python server.py
```

6. Run the agent in a second terminal:

```bash
python agent.py
```

The
