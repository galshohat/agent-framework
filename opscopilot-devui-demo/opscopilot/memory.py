"""
Simple memory/context provider for OpsCopilot demo.
"""
import re
from typing import Any
from collections.abc import MutableSequence, Sequence
from agent_framework import ContextProvider, Context, ChatMessage


class OpsMemory(ContextProvider):
    """
    Simple context provider that remembers:
    - preferred_language (default: hebrew)
    - last_customer (optional)
    - last_service (optional)
    
    Adds instructions on invoke and extracts context on completion.
    """
    
    def __init__(self):
        self.preferred_language: str = "hebrew"
        self.last_customer: str | None = None
        self.last_service: str | None = None
    
    async def invoking(self, messages: ChatMessage | MutableSequence[ChatMessage], **kwargs: Any) -> Context:
        """
        Called before agent runs. Returns context instructions.
        """
        instructions = []
        
        # Language preference
        if self.preferred_language.lower() == "hebrew":
            instructions.append("Respond in Hebrew when addressing the customer. Keep technical terms in English.")
        else:
            instructions.append(f"Respond in {self.preferred_language}. Keep answers concise.")
        
        # Add context about previous interactions
        if self.last_service:
            instructions.append(f"Context: Previous interaction involved service '{self.last_service}'.")
        
        if self.last_customer:
            instructions.append(f"Context: Previous customer was '{self.last_customer}'.")
        
        return Context(instructions=" ".join(instructions) if instructions else None)
    
    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: ChatMessage | Sequence[ChatMessage] | None = None,
        invoke_exception: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Called after agent runs. Extracts and stores context.
        """
        # Ensure request_messages is a list
        messages_list = [request_messages] if isinstance(request_messages, ChatMessage) else list(request_messages)
        
        # Look for user messages and extract info
        for msg in messages_list:
            if hasattr(msg, 'role') and msg.role.value == "user":
                # Get the text content from the message
                text = ""
                if hasattr(msg, 'contents') and msg.contents:
                    for content in msg.contents:
                        if hasattr(content, 'text'):
                            text += content.text + " "
                
                self._extract_context(text)
    
    def _extract_context(self, text: str) -> None:
        """Extract customer and service from text using simple patterns."""
        # Look for customer pattern
        customer_match = re.search(r'[Cc]ustomer[:\s]+([A-Za-z0-9_-]+)', text)
        if customer_match:
            self.last_customer = customer_match.group(1)
        
        # Look for service pattern
        service_match = re.search(r'[Ss]ervice[:\s]+([A-Za-z0-9_-]+)', text)
        if service_match:
            self.last_service = service_match.group(1)
    
    def set_language(self, language: str) -> None:
        """Update preferred language."""
        self.preferred_language = language
    
    def get_state(self) -> dict:
        """Return current memory state for debugging."""
        return {
            "preferred_language": self.preferred_language,
            "last_customer": self.last_customer,
            "last_service": self.last_service,
        }
    
    def clear(self) -> None:
        """Clear memory state."""
        self.last_customer = None
        self.last_service = None
    
    def serialize(self) -> str:
        """Serialize the memory for thread persistence."""
        import json
        return json.dumps(self.get_state())


# Global instance for sharing across agents
_ops_memory = OpsMemory()


def get_ops_memory() -> OpsMemory:
    """Return the shared OpsMemory instance."""
    return _ops_memory
