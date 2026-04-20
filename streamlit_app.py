"""Streamlit UI for AI Browser Agent."""
import streamlit as st
import asyncio
import logging
from io import StringIO
from datetime import datetime
from typing import Optional
import sys

# Configure page
st.set_page_config(
    page_title="AI Browser Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .output-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .log-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .success-message {
        color: #28a745;
        font-weight: 600;
    }
    .error-message {
        color: #dc3545;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitLogHandler(logging.Handler):
    """Custom logging handler to capture logs for Streamlit display."""
    
    def __init__(self):
        super().__init__()
        self.log_buffer = StringIO()
        
    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_buffer.write(msg + '\n')
        except Exception:
            self.handleError(record)
    
    def get_logs(self) -> str:
        return self.log_buffer.getvalue()
    
    def clear_logs(self):
        self.log_buffer = StringIO()


def setup_logging() -> StreamlitLogHandler:
    """Setup logging with custom handler for Streamlit."""
    log_handler = StreamlitLogHandler()
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    log_handler.setFormatter(formatter)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    return log_handler


def extract_final_result(history) -> str:
    """
    Extract readable final result from AgentHistoryList.
    
    Args:
        history: AgentHistoryList object from agent execution
        
    Returns:
        Formatted string with the final result
    """
    try:
        if not history or len(history.history) == 0:
            return "No results found."
        
        # Get the last action/result
        last_entry = history.history[-1]
        
        # Extract result based on history structure
        result_parts = []
        
        # Try to get the final result/output
        if hasattr(last_entry, 'result') and last_entry.result:
            result_parts.append(f"**Final Result:**\n{last_entry.result}")
        
        # Check for model output
        if hasattr(last_entry, 'model_output') and last_entry.model_output:
            result_parts.append(f"\n**Output:**\n{last_entry.model_output}")
        
        # Iterate through all history entries to collect important information
        for i, entry in enumerate(history.history):
            if hasattr(entry, 'state') and entry.state:
                if hasattr(entry.state, 'extracted_content') and entry.state.extracted_content:
                    result_parts.append(f"\n**Extracted Content (Step {i+1}):**\n{entry.state.extracted_content}")
        
        if result_parts:
            return "\n\n".join(result_parts)
        else:
            # Fallback: return string representation
            return f"Task completed successfully.\n\n**History Summary:**\n{str(history)}"
            
    except Exception as e:
        return f"Result extraction completed. See logs for details.\n\nError formatting output: {str(e)}"


def run_agent_sync(task: str, log_handler: StreamlitLogHandler) -> tuple[Optional[any], Optional[str]]:
    """
    Synchronous wrapper for async agent execution.
    
    Args:
        task: Task description
        log_handler: Logging handler
        
    Returns:
        Tuple of (history, error_message)
    """
    try:
        # Import here to avoid issues if modules aren't available
        from app.agents.agent import BrowserAgent
        
        log_handler.clear_logs()
        
        # Run async agent execution
        agent = BrowserAgent()
        history = asyncio.run(agent.execute(task))
        
        return history, None
        
    except Exception as e:
        error_msg = f"Error during execution: {str(e)}"
        logging.error(error_msg, exc_info=True)
        return None, error_msg


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🤖 AI Browser Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Automated web task execution powered by AI</div>',
        unsafe_allow_html=True
    )
    
    # Setup logging
    if 'log_handler' not in st.session_state:
        st.session_state.log_handler = setup_logging()
    
    # Sidebar with examples and info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This AI Browser Agent can automate web tasks using natural language instructions.
        Simply describe what you want to do, and the agent will handle it!
        """)
        
        st.header("📝 Example Tasks")
        examples = {
            "Search Jobs": "Find top 5 AI jobs in Hyderabad on LinkedIn",
            "Extract Data": "Go to quotes.toscrape.com and extract the first 5 quotes with their authors",
            "Research": "Search for the latest Python web scraping libraries and summarize the top 3",
            "Weather Check": "Find the current weather in New York City"
        }
        
        for name, task in examples.items():
            if st.button(name, key=f"example_{name}", use_container_width=True):
                st.session_state.task_input = task
    
    # Main input section
    st.header("🎯 Task Input")
    
    # Initialize session state for task input
    if 'task_input' not in st.session_state:
        st.session_state.task_input = ""
    
    task = st.text_area(
        "Describe your task:",
        value=st.session_state.task_input,
        height=100,
        placeholder="Example: Find top 5 AI jobs in Hyderabad on LinkedIn",
        help="Enter a natural language description of the web task you want to automate"
    )
    
    # Update session state
    st.session_state.task_input = task
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        run_button = st.button("▶️ Run Agent", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.task_input = ""
        st.rerun()
    
    # Execution section
    if run_button:
        if not task.strip():
            st.warning("⚠️ Please enter a task description before running the agent.")
        else:
            st.divider()
            
            # Create placeholders for dynamic updates
            status_placeholder = st.empty()
            logs_placeholder = st.empty()
            result_placeholder = st.empty()
            
            # Show loading state
            with status_placeholder:
                st.info("🔄 Initializing agent...")
            
            # Run the agent
            with st.spinner("Agent is working..."):
                history, error = run_agent_sync(task, st.session_state.log_handler)
            
            # Display logs
            logs = st.session_state.log_handler.get_logs()
            if logs:
                with st.expander("📋 Execution Logs", expanded=False):
                    st.markdown(f'<div class="log-box">{logs}</div>', unsafe_allow_html=True)
            
            # Display results
            if error:
                status_placeholder.error(f"❌ Execution Failed")
                result_placeholder.markdown(f'<div class="error-message">{error}</div>', unsafe_allow_html=True)
            else:
                status_placeholder.success("✅ Task Completed Successfully")
                
                # Extract and display final result
                final_result = extract_final_result(history)
                
                with result_placeholder:
                    st.header("📊 Results")
                    st.markdown(f'<div class="output-box">{final_result}</div>', unsafe_allow_html=True)
                    
                    # Download button for full history
                    st.download_button(
                        label="⬇️ Download Full History",
                        data=str(history),
                        file_name=f"agent_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
    
    # Footer
    st.divider()
    st.caption("Built with Streamlit • Powered by Gemini AI")


if __name__ == "__main__":
    main()
