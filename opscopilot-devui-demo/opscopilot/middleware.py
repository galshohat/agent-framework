"""
Middleware for OpsCopilot demo.
Simple logging middleware for agents and tools.
"""
import time
from typing import Callable, Awaitable
from agent_framework import AgentRunContext, FunctionInvocationContext


async def logging_agent_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Simple middleware that logs agent execution with timing."""
    messages_count = len(context.messages) if hasattr(context, 'messages') else 0
    
    print(f"\n{'='*50}")
    print(f"🤖 Agent starting... (messages: {messages_count})")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    try:
        await next(context)
        elapsed = time.time() - start_time
        
        print(f"\n{'='*50}")
        print(f"✅ Agent finished! (took {elapsed:.2f}s)")
        print(f"{'='*50}\n")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n{'='*50}")
        print(f"❌ Agent ERROR: {str(e)}")
        print(f"   Elapsed: {elapsed:.2f}s")
        print(f"{'='*50}\n")
        raise


async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """Middleware that logs function calls with inputs and outputs."""
    func_name = context.function.name if hasattr(context, 'function') else "Unknown"
    args = context.arguments if hasattr(context, 'arguments') else {}
    
    print(f"\n  🔧 Tool CALL: {func_name}")
    print(f"     Args: {args}")
    
    start_time = time.time()
    
    try:
        await next(context)
        elapsed = time.time() - start_time
        
        # Truncate long results for readability
        result_str = str(context.result) if hasattr(context, 'result') else "N/A"
        if len(result_str) > 200:
            result_str = result_str[:200] + "..."
        
        print(f"  ✅ Tool RESULT: {func_name}")
        print(f"     Elapsed: {elapsed:.3f}s")
        print(f"     Result: {result_str}")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"  ❌ Tool ERROR: {func_name}")
        print(f"     Elapsed: {elapsed:.3f}s")
        print(f"     Error: {str(e)}")
        raise


def get_middleware_list() -> list:
    """Return the list of middleware to attach to agents."""
    return [
        logging_agent_middleware,
        logging_function_middleware,
    ]
