import pytest
from src.mcp_tools.ast_validator import ASTValidator

def test_no_semantic_drift():
    """Test that a safe refactor passes AST validation."""
    code_orig = "def calculate(a, b):\n    return a + b"
    code_new = "def calculate(a, b):\n    # Added comment for clarity\n    return a + b"
    
    validator = ASTValidator(code_orig, code_new)
    is_safe, reasons = validator.check_semantic_drift()
    
    assert is_safe is True
    assert len(reasons) == 0

def test_signature_modification_detected():
    """Test that changing function parameters triggers Semantic Drift."""
    code_orig = "def calculate(a, b):\n    return a + b"
    code_new = "def calculate(val1, val2):\n    return val1 + val2"
    
    validator = ASTValidator(code_orig, code_new)
    is_safe, reasons = validator.check_semantic_drift()
    
    assert is_safe is False
    assert any("Modified signature" in r for r in reasons)