from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
from bs4 import BeautifulSoup 
from typing import List, Dict  

load_dotenv()

USER_AGENT = "docs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs"
}

async def search_docs(query: str) -> Dict | None:
    payload = json.dumps({"q": query, "num": 2})
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.getenv("SERPER_API_KEY")
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SERPER_URL, headers=headers, data=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}
        
async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        except httpx.TimeoutException:
            return "Timeout error"
        
#mcp = FastMCP("search-docs", host="0.0.0.0", port=8001 )
mcp = FastMCP(name="SearchLib", stateless_http=True)

@mcp.tool(description="A tool to search the library")
async def search_lib(query:str, library:str):
    """
    Search the docs for a given query and library
    Supports langchain, openai, and llama-index

    Args:
        query: The query to search for (e.g. "Chroma DB")
        library: The library to search in (e.g. "langchain")
    
    Returns:
        Text from the documentation
    """
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported by this tool")
    
    query = f"site:{docs_urls[library]} {query}"
    results = await search_docs(query)
    if len(results["organic"]) == 0:
        return "No result found"
    
    text = ""
    for result in results["organic"]:
        text += await fetch_url(result["link"])
    return text
'''
if __name__ == "__main__":
#    mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")
'''