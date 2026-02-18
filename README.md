# AI Browser Agent

An intelligent browser automation system powered by AI that can perform complex web tasks autonomously using natural language instructions.

## Features

- **Natural Language Tasks**: Describe tasks in plain English
- **Intelligent Navigation**: AI-powered decision making for web interactions
- **Multi-Step Workflows**: Handle complex, multi-page automation tasks
- **Form Filling**: Automatically fill and submit web forms
- **Data Extraction**: Extract structured information from web pages
- **Error Handling**: Robust error handling and recovery mechanisms
- **Execution History**: Detailed logging and history tracking

## Architecture

The application follows a modular architecture:

- **Agent**: Core browser automation engine using LLM for decision making
- **Tasks**: Reusable task templates and definitions
- **Configuration**: Environment-based configuration management
- **Utilities**: Helper functions for logging and history management

## Installation

### Prerequisites

- Python 3.11 or higher
- Gemini API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-browser-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium --with-deps
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

## Usage

### Command Line Interface

Run a custom task:
```bash
python -m app.main "Search Google for 'Python web scraping' and tell me the top 3 results"
```

Run a predefined example:
```bash
python -m app.main --example search
python -m app.main --example form
python -m app.main --example extract
python -m app.main --example research
```

With verbose logging:
```bash
python -m app.main --example search --verbose
```

With detailed summary:
```bash
python -m app.main --example search --summary
```

### Programmatic Usage

```python
import asyncio
from app.agent import BrowserAgent
from app.tasks import TaskTemplates

async def main():
    agent = BrowserAgent()
    
    task = TaskTemplates.basic_search("Python web frameworks", top_n=5)
    await agent.execute(task)

if __name__ == "__main__":
    asyncio.run(main())
```

### Task Templates

Use predefined templates for common scenarios:

```python
from app.tasks import TaskTemplates

# Basic search
task = TaskTemplates.basic_search("query", top_n=3)

# Form filling
task = TaskTemplates.form_filling(
    url="https://example.com/form",
    fields={"name": "John", "email": "john@example.com"}
)

# Data extraction
task = TaskTemplates.data_extraction(
    url="https://example.com/data",
    extraction_instructions="Extract product names and prices"
)

# Multi-step research
task = TaskTemplates.multi_step_research(
    search_query="Python async frameworks",
    research_goals="Compare top 3 frameworks"
)
```

## Docker Usage

### Build the image:
```bash
docker build -t ai-browser-agent .
```

### Run the container:
```bash
docker run --rm \
  --env-file .env \
  ai-browser-agent \
  python -m app.main --example search
```

### Interactive mode:
```bash
docker run -it --rm \
  --env-file .env \
  ai-browser-agent \
  python -m app.main "Your task here"
```

## Example CLI Usage

```bash
# Basic search task
python -m app.main "Find the latest news about AI"

# Form submission
python -m app.main "Go to https://httpbin.org/forms/post and fill out the form with name=John, email=john@example.com, then submit"

# Data extraction
python -m app.main "Extract all product names and prices from https://example.com/products"

# Multi-step research
python -m app.main "Research the top 3 Python web frameworks, visit each official site, and compare their features"
```

## Configuration

Configuration is managed through environment variables:

- `GEMINI_API_KEY`: Your Gemini API key (required)
- `GEMINI_MODEL`: Model to use (default: `gemini-pro`)

## Project Structure

```
ai-browser-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── agent.py         # Browser agent implementation
│   ├── config.py        # Configuration management
│   ├── tasks.py         # Task templates and examples
│   └── utils.py         # Utility functions
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## License

MIT License
