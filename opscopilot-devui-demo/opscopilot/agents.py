"""
Agent definitions for OpsCopilot demo.
"""
import os
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential, AzureCliCredential

from .models import TriageResult, FinalPlan
from .tools import (
    fetch_service_health,
    lookup_runbook,
    search_known_issues,
    restart_service,
    open_sev1_bridge,
)
from .middleware import logging_agent_middleware, logging_function_middleware
from .memory import get_ops_memory

# Load environment variables
load_dotenv()


def create_chat_client():
    """
    Create a chat client based on environment configuration.
    Uses Azure OpenAI with DefaultAzureCredential or AzureCliCredential.
    """
    # Try to use Azure CLI credential for local development
    try:
        credential = AzureCliCredential()
        print("🔵 Using Azure OpenAI with Azure CLI credential")
        return AzureOpenAIChatClient(credential=credential)
    except Exception as e:
        print(f"⚠️ Azure CLI credential failed: {e}")
        
    # Fall back to DefaultAzureCredential
    try:
        credential = DefaultAzureCredential()
        print("🔵 Using Azure OpenAI with DefaultAzureCredential")
        return AzureOpenAIChatClient(credential=credential)
    except Exception as e:
        raise ValueError(
            f"Failed to create Azure OpenAI client: {e}\n"
            "Make sure you are logged in with Azure CLI: az login"
        )


# Shared chat client (created lazily)
_chat_client = None


def get_chat_client():
    """Get or create the shared chat client."""
    global _chat_client
    if _chat_client is None:
        _chat_client = create_chat_client()
    return _chat_client


def build_classifier_agent() -> ChatAgent:
    """
    Build the classifier agent that triages incidents.
    Determines category, severity, and whether approval is needed.
    """
    return get_chat_client().as_agent(
        name="ClassifierAgent",
        instructions="""You are an expert incident classifier for cloud operations.

Your job is to analyze an incident and determine:
1. **Category**: Is this an Incident, Question, Change request, or Security issue?
2. **Severity**: Sev1 (critical), Sev2 (high), or Sev3 (low)
3. **Confidence**: How confident are you in this classification (0.0 to 1.0)
4. **Next Action**: What should be done next
5. **Needs Approval**: Does this require human approval for a dangerous action?
6. **Approval Action**: If approval needed, specify: "restart_service" or "open_sev1_bridge"

Classification guidelines:
- Sev1: Customer-facing outage, data loss risk, security breach
- Sev2: Degraded performance, partial outage, potential escalation
- Sev3: Minor issues, questions, planned changes

Set needs_approval=true if:
- The recommended action involves restarting a production service
- A Sev1 bridge call should be opened
- Any action that could cause customer impact

Always output valid JSON matching the TriageResult schema.""",
        response_format=TriageResult,
        middleware=[logging_agent_middleware, logging_function_middleware],
        context_providers=[get_ops_memory()],
    )


def build_writer_agent() -> ChatAgent:
    """
    Build the writer agent that creates the final incident plan.
    """
    return get_chat_client().as_agent(
        name="WriterAgent",
        instructions="""You are an expert technical writer for cloud operations.

Your job is to create a comprehensive incident response plan that includes:
1. **Summary**: A brief 1-2 sentence summary of the situation
2. **Steps**: 3-6 actionable steps to resolve or investigate the issue
3. **Customer Message**: A professional message to send to the customer (can be in Hebrew if context indicates)
4. **Internal Note**: Technical notes for the ops team

Guidelines:
- Be concise but thorough
- Steps should be actionable and specific
- Customer message should be empathetic and informative
- Internal notes can include technical details and caveats

Always output valid JSON matching the FinalPlan schema.""",
        response_format=FinalPlan,
        tools=[fetch_service_health, lookup_runbook, search_known_issues],
        middleware=[logging_agent_middleware, logging_function_middleware],
        context_providers=[get_ops_memory()],
    )


def build_qa_agent() -> ChatAgent:
    """
    Build the QA agent that reviews plans for safety and consistency.
    """
    return get_chat_client().as_agent(
        name="QAAgent",
        instructions="""You are a quality assurance reviewer for incident response plans.

Your job is to review a proposed incident plan and:
1. Verify the plan is safe and won't cause additional issues
2. Check for consistency between the summary, steps, and messages
3. Ensure customer communication is appropriate
4. Suggest 1-2 improvements if needed

Output your review as plain text with:
- ✅ APPROVED or ⚠️ NEEDS REVISION
- Brief explanation
- Suggested improvements (if any)

Be constructive but thorough. Safety is the top priority.""",
        middleware=[logging_agent_middleware, logging_function_middleware],
        context_providers=[get_ops_memory()],
    )


def build_agents() -> dict[str, ChatAgent]:
    """
    Build all agents and return them in a dictionary.
    """
    return {
        "classifier": build_classifier_agent(),
        "writer": build_writer_agent(),
        "qa": build_qa_agent(),
    }


# Convenience exports
__all__ = [
    "build_classifier_agent",
    "build_writer_agent", 
    "build_qa_agent",
    "build_agents",
    "get_chat_client",
]
