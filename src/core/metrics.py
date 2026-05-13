"""
Formal metrics calculation for AutoRefactorOps.
Evaluates the success of the Multi-Agent System based on Section 3 of the model.
"""

def calculate_sdr(failed_tests: int, total_tests: int) -> float:
    """
    Calculates Semantic Drift Rate (SDR).
    Formula: (Failed Tests / Total Tests) * 100
    Lower is better. A successful refactor MUST have an SDR of 0.0%.
    """
    if total_tests == 0:
        return 0.0
    return (failed_tests / total_tests) * 100.0

def calculate_arr(successful_refactors: int, total_attempts: int) -> float:
    """
    Calculates Autonomous Resolution Rate (ARR).
    Formula: (Successful Refactors / Total Attempts) * 100
    Higher is better. Measures the autonomous capability of the agents.
    """
    if total_attempts == 0:
        return 0.0
    return (successful_refactors / total_attempts) * 100.0