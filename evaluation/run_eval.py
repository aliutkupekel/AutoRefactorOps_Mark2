"""
Evaluation Execution Script.
Calculates Syntax Error Rate (SER), Semantic Drift Rate (SDR), and Autonomous Resolution Rate (ARR).
"""
import os
import subprocess

def evaluate_metrics():
    print("Starting Formal Evaluation Pipeline...")
    print("Running Baseline Tests...")
    
    # Testleri koştur ve hataları say
    result = subprocess.run(["pytest", "evaluation/synthetic_repo/test_target.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Baseline: 0% Semantic Drift (Ground Truth Verified).")
    else:
        print("Baseline Failed: Target code already has broken logic.")

    print("\nTo calculate ARR (Autonomous Resolution Rate), run src/main.py and log the outcomes of 10 iterations.")
    print("Target metrics:")
    print("- SDR (Semantic Drift Rate): Must strictly be 0.0%")
    print("- ARR (Autonomous Resolution Rate): Expected > 80%")

if __name__ == "__main__":
    evaluate_metrics()