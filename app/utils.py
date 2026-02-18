"""Utility functions for the browser agent."""
import logging
from typing import Optional, List, Dict, Any
from browser_use import AgentHistoryList


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def format_history_summary(history: AgentHistoryList) -> Dict[str, Any]:
    """Extract and format summary information from agent history."""
    return {
        "urls": history.urls(),
        "screenshot_paths": history.screenshot_paths(),
        "action_names": history.action_names(),
        "extracted_content": history.extracted_content(),
        "errors": history.errors(),
        "number_of_steps": history.number_of_steps(),
        "total_duration_seconds": history.total_duration_seconds(),
        "is_done": history.is_done(),
        "is_successful": history.is_successful(),
        "has_errors": history.has_errors(),
        "final_result": history.final_result(),
    }


def print_history_summary(history: AgentHistoryList) -> None:
    """Print a formatted summary of agent execution history."""
    summary = format_history_summary(history)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Agent Execution Summary")
    logger.info("=" * 60)
    logger.info(f"Steps executed: {summary['number_of_steps']}")
    logger.info(f"Total duration: {summary['total_duration_seconds']:.2f} seconds")
    logger.info(f"Completed: {summary['is_done']}")
    logger.info(f"Successful: {summary['is_successful']}")
    logger.info(f"Has errors: {summary['has_errors']}")
    
    if summary['urls']:
        logger.info(f"\nVisited URLs ({len(summary['urls'])}):")
        for i, url in enumerate(summary['urls'], 1):
            logger.info(f"  {i}. {url}")
    
    if summary['action_names']:
        logger.info(f"\nActions executed ({len(summary['action_names'])}):")
        for i, action in enumerate(summary['action_names'], 1):
            logger.info(f"  {i}. {action}")
    
    if summary['errors']:
        error_count = sum(1 for e in summary['errors'] if e is not None)
        if error_count > 0:
            logger.warning(f"\nErrors encountered: {error_count}")
            for i, error in enumerate(summary['errors'], 1):
                if error:
                    logger.warning(f"  Step {i}: {error}")
    
    if summary['final_result']:
        logger.info(f"\nFinal Result:\n{summary['final_result']}")
    
    logger.info("=" * 60)
