# Memory Update & Session Recap Guide

## Purpose

This guide explains the "update memory" workflow that enables context-aware operations and maintains actionable project memory across Copilot sessions.

## How It Works

### User Workflow

1. **Before major changes**, request a recap:
   ```
   "Update memory"
   "Show project status"
   "Give me a recap"
   ```

2. **Copilot responds** with current PROJECT_STATUS.md contents

3. **Review the status** and decide next action

4. **Request specific work**:
   ```
   "Implement rate limiting"
   "Plan Azure migration"
   "Add database persistence"
   ```

5. **Copilot provides** step-by-step CLI commands and templates

6. **Execute commands** (all are copy/paste ready)

7. **Copilot updates** PROJECT_STATUS.md after significant changes

## When to Request a Recap

Always request a recap **before** these major operations:

- ✅ Azure migration or platform changes
- ✅ Database schema changes  
- ✅ API breaking changes
- ✅ Major refactoring (> 500 lines)
- ✅ Production deployments
- ✅ Dependency upgrades (major versions)
- ✅ Architecture changes
- ✅ New feature implementation (when unsure of current state)

## Key Documents

### PROJECT_STATUS.md
**The canonical project status document**

Contains:
- Current features and their status
- Missing/priority gaps  
- Architecture (current and planned)
- Development workflow
- Key commands
- File structure
- Recent changes
- Next actions

**When to update:**
- After significant feature additions
- After infrastructure changes
- After incident recovery
- Monthly (at minimum)

### Supporting Documents
- **CHAOS_ANALYSIS.md** - Historical incident analysis (Feb 2026)
- **RECOVERY_PLAN.md** - Recovery from code bloat incident
- **README.md** - User-facing documentation and quick start

## CLI-First Workflow

This project uses a **terminal-centric workflow**:

1. User copies terminal output
2. Copilot reads and responds
3. All commands are **copy/paste ready**
4. Copilot CLI available separately for code/command help

### Example Interaction

```
User: "Update memory"

Copilot: [Displays PROJECT_STATUS.md content]

User: "Add rate limiting to the /validate endpoint"

Copilot: "I'll implement rate limiting. Here are the steps:

1. Install slowapi:
   pip install slowapi

2. Update requirements.txt:
   echo "slowapi==0.1.9" >> requirements.txt

3. [Provides detailed implementation steps]
"

User: [Copies and pastes commands]
```

## Memory Persistence Strategy

### What Gets Stored
- Critical architectural decisions
- Missing features and priorities  
- Code conventions and patterns
- Common commands and workflows
- Historical incidents and learnings

### What Gets Documented
- Current feature status
- Deployment configurations
- File structure and organization
- Testing commands and practices
- Security considerations

### What Gets Updated
- PROJECT_STATUS.md (after significant changes)
- Repository memories (via store_memory tool)
- Supporting docs as needed

## Best Practices

### For Users
1. Request recap before major changes
2. Review status before deciding next steps
3. Provide context when making requests
4. Validate changes after implementation

### For Copilot Agents
1. Print PROJECT_STATUS.md when user requests recap
2. Store new facts to memory when discovered
3. Update PROJECT_STATUS.md after significant work
4. Reference existing status when planning work
5. Maintain CLI-first, copy/paste ready command style

## Quick Commands

```bash
# View project status
cat PROJECT_STATUS.md

# Check what's changed recently
git log --oneline -10

# Run all tests to validate current state
python -m unittest discover tests/ -v

# Check for uncommitted changes
git status
```

## Troubleshooting

### "I'm not sure what the current state is"
→ Request: "Update memory" or "Show project status"

### "What was that command again?"
→ Check PROJECT_STATUS.md "Key Commands" section

### "What are the priority tasks?"
→ Check PROJECT_STATUS.md "Missing/Priority Gaps" section

### "How do I deploy this?"
→ Check PROJECT_STATUS.md "Deployment Information" section

---

**Version:** 1.0  
**Last Updated:** 2026-02-11  
**Purpose:** Enable actionable project memory and context-aware operations
