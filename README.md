# Multi-Tool Assistant (LangChain + LangGraph)

A chatbot where one LLM decides on its own which tool to call (or several, one after another) based on your question. Built to revise the **tool calling** concept in LangChain.

## Tools

| Tool | What it does |
|------|--------------|
| `web_search` | Searches the web for latest news and real-time info (Tavily) |
| `weather_tool` | Gets the current weather of a city (Open-Meteo, no API key needed) |
| `calculator` | Solves math expressions safely (numexpr) |

## Concepts Covered

- Defining tools with `@tool`, docstrings and type hints
- Binding tools to an LLM with `bind_tools`
- Reading `tool_calls` from the model response
- Executing tools with `ToolNode`
- LangGraph state, nodes, conditional edges and loops
- Error handling inside tools

## How It Works

```
START -> query_node -> llm -> (tool call?) -> tools -> llm -> ... -> query_node
                         |
                         +-> no tool call -> query_node (next question)
```

Type `exit` or `quit` to stop.

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   git clone https://github.com/Ishaan0901/tools_revision.git
   cd tools_revision
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your keys:
   - `GROQ_API_KEY` from console.groq.com
   - `TAVILY_API_KEY` from tavily.com
4. Run:
   ```bash
   python backend/main.py
   ```

## Example

```
Human: what is 25*4?
AI: 25 * 4 = 100

Human: weather in Delhi and multiply the temperature by 2
AI: ...
```

## Tech Stack

Python, LangChain, LangGraph, Groq (`openai/gpt-oss-20b`), Tavily, Open-Meteo
