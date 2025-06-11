import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import streamlit as st
# from crew_setup.main_crew import run_crew
# from utils.file_loader import read_uploaded_file

# st.set_page_config(page_title="Autonomous Agent", layout="centered")

# st.title(" Goal-Driven Workflow Automation")

# goal = st.text_area(" Enter your high-level goal (e.g., Summarize and email this):")

# uploaded_file = st.file_uploader(" Upload your input file (PDF, TXT, CSV):", type=["pdf", "txt", "csv"])

# if st.button("Execute Goal"):
#     if goal.strip() and uploaded_file is not None:
#         with st.spinner("Reading file and executing..."):
#             content = read_uploaded_file(uploaded_file)
#             full_goal = f"{goal}\n\nContent:\n{content}"
#             run_crew(full_goal)
#             st.success(" Goal execution completed.")
#     else:
#         st.error("Please enter a goal and upload a file.")

import streamlit as st
from crew_setup.main_crew import run_crew
from utils.file_loader import read_uploaded_file

st.set_page_config(page_title="Autonomous Agent", layout="centered")

st.title(" Goal-Driven Workflow Automation")

goal = st.text_area(" Enter your high-level goal (e.g., Summarize and email this):")

uploaded_file = st.file_uploader(" Upload your input file (PDF, TXT, CSV):", type=["pdf", "txt", "csv"])

if st.button("Execute Goal"):
    if goal.strip() and uploaded_file is not None:
        with st.spinner(" Reading file and executing..."):
            content = read_uploaded_file(uploaded_file)
            full_goal = f"{goal}\n\nContent:\n{content}"
            result = run_crew(full_goal)

            if result.startswith("🚫"):
                st.warning(result)
            else:
                st.success(result)
    else:
        st.error(" Please enter a goal and upload a file.")
