
import asyncio
import json

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    # Connect to the MCP server
    client = MultiServerMCPClient(
        {
            "research_server": {
                "transport": "sse",
                "url": "http://127.0.0.1:8000/sse",
            }
        }
    )

    # Discover available tools
    tools = await client.get_tools()

    # Find the tools by name
    search_tool = next(
        tool for tool in tools if tool.name == "search_web"
    )
    read_tool = next(
        tool for tool in tools if tool.name == "read_page"
    )
    save_tool = next(
        tool for tool in tools if tool.name == "save_search"
    )

    # Search the web
    result = await search_tool.ainvoke(
        {"query": "latest AI agent development"}
    )

    # Convert the returned JSON text into Python data
    search_results = json.loads(result[0]["text"])

    if not search_results:
        print("No search results found.")
        return

    # Get the first result's URL
    url = search_results[0]["url"]
    print("URL:", url)

    # Read the webpage
    page_result = await read_tool.ainvoke({"url": url})
    page_text = page_result[0]["text"]

    # Save the extracted webpage text
    save_result = await save_tool.ainvoke(
        {
            "title": "AI_Agent_Research_Page",
            "content": page_text,
        }
    )

    print(save_result)


if __name__ == "__main__":
    asyncio.run(main())
