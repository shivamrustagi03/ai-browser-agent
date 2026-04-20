# AI Browser Agent - Streamlit UI

A clean, professional Streamlit interface for your AI Browser Agent.

## Features

✨ **Clean Interface**
- Modern, responsive design
- Easy-to-use task input
- Example tasks in sidebar

🔄 **Real-time Updates**
- Loading spinners during execution
- Live execution logs
- Clear success/error messages

📊 **Rich Output Display**
- Formatted final results
- Expandable execution logs
- Download history option

## Installation

1. **Install Streamlit dependencies:**
```bash
pip install -r requirements_streamlit.txt
```

2. **Ensure your main project dependencies are installed:**
```bash
pip install -r requirements.txt  # Your existing requirements
```

## Running the UI

From your project root directory, run:

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **Enter a task** in the text area (or click an example from the sidebar)
2. **Click "Run Agent"** to start execution
3. **View logs** in the expandable section (optional)
4. **See results** in the formatted output section

## Example Tasks

Try these example tasks:

- **Job Search**: "Find top 5 AI jobs in Hyderabad on LinkedIn"
- **Data Extraction**: "Go to quotes.toscrape.com and extract the first 5 quotes"
- **Research**: "Search for latest Python web scraping libraries and summarize top 3"
- **Weather**: "Find current weather in New York City"

## Project Structure

```
streamlit_app.py           # Main Streamlit UI
requirements_streamlit.txt # Streamlit dependencies
app/
  agents/agent.py         # Your existing agent logic
  main.py                 # Your existing CLI
```

## Key Features Explained

### Async Support
The UI handles async agent execution properly:
```python
def run_agent_sync(task: str):
    agent = BrowserAgent()
    return asyncio.run(agent.execute(task))
```

### Log Capture
A custom `StreamlitLogHandler` captures all logs during execution and displays them in a clean terminal-style box.

### Result Extraction
The `extract_final_result()` function intelligently parses the `AgentHistoryList` to show the most relevant output to users.

## Troubleshooting

**Import errors**: Make sure you're running from the project root and all dependencies are installed.

**Agent execution fails**: Check your `.env` file has the correct `GEMINI_API_KEY` configured.

**Logs don't appear**: Ensure logging is properly configured in your agent modules.

## Customization

### Change Theme
Edit `.streamlit/config.toml` (create if it doesn't exist):
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Modify Examples
Edit the `examples` dictionary in `streamlit_app.py`:
```python
examples = {
    "Your Task": "Task description here",
    # Add more examples
}
```

## License

Same as the main project.
