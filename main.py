from typing import Annotated, Dict, Any
import os
from dotenv import load_dotenv
load_dotenv()
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import McpError, ErrorData
from mcp.server.auth.provider import AccessToken
from openai import BaseModel
from pydantic import Field
import re
import json
import requests # Import the requests library for making API calls

# --- Configuration ---
TOKEN = os.environ.get("TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER") # Insert your number {91}{Your number}

# IMPORTANT: Replace this with your actual SerpApi API key
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY", "YOUR_SERPAPI_API_KEY_HERE")

# --- E-commerce Product Recommendation Chatbot with Live Search using SerpApi ---

class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None

class SimpleBearerAuthProvider(BearerAuthProvider):
    """
    A simple BearerAuthProvider that does not require any specific configuration.
    """
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(
            public_key=k.public_key, jwks_uri=None, issuer=None, audience=None
        )
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="unknown",
                scopes=[],
                expires_at=None,
            )
        return None

mcp = FastMCP(
    "My MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Product Search Tool using SerpApi ---
SearchToolDescription = RichToolDescription(
    description="Searches for products using Google Shopping via SerpApi, and returns the raw text results.",
    use_when="Use this tool when a user asks for a product recommendation or is looking for a specific item to buy.",
    side_effects="The user will receive a list of product search results, which can be used to provide recommendations.",
)

@mcp.tool(description=SearchToolDescription.model_dump_json())
async def search_for_products(
    query: Annotated[
        str, Field(description="A description of the user's needs or the product they are looking for.")
    ]
) -> str:
    """
    Fetches product data from SerpApi based on the user's query.
    It returns a plain text string of results for the LLM to process.
    """
    # Check for specific conversational triggers first
    # This is a workaround; in a production environment, this logic would
    # typically be handled by the conversational agent, not the tool.
    if query.lower() in ["hi", "/mcp use 2OMm2SBD2x"]:
        return "I am assigned to buy a product for you."

    if SERPAPI_API_KEY == "YOUR_SERPAPI_API_KEY_HERE":
        return "SerpApi key is not configured. Please replace 'YOUR_SERPAPI_API_KEY_HERE' with your key."

    try:
        # SerpApi endpoint and parameters
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": SERPAPI_API_KEY
        }

        # Make the request
        response = requests.get(url, params=params)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        
        # Check if the response contains shopping results
        if "shopping_results" not in data or not data["shopping_results"]:
            return f"I'm sorry, I couldn't find any Google Shopping results for '{query}'. Please try a different query."

        # Format the results into a readable string for the LLM
        results_string = f"Google Shopping Results for '{query}':\n\n"
        for result in data["shopping_results"]:
            results_string += f"Title: {result.get('title', 'N/A')}\n"
            results_string += f"Price: {result.get('price', 'N/A')}\n"
            results_string += f"Source: {result.get('source', 'N/A')}\n"
            results_string += f"Link: {result.get('link', 'N/A')}\n"
            results_string += "---\n"
        
        return results_string

    except requests.exceptions.RequestException as e:
        # Handle potential errors during the API call
        return f"An error occurred while fetching products: {e}"

async def main():
    await mcp.run_async(
        "streamable-http",
        host="0.0.0.0",
        port=8085,
    )

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
