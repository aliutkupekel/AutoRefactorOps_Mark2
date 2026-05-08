import pytest
from src.mcp_tools.ast_validator import ASTValidator

def test_no_semantic_drift():
    code_orig = "def add(a, b): return a + b"
    code_new = "def add(a, b):\n    # Optimized\n    return a + b"
    
    validator = ASTValidator(code_orig, code_new)
    is_safe, reasons = validator.check_semantic_drift()
    
    assert is_safe is True
    assert len(reasons) == 0

def test_signature_modification_detected():
    code_orig = "def add(a, b): return a + b"
    code_new = "def add(val1, val2): return val1 + val2"
    
    validator = ASTValidator(code_orig, code_new)
    is_safe, reasons = validator.check_semantic_drift()
    
    assert is_safe is False
    assert any("Modified signature" in r for r in reasons)