import streamlit as st
import sys
import contextlib
import re
import os
from io import StringIO
from src.main import main

# Page configuration
st.set_page_config(page_title="AutoRefactorOps Dashboard", page_icon="⚙️", layout="wide")

# Function to clean terminal color codes (ANSI escape sequences)
def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Dashboard Header
st.title("⚙️ AutoRefactorOps: Multi-Agent System")
st.markdown("#### Autonomous Technical Debt Reduction & Verification Dashboard")
st.markdown("Developed by Ali, Alperen, Yiğit & Niyazi")
st.divider()

# Dashboard Information Cards (4 Agents)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("🕵️ **Discovery Agent**\n\nScans codebase for high Cyclomatic Complexity.")
with col2:
    st.warning("👷‍♂️ **Refactoring Agent**\n\nReduces Technical Debt (Delta D) autonomously.")
with col3:
    st.success("🧐 **Verification Agent**\n\nEnsures Zero Semantic Drift via AST & Tests.")
with col4:
    st.error("🛡️ **Rollback Agent**\n\nGuarantees safety via Git state saving and autonomous rollbacks.")

st.markdown("---")

# --- YENİ EKLENEN BÖLÜM: KOD ÖNİZLEME ---
st.markdown("### 📂 Target Codebase for Analysis")
target_file_path = "evaluation/synthetic_repo/target_smelly.py"

# Hedef dosyayı okuyup ekranda gösteriyoruz
try:
    with open(target_file_path, "r", encoding="utf-8") as f:
        smelly_code = f.read()
    
    with st.expander(f"👀 View Current Target File ({target_file_path})", expanded=True):
        st.markdown("This is the highly complex 'spaghetti code' the agents will attempt to refactor:")
        st.code(smelly_code, language="python")
except Exception as e:
    st.warning(f"Could not load target file. Make sure it exists at {target_file_path}")

st.markdown("---")
# ----------------------------------------

# Trigger Button
if st.button("🚀 INITIATE AUTONOMOUS PIPELINE", type="primary", use_container_width=True):
    
    # UI Elements for loading state
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    status_text.info("System Initialized. Agents are scanning the target directory... (This may take 1-2 minutes)")
    progress_bar.progress(30)
    
    # Buffer to catch terminal outputs
    output_buffer = StringIO()
    
    with contextlib.redirect_stdout(output_buffer):
        try:
            main()
        except Exception as e:
            print(f"\nCRITICAL ERROR: {str(e)}")
            
    progress_bar.progress(100)
    status_text.success("Pipeline Execution Successfully Completed!")
    
    # Clean the output from weird terminal characters
    raw_output = output_buffer.getvalue()
    cleaned_output = clean_ansi(raw_output)
    
    st.markdown("### 📊 Final Operation Report")
    
    # Extract only the final report part to show it cleanly
    if "FINAL OPERATION REPORT" in cleaned_output:
        final_report_section = cleaned_output.split("FINAL OPERATION REPORT")[-1]
        final_report_clean = final_report_section.replace("=", "").strip()
        
        # Show the final result in a beautiful, highlighted box
        st.success(final_report_clean)
    else:
        st.warning("System finished, but the final report format was unexpected. See details below.")
    
    # Hide the long, boring terminal logs inside a clickable accordion (expander)
    with st.expander("🔍 View Detailed Agent Execution Logs (Terminal Output)"):
        st.text(cleaned_output)
        
st.markdown("---")
st.caption("AutoRefactorOps v1.0 | Academic Evaluation Build")