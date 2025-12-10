# Athena Core - Deployment Guide

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start Athena Core
docker-compose up -d

# With Ollama for LLM routing
docker-compose --profile with-ollama up -d

# View logs
docker-compose logs -f athena-core
```

Access: http://localhost:8000

### Option 2: Docker Build

```bash
# Build image
docker build -t athena-core .

# Run container
docker run -d -p 8000:8000 --name athena athena-core
```

### Option 3: Local Development

```bash
# Create virtual environment
python3 -m venv spark-lab
source spark-lab/bin/activate

# Install dependencies
pip install -r athena_system/requirements.txt

# Run server
python -m athena_system.web_ui.server
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SAP_API_KEY` | SAP API Business Hub API key | (empty - uses mock) |
| `SAP_API_HUB_URL` | SAP API endpoint | https://sandbox.api.sap.com |
| `OLLAMA_URL` | Ollama server URL | http://localhost:11434 |
| `OLLAMA_MODEL` | LLM model for routing | llama3.2 |

### SAP Integration

1. Sign up at https://api.sap.com
2. Get API key from dashboard
3. Set environment variable:

```bash
export SAP_API_KEY="your-api-key"
```

### LLM Routing

For semantic routing with Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2

# Athena will auto-detect Ollama
```

---

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Chat interface |
| `/dashboard` | Agent dashboard |
| `/api/chat` | Chat API (POST) |
| `/api/sap/status` | SAP connection status |
| `/api/sap/partners` | Business partners |
| `/api/sap/orders` | Sales orders |
| `/api/sap/revenue` | Revenue summary |
| `/api/dashboard` | Dashboard data |

---

## Public Demo (ngrok)

1. Sign up at https://ngrok.com
2. Install: `sudo snap install ngrok`
3. Authenticate: `ngrok config add-authtoken YOUR_TOKEN`
4. Expose: `ngrok http 8000`
5. Share the https URL with clients

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Athena Core                      │
├─────────────────────────────────────────────────┤
│  Web UI (index.html, dashboard.html)            │
├─────────────────────────────────────────────────┤
│  Server (server.py)                             │
│  ├── Chat API                                   │
│  ├── SAP Data APIs                              │
│  └── Dashboard API                              │
├─────────────────────────────────────────────────┤
│  Agents                                         │
│  ├── LLM Router (Ollama + Keyword Fallback)     │
│  ├── Orchestrator (400+ agents)                 │
│  └── Specialized Agents (Legal, Sales, etc.)   │
├─────────────────────────────────────────────────┤
│  Integrations                                   │
│  ├── SAP Connector (API Hub + Mock)             │
│  └── NANDA (Decentralized Registry)             │
└─────────────────────────────────────────────────┘
```
