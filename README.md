# AutoRefactorOps
A Formally Constrained Multi-Agent Framework for Code Refactoring

## Project Overview
"AutoRefactorOps" is a formally constrained multi-agent framework for semantics-preserving code refactoring and technical debt remediation.

## Finalized Requirements (Scope Locked)
1. **Model Context Protocol (MCP) Governance:** A strict bus that controls all file system accesses.
2. **Multi-Agent System:**
   - **Discovery Agent:** Read-only access to scan AST and calculate cyclomatic complexity.
   - **Generator Agent:** Drafts refactored code without write permissions.
   - **Verifier Agent:** Compiles, runs unit tests, and performs AST cross-verification.
   - **Rollback Agent:** Handles Git commits and deterministic rollbacks.
3. **Formal Constraint:** The system will ONLY merge code if Semantic Drift ($S$) = 0 and Technical Debt ($\Delta D$) is reduced.

## Architecture Baseline
The architecture logically separates generative tasks from execution tasks. Modules include:
- `/agents`: Contains all 4 specialized agent logic.
- `/mcp_bus`: The strict schema and ACL verifier.
- `/target_repo`: The sandbox environment containing code to be refactored.

## Contributors
* Ali Utku Pekel
* Alperen Atalay
