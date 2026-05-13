"""
Global State Management for the Multi-Agent System.
Ensures thread-safe and deterministic tracking of the refactoring pipeline.
"""
from dataclasses import dataclass

@dataclass
class RefactoringState:
    target_file: str = ""
    original_code: str = ""
    refactored_code: str = ""
    is_safe: bool = False
    delta_d: int = 0
    test_passed: bool = False

# Global singleton state instance used by CrewAI Tools
current_state = RefactoringState()