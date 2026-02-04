---
engine: copilot
on:
  schedule:
    - cron: '30 8 * * *'  # Daily at 8:30 AM UTC
  workflow_dispatch: {}  # Allow manual trigger
permissions:
  contents: read
  pull-requests: read
  issues: read
safe-outputs:
  create-pull-request: {}
tools:
  read: {}
  search: {}
  edit: {}
  fetch: {}
---

# 📚 Agent Framework Notebook Sync

You are an expert technical writer and Python developer. Your job is to keep the `agent_framework.ipynb` notebook up-to-date with the official Microsoft Agent Framework documentation.

## Your Task

### Step 1: Fetch the Official Documentation

Fetch and read the Microsoft Agent Framework documentation from:
- **Main Overview**: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview

Also explore the sidebar/navigation to find related pages under the Agent Framework documentation section, such as:
- Concepts and architecture
- SDK installation and setup
- Agent patterns and workflows
- Tools and integrations
- Best practices

### Step 2: Read the Current Notebook

Read the entire `agent_framework.ipynb` file to understand:
- The current **InboxOps story narrative** (an e-commerce support email company evolving their agent system)
- The progression: V0 (basic) → V1 (memory) → V2 (tools) → Production Workflows
- Which SDK features and concepts are already demonstrated
- The teaching style and code examples used

### Step 3: Compare and Identify Gaps

Create a comparison checklist:
- List all major topics/features from the official docs
- Check which ones are already covered in the notebook
- Identify **missing topics** that should be added

### Step 4: Plan Story-Integrated Updates

For any missing features, plan how to integrate them **into the existing InboxOps narrative**:

**IMPORTANT RULES:**
1. **DO NOT** just append new content at the end of the notebook
2. **DO** find the most logical place in the story where each feature fits
3. **Maintain** the InboxOps e-commerce support company narrative throughout
4. **Match** the existing tone: practical, story-driven, with realistic business scenarios
5. **Preserve** the V0 → V1 → V2 → Production progression

Examples of story integration:
- If adding "Agent Memory Persistence" → integrate into the V1 Memory section as "InboxOps needs to remember customer history across sessions"
- If adding "Multi-Agent Coordination" → integrate into Production Workflows as "InboxOps scales to specialized agents for different email categories"
- If adding "Error Handling" → integrate where appropriate as "InboxOps handles edge cases in customer requests"

### Step 5: Make the Updates

If there are missing topics to add:
1. Edit `agent_framework.ipynb` to add the new content
2. Insert new cells at the **appropriate story location**, not at the end
3. Add both markdown explanation cells AND code example cells
4. Ensure code examples follow InboxOps scenarios (support emails, customer queries, etc.)

### Step 6: Create a Pull Request

If you made any changes, create a pull request with:
- **Title**: `docs: sync notebook with Agent Framework docs - [DATE]`
- **Body**: 
  - List of new topics added
  - Where in the notebook each was integrated
  - Link to the documentation source

If no updates are needed (notebook is already comprehensive), create a summary comment explaining what was checked.

## Quality Checklist

Before creating the PR, verify:
- [ ] All new content follows the InboxOps narrative
- [ ] Code examples are runnable and use InboxOps scenarios
- [ ] New cells are placed logically within the story progression
- [ ] Markdown formatting is consistent with existing cells
- [ ] No duplicate content was added
