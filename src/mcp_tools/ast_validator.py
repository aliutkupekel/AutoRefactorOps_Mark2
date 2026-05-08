import ast
from typing import List, Dict, Tuple

class ASTValidator:
    """
    Formally verifies that a refactored Python code does not exhibit Semantic Drift 
    by comparing its Abstract Syntax Tree (AST) against the original code.
    """

    def __init__(self, original_code: str, refactored_code: str):
        self.original_code = original_code
        self.refactored_code = refactored_code
        self.original_tree = ast.parse(original_code)
        self.refactored_tree = ast.parse(refactored_code)

    def _extract_function_signatures(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extracts function names and their arguments from the AST."""
        signatures = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                signatures[node.name] = args
        return signatures

    def _extract_imports(self, tree: ast.AST) -> set:
        """Extracts all imported modules from the AST."""
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        return imports

    def check_semantic_drift(self) -> Tuple[bool, List[str]]:
        """
        Validates the refactored code against the original.
        Returns a tuple: (is_safe: bool, drift_reasons: List[str])
        """
        drift_reasons = []
        is_safe = True

        # 1. API Signature Check
        orig_sigs = self._extract_function_signatures(self.original_tree)
        refact_sigs = self._extract_function_signatures(self.refactored_tree)

        for func_name, args in orig_sigs.items():
            if func_name not in refact_sigs:
                is_safe = False
                drift_reasons.append(f"Semantic Drift: Missing original function '{func_name}'.")
            elif refact_sigs[func_name] != args:
                is_safe = False
                drift_reasons.append(f"Semantic Drift: Modified signature for '{func_name}'. Expected {args}, got {refact_sigs[func_name]}.")

        # 2. Hallucinated Dependency Check
        orig_imports = self._extract_imports(self.original_tree)
        refact_imports = self._extract_imports(self.refactored_tree)

        unapproved_imports = refact_imports - orig_imports
        if unapproved_imports:
            is_safe = False
            drift_reasons.append(f"Semantic Drift: Unapproved imports detected: {unapproved_imports}.")

        return is_safe, drift_reasons

if __name__ == "__main__":
    # Sistemin çalıştığını kanıtlayan hızlı test
    code_before = "import math\ndef calc(r):\n    return math.pi * r"
    
    # LLM'in uydurduğu kötü senaryo: 'os' kütüphanesini uydurmuş ve 'r' parametresini 'radius' yapmış
    code_after_bad = "import math\nimport os\ndef calc(radius):\n    return math.pi * radius"
    
    validator = ASTValidator(code_before, code_after_bad)
    safe, reasons = validator.check_semantic_drift()
    print(f"Kod Güvenli mi?: {safe}")
    for r in reasons:
        print(f"- {r}")