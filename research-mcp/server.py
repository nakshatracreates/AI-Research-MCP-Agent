
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastmcp import FastMCP
from tavily import TavilyClient

load_dotenv()

# Initialize the MCP server
mcp = FastMCP("Research MCP Server")

# Initialize Tavily using the API key in .env
api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise ValueError("TAVILY_API_KEY is missing from .env")

tavily = TavilyClient(api_key=api_key)


@mcp.tool()
def search_web(query: str):
    """Search the web and return relevant results."""
    response = tavily.search(
        query=query,
        max_results=5,
    )
    return response["results"]


@mcp.tool()
def read_page(url: str):
    """Fetch a public webpage and return its readable text."""
    parsed_url = urlparse(url)

    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.hostname
        or parsed_url.username
        or parsed_url.password
    ):
        raise ValueError("A valid HTTP or HTTPS URL is required.")

    # Prevent requests to local and private network addresses.
    import ipaddress
    import socket

    try:
        addresses = socket.getaddrinfo(
            parsed_url.hostname, None, type=socket.SOCK_STREAM
        )
        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                raise ValueError("Private or non-public addresses are not allowed.")
    except socket.gaierror as exc:
        raise ValueError("Could not resolve the webpage hostname.") from exc

    response = requests.get(
        url,
        timeout=10,
        allow_redirects=False,
        headers={"User-Agent": "AI-Research-MCP-Agent/1.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)


@mcp.tool()
def save_search(title: str, content: str):
    """Save research content as a Markdown file."""

    safe_title = "".join(
        char for char in title
        if char.isalnum() or char in ("_", "-")
    )

    if not safe_title:
        raise ValueError("Title must contain letters or numbers.")

    research_dir = "research"
    os.makedirs(research_dir, exist_ok=True)

    file_path = os.path.join(
        research_dir, f"{safe_title}.md"
    )

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Research saved to {file_path}"


if __name__ == "__main__":
    mcp.run(transport="sse")

