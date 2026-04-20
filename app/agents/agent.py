"""Browser agent implementation."""
import logging
from typing import Optional
from browser_use import Agent, ChatGoogleGenerativeAI, AgentHistoryList

from app.core.config import Config

logger = logging.getLogger(__name__)


class BrowserAgent:
    """AI-powered browser automation agent."""
    
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the browser agent.
        
        Args:
            model: Gemini model name (defaults to Config.GEMINI_MODEL)
            api_key: Gemini API key (defaults to Config.GEMINI_API_KEY)
        """
        Config.validate()
        
        self.model = model or Config.GEMINI_MODEL
        self.api_key = api_key or Config.GEMINI_API_KEY
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key
        )
        
        logger.info(f"Browser agent initialized with model: {self.model}")
    
    async def execute(self, task: str) -> AgentHistoryList:
        """
        Execute a browser automation task.
        
        Args:
            task: Natural language description of the task to perform
            
        Returns:
            AgentHistoryList with execution history
        """
        logger.info(f"Executing task: {task[:100]}...")
        
        agent = Agent(task=task, llm=self.llm)
        history = await agent.run()
        
        logger.info("Task execution completed")
        return history
