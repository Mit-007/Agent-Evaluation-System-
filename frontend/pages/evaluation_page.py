import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000"  # change this


# =========================
# API HELPERS
# =========================
def run_evaluation(agent_id,project_id,chat_input):
    payload = {"agent_id" : agent_id,"project_id" : project_id ,"chat": chat_input}
    res = requests.post(
        f"{API_BASE_URL}/evaluations/run",
        json=payload
    )
    return res.json()


def get_evaluation_result(tracking_id):
    res = requests.get(f"{API_BASE_URL}/evaluations/{tracking_id}")
    return res.json()


def get_all_evaluations_for_agent(agent_id):
    res = requests.get(f"{API_BASE_URL}/agents/{agent_id}/evaluations")
    return res.json()


# =========================
# UI
# =========================
st.set_page_config(page_title="Evaluation Manager", layout="wide")

st.title("📊 Evaluation Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "Run New Evaluation",
        "View Evaluation Result",
        "View All Evaluations for Agent",
    ],
)


# =========================
# 1. RUN NEW EVALUATION
# =========================
if menu == "Run New Evaluation":
    st.subheader("🚀 Run New Evaluation")

    agent_id = st.text_input("Agent ID")
    project_id = st.text_input("project ID")
    chat_input = st.text_area("Chat Input (User Query)")

    if st.button("Run Evaluation"):
        if agent_id and chat_input:
            try:
                result = run_evaluation(agent_id, project_id, chat_input)
                st.success("Evaluation started successfully!")
                for dict in result['benchmark_score']:
                    filled = "█" * dict['score']
                    st.write(f"**{dict['dimension']}**")
                    st.write(f"{filled}  **{dict['score']}/10**")
                st.success(f"Overall Score :{result['overall_score']}/{(len(result['benchmark_score']))*10}")
                st.markdown(result['response'])
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID and chat input")


# =========================
# 2. VIEW SINGLE EVALUATION RESULT
# =========================
elif menu == "View Evaluation Result":
    st.subheader("🔍 View Evaluation Result")

    tracking_id = st.text_input("Tracking ID")

    if st.button("Get Result"):
        if tracking_id:
            try:
                result = get_evaluation_result(tracking_id)
                st.success("Evaluation result fetched!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Tracking ID")


# =========================
# 3. VIEW ALL EVALUATIONS FOR AGENT
# =========================
elif menu == "View All Evaluations for Agent":
    st.subheader("📋 All Evaluations for Agent")

    agent_id = st.text_input("Agent ID")

    if st.button("Fetch Evaluations"):
        if agent_id:
            try:
                data = get_all_evaluations_for_agent(agent_id)
                st.success("Evaluations fetched successfully!")

                if isinstance(data, list):
                    st.table(data)
                else:
                    st.json(data)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID")