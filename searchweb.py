from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from typing import List, Dict  

load_dotenv()
PORT = os.getenv("PORT", 10000)

tavily_client = TavilyClient(os.environ["TAVILY_API_KEY"])

mcp = FastMCP(name="SearchWeb", stateless_http=True)

@mcp.tool(description="A tool to search the web")
async def search_web( query:str ) -> List[Dict]:
    """
    Use the tool to search the web for information using tavily api

    Args:
        query: The search query

    Returns:
        The search results.
    """
    try:
        response = tavily_client.search(query)
        return response["results"]
    except:
        return "No results found"
    
if __name__ == "__main__":
#    mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")