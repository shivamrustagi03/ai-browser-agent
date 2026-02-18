"""Main entry point for the browser agent application."""
import asyncio
import argparse
import logging
import sys

from app.agent import BrowserAgent
from app.config import Config
from app.tasks import ExampleTasks, TaskTemplates
from app.utils import setup_logging, print_history_summary


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Browser Agent - Automated web task execution"
    )
    
    parser.add_argument(
        "task",
        nargs="?",
        help="Task description in natural language"
    )
    
    parser.add_argument(
        "--example",
        choices=["search", "form", "extract", "research"],
        help="Run a predefined example task"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help=f"Gemini model to use (default: {Config.GEMINI_MODEL})"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print detailed execution summary"
    )
    
    return parser.parse_args()


def get_task_from_args(args: argparse.Namespace) -> str:
    """Determine the task to execute based on arguments."""
    if args.example:
        examples = {
            "search": ExampleTasks.SEARCH_BROWSER_AUTOMATION,
            "form": ExampleTasks.FORM_FILLING_HTTPBIN,
            "extract": ExampleTasks.EXTRACT_QUOTES,
            "research": ExampleTasks.RESEARCH_PYTHON_SCRAPING,
        }
        return examples[args.example]
    
    if args.task:
        return args.task
    
    parser = argparse.ArgumentParser()
    parser.error("Either provide a task description or use --example option")


async def main() -> None:
    """Main application entry point."""
    args = parse_arguments()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    logger = logging.getLogger(__name__)
    
    try:
        task = get_task_from_args(args)
        
        logger.info("Initializing browser agent...")
        agent_wrapper = BrowserAgent(model=args.model)
        
        logger.info("Starting task execution...")
        history = await agent_wrapper.execute(task)
        
        if args.summary:
            print_history_summary(history)
        else:
            logger.info("Task execution completed successfully")
            
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
