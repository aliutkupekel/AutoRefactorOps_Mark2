import os
from crewai.tools import tool
from src.mcp_tools.ast_validator import ASTValidator
from src.mcp_tools.cyclomatic import ComplexityAnalyzer
from src.mcp_tools.test_runner import TestRunner
from src.mcp_tools.git_manager import GitManager

# Global state to hold pre-refactor code for validation
class SystemState:
    original_code: str = ""
    target_file: str = ""

state = SystemState()

@tool("Scan Directory for High Debt")
def scan_directory(directory_path: str) -> str:
    """Scans a directory to find the Python file with the highest cyclomatic complexity."""
    highest_complexity = -1
    target_file = None
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and file != "test_target.py": # exclude tests
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    complexity = ComplexityAnalyzer.calculate_total_complexity(code)
                    if complexity > highest_complexity:
                        highest_complexity = complexity
                        target_file = file_path
                except Exception:
                    continue
                    
    if target_file:
        state.target_file = target_file
        with open(target_file, 'r', encoding='utf-8') as f:
            state.original_code = f.read()
        return f"Found high debt file: {target_file} with complexity {highest_complexity}"
    return "No suitable Python files found."

@tool("Read Target File")
def read_target_file(dummy_param: str = "") -> str:
    """Reads the content of the target file identified for refactoring."""
    if not state.target_file:
        return "Error: No target file has been identified yet."
    return state.original_code

@tool("Write Refactored Code")
def write_refactored_code(new_code: str) -> str:
    """Writes the refactored code back to the target file."""
    if not state.target_file:
        return "Error: No target file has been identified yet."
    
    # Kopyalama hatasını önlemek için çift tırnak ve temizleme kullanıyoruz
    clean_code = new_code.replace("```python", "").replace("```", "")
    clean_code = clean_code.strip()
    
    try:
        with open(state.target_file, 'w', encoding='utf-8') as f:
            f.write(clean_code)
        return "Successfully wrote refactored code to file."
    except Exception as e:
        return f"Failed to write file: {str(e)}"

@tool("Run AST Validation")
def run_ast_validation(dummy_param: str = "") -> str:
    """Validates the refactored code against the original code to ensure no semantic drift."""
    try:
        with open(state.target_file, 'r', encoding='utf-8') as f:
            current_code = f.read()
            
        validator = ASTValidator(state.original_code, current_code)
        is_safe, reasons = validator.check_semantic_drift()
        
        if is_safe:
            return "AST Validation PASSED. No semantic drift detected."
        else:
            return f"AST Validation FAILED. Reasons: {', '.join(reasons)}"
    except Exception as e:
         return f"AST Validation Error: {str(e)}"

@tool("Calculate Complexity Reduction")
def calculate_complexity_reduction(dummy_param: str = "") -> str:
    """Calculates the reduction in technical debt (Delta D)."""
    try:
         with open(state.target_file, 'r', encoding='utf-8') as f:
            current_code = f.read()
            
         result = ComplexityAnalyzer.evaluate_debt_reduction(state.original_code, current_code)
         
         if not result['success']:
             return result['error']
             
         return f"Complexity Analysis: Original={result['original_complexity']}, Refactored={result['refactored_complexity']}, Delta_D={result['delta_d']}. Improved: {result['is_improved']}"
    except Exception as e:
         return f"Complexity Analysis Error: {str(e)}"

@tool("Run Unit Tests")
def run_unit_tests(test_path: str) -> str:
    """Executes unit tests to verify behavior preservation."""
    runner = TestRunner()
    result = runner.run_tests(test_path)
    
    if result['passed']:
        return "Unit Tests PASSED."
    else:
        return f"Unit Tests FAILED.\nOutput: {result['output']}\nError: {result['error']}"

@tool("Execute Git State Save")
def execute_git_state_save(dummy_param: str = "") -> str:
    """Saves the current state of the repository before modifications."""
    gm = GitManager()
    result = gm.save_state("AutoRefactorOps: Pre-refactor safety state")
    return result['message']

@tool("Execute Git Rollback")
def execute_git_rollback(dummy_param: str = "") -> str:
    """Rolls back the repository to the last safe commit."""
    gm = GitManager()
    result = gm.rollback()
    return result['message']