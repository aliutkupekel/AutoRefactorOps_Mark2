"""
Core Configuration and Thresholds for AutoRefactorOps.
Based on the Formal Optimization and Risk Model (Section 3).
"""

# Risk Tolerance Threshold (tau)
# P(R) < tau must hold true for a valid refactoring.
RISK_TOLERANCE_TAU = 0.0  # Strict zero tolerance for semantic drift

# Target metric for successful debt reduction
MIN_DELTA_D = 1  # The minimum complexity reduction required to accept a merge

# Target Paths
TARGET_EVAL_DIR = "evaluation/synthetic_repo"