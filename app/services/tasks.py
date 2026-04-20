"""Predefined task templates for common browser automation scenarios."""
from typing import Dict, Any


class TaskTemplates:
    """Collection of reusable task definitions."""
    
    @staticmethod
    def basic_search(query: str, top_n: int = 3) -> str:
        """
        Create a task for searching Google and extracting top results.
        
        Args:
            query: Search query string
            top_n: Number of top results to extract
            
        Returns:
            Task description string
        """
        return f"Search Google for '{query}' and tell me the top {top_n} results"
    
    @staticmethod
    def form_filling(
        url: str,
        fields: Dict[str, str],
        submit: bool = True
    ) -> str:
        """
        Create a task for filling out a web form.
        
        Args:
            url: URL of the form page
            fields: Dictionary mapping field names to values
            submit: Whether to submit the form after filling
            
        Returns:
            Task description string
        """
        field_list = "\n".join([f"- {k}: {v}" for k, v in fields.items()])
        submit_text = "Then submit the form and tell me what response you get." if submit else ""
        
        return f"""Go to {url} and fill out the form with:
{field_list}
{submit_text}"""
    
    @staticmethod
    def data_extraction(
        url: str,
        extraction_instructions: str
    ) -> str:
        """
        Create a task for extracting structured data from a webpage.
        
        Args:
            url: URL to extract data from
            extraction_instructions: Description of what data to extract
            
        Returns:
            Task description string
        """
        return f"""Go to {url} and extract the following information:
{extraction_instructions}
Present the information in a clear, structured format."""
    
    @staticmethod
    def multi_step_research(
        search_query: str,
        research_goals: str,
        output_format: str = "summary"
    ) -> str:
        """
        Create a task for multi-step research across multiple pages.
        
        Args:
            search_query: Initial search query
            research_goals: Description of research objectives
            output_format: Desired output format (summary, comparison, etc.)
            
        Returns:
            Task description string
        """
        return f"""I want you to research: {search_query}

Here's what I need:
{research_goals}

Present your findings in a {output_format} format."""


class ExampleTasks:
    """Example task definitions for common use cases."""
    
    SEARCH_BROWSER_AUTOMATION = (
        "Search Google for 'what is browser automation' "
        "and tell me the top 3 results"
    )
    
    FORM_FILLING_HTTPBIN = """Go to https://httpbin.org/forms/post and fill out the contact form with:
- Customer name: John Doe
- Telephone: 555-123-4567
- Email: john.doe@example.com
- Size: Medium
- Topping: cheese
- Delivery time: now
- Comments: This is a test form submission
Then submit the form and tell me what response you get."""
    
    EXTRACT_QUOTES = """Go to https://quotes.toscrape.com/ and extract the following information:
- The first 5 quotes on the page
- The author of each quote
- The tags associated with each quote
Present the information in a clear, structured format like:
Quote 1: "[quote text]" - Author: [author name] - Tags: [tag1, tag2, ...]
Quote 2: "[quote text]" - Author: [author name] - Tags: [tag1, tag2, ...]
etc."""
    
    RESEARCH_PYTHON_SCRAPING = """I want you to research Python web scraping libraries. Here's what I need:
1. First, search Google for "best Python web scraping libraries 2025"
2. Find a reputable article or blog post about this topic
3. From that article, extract the top 3 recommended libraries
4. For each library, visit its official website or GitHub page
5. Extract key information about each library:
- Name
- Brief description
- Main features or advantages
- GitHub stars (if available)
Present your findings in a summary format comparing the three libraries."""
