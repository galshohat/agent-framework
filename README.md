# Agent Framework Demo

A demo notebook showcasing Microsoft Agent Framework with Azure OpenAI.

## Setup

### 1. Install Dependencies

```bash
pip install agent-framework --pre python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
API_VERSION=2025-01-01-preview
```

### 3. Azure CLI Authentication

This demo uses Azure CLI credentials. Make sure you're logged in:

```bash
az login
```

## Usage

Open `agent_framework.ipynb` and run the cells to interact with the agent.

## License

MIT
