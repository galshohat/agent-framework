# Support Email Copilot — Microsoft Agent Framework

A complete learning journey for building an AI-powered support email system using Microsoft Agent Framework.

## Prerequisites

1. **Azure subscription** with access to Azure OpenAI
2. **Azure OpenAI resource** with a deployed model (e.g., `gpt-4o-mini`)
3. **Azure CLI** installed and authenticated (`az login`)
4. **Python 3.10+** installed

## Setup Instructions

### 1. Install Azure CLI

```bash
# macOS
brew install azure-cli

# Authenticate
az login
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

**Important:** The `--pre` flag is required to install the pre-release version of agent-framework, which includes the `as_agent()` method and other essential features.

```bash
pip install -U agent-framework --pre
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure OpenAI configuration
# Get these values from Azure Portal > Your OpenAI Resource
```

Required values in `.env`:
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_VERSION`: API version (e.g., `2024-02-15-preview`)
- `AZURE_OPENAI_DEPLOYMENT`: Your model deployment name

### 5. Run the Notebook

```bash
jupyter notebook agent_framework.ipynb
```

Or open in VS Code with the Jupyter extension.

## What You'll Build

By completing this notebook, you'll create a **Support Email Copilot** with:

- ✅ Email classification (Spam / Not Spam / Uncertain)
- ✅ Customer SLA and ticket status lookup
- ✅ Professional response drafting with customizable tone
- ✅ Human-in-the-loop approval workflows
- ✅ Persistent user preference memory
- ✅ Parallel processing for long emails
- ✅ Multi-agent quality review
- ✅ Complete observability and logging

## Project Structure

```
SDK-Magentic-Workflow/
├── .env                      # Your Azure OpenAI configuration
├── .env.example              # Example configuration file
├── requirements.txt          # Python dependencies
├── agent_framework.ipynb     # Main learning notebook
├── .github/
│   └── agents/
│       ├── backend-agent.md
│       ├── frontend-agent.md
│       └── integration-agent.md
└── README.md                 # This file
```

## Troubleshooting

### AttributeError: 'AzureOpenAIChatClient' object has no attribute 'as_agent'

This error means the pre-release version of agent-framework was not installed correctly. Fix it with:

```bash
# Uninstall any existing version
pip uninstall -y agent-framework

# Install the pre-release version with --pre flag
pip install -U agent-framework --pre

# Verify installation
pip show agent-framework
```

**Important:** The `--pre` flag is required. The stable version does not include the `as_agent()` method.

After reinstalling, restart your Jupyter kernel (Kernel → Restart Kernel) and re-run the setup cells.

### Authentication Issues

If you see authentication errors:

```bash
# Re-authenticate with Azure CLI
az login

# Verify your account
az account show

# Check Azure OpenAI access
az cognitiveservices account show --name <your-openai-resource-name> --resource-group <your-resource-group>
```

### Module Not Found

If you see `ModuleNotFoundError`:

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies with --pre flag
pip install -U agent-framework --pre
pip install -r requirements.txt
```

## Learn More

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

MIT
