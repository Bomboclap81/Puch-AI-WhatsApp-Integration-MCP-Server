# Puch AI - WhatsApp Integration MCP Server

This MCP server enables Puch AI to interact with WhatsApp and perform various tasks.

## Overview

Puch AI is an AI assistant that can automate tasks and provide information through various channels. This MCP server provides a bridge between Puch AI and WhatsApp, allowing Puch AI to:

*   Fetch information from the web using the `fetch` tool.
*   Search for products using the `search_for_products` tool.
*   (Potentially) Send and receive messages through WhatsApp (if implemented).

## Setup

1.  **Clone the repository:**

    ```
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a `.env` file:**

    Create a `.env` file in the root directory with the following contents:

    ```
    SERPAPI_API_KEY=YOUR_SERPAPI_API_KEY
    MY_NUMBER=YOUR_PHONE_NUMBER
    TOKEN=YOUR_BEARER_TOKEN
    ```

    *   `SERPAPI_API_KEY`: Obtain a SerpApi API key from [https://serpapi.com/](https://serpapi.com/) and replace `YOUR_SERPAPI_API_KEY` with your actual API key. This is required for the `search_for_products` tool.
    *   `MY_NUMBER`: Replace `YOUR_PHONE_NUMBER` with your WhatsApp phone number (including the country code, e.g., `919579472584`). This may be used for future WhatsApp integration features.
    *   `TOKEN`: Replace `YOUR_BEARER_TOKEN` with a secure bearer token. This token is used to authenticate requests to the MCP server.

3.  **Install the dependencies:**

    ```
    pip install -r requirements.txt
    ```

4.  **Run the server:**

    ```
    python main.py
    ```

## Authentication

The server requires a bearer token for authentication. Include the following header in your requests:

```
Authorization: Bearer YOUR_BEARER_TOKEN
```

Replace `YOUR_BEARER_TOKEN` with the value you set in the `.env` file.

## Available Tools

### `fetch`

Fetches the content of a URL.

*   **Parameters:**
    *   `url` (string, required): The URL to fetch.
    *   `max_length` (integer, optional): The maximum number of characters to return (default: 5000).
    *   `start_index` (integer, optional): The index to start the content from (default: 0).
    *   `raw` (boolean, optional): Whether to return the raw HTML content (default: False).

### `search_for_products`

Searches for products using Google Shopping via SerpApi.

*   **Parameters:**
    *   `query` (string, required): A description of the user's needs or the product they are looking for.

## WhatsApp Integration (Future)

This MCP server is designed to be integrated with WhatsApp. In the future, it may be possible to send and receive messages through WhatsApp using this server.

## Example Usage

To search for a product and recommend it to a user, you can use the `search_for_products` tool. For example, to search for a laptop, you can send the following request:

```
POST /mcp/
Authorization: Bearer YOUR_BEARER_TOKEN
Content-Type: application/json

{
  "tool_name": "search_for_products",
  "arguments": {
    "query": "laptop"
  }
}
```

The server will respond with a list of product search results, which you can then use to recommend a product to the user.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.
