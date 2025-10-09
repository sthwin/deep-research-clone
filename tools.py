import os
import re

from firecrawl import FirecrawlApp, ScrapeOptions


def web_search_tool(query: str):
    """
    Web Search Tool
    Args:
        query: str
            The query to search the web for
    Returns:
        A list of search results with the website content in markdown format
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=1,
        scrape_options=ScrapeOptions(
            formats=["markdown"],
        ),
    )

    if not response.success:
        return "Error using tool: " + response.error

    cleaned_chunks = []

    for result in response.data:

        title = result["title"]
        url = result["url"]
        markdown = result["markdown"]

        cleaned = re.sub(r"\\+|\n+", "", markdown).strip()
        cleaned = cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

        cleaned_chunk = {"title": title, "url": url, "markdown": cleaned}

        cleaned_chunks.append(cleaned_chunk)

    return cleaned_chunks


def save_report_to_md(content: str) -> str:
    """Save report content to report.md file."""
    with open("report.md", "w") as f:
        f.write(content)
    return "report.md"
