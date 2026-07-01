import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000" 

# =========================
# API HELPERS
# =========================
def run_evaluation(agent_id,chat_input):
    payload = {"agent_id" : agent_id,"chat": chat_input}
    response = requests.post(f"{API_BASE_URL}/evaluations/run",json=payload)
    response.raise_for_status()
    return response.json()

def get_evaluation_result(tracking_id):
    response = requests.get(f"{API_BASE_URL}/evaluations/{tracking_id}")
    response.raise_for_status()
    return response.json()

def get_all_evaluations_for_agent(agent_id):
    response = requests.get(f"{API_BASE_URL}/agents/{agent_id}/evaluations")
    response.raise_for_status()
    return response.json()

def get_latest_evaluation_for_agent(agent_id):
    response = requests.get(f"{API_BASE_URL}/agents/{agent_id}/evaluations/latest")
    response.raise_for_status()
    return response.json()

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
        "View latest Evaluation of Agent"
    ],
)


# =========================
# 1. RUN NEW EVALUATION
# =========================
if menu == "Run New Evaluation":
    st.subheader("🚀 Run New Evaluation")

    agent_id = st.text_input("Agent ID")
    chat_input = st.text_area("Chat Input (User Query)")

    if st.button("Run Evaluation"):
        if agent_id and chat_input:
            try:
                result = run_evaluation(agent_id, chat_input)
                st.success("Evaluation started successfully!")
                for dict in result['benchmark_score']:
                    filled = "█" * dict['score']
                    st.write(f"**{dict['dimension']}**")
                    st.write(f"{filled}  **{dict['score']}/10**")
                st.success(f"Overall Score :{result['overall_score']}/{(len(result['benchmark_score']))*10}")
                st.header("✅ Response")
                st.subheader("Overall Assessment")
                st.write(result["response"])
                st.header("✅ Detailed Evaluation Result") 
                for out in result["dimensions_results"]:
                    with st.expander(f"📌 {out["dimension"]}", expanded=False):
                        st.metric("Benchmark Score", out["benchmarkScore"])
                        st.markdown("**Reason**")
                        st.write(out["worker_llm_response"]["reason"])
                        if len(out["worker_llm_response"]["chat_issue"])>0 :
                            st.markdown("**Chat Issue**")
                            for chat_issue in out["worker_llm_response"]["chat_issue"]:
                                st.write(chat_issue['evidence'])
                                st.write(chat_issue['explanation'])
                        if len(out["worker_llm_response"]["prompt_issue"]) > 0:
                            st.markdown("**Prompt Issue**")
                            for prompt_issue in out["worker_llm_response"]["prompt_issue"]:
                                st.write(prompt_issue['evidence'])
                                st.write(prompt_issue['explanation'])
                        st.markdown("**Recommended Prompt Improvements**")
                        st.write(out["worker_llm_response"]["recommended_prompt_improvements"])

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
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
                st.header("✅ Response")
                st.write("Tracking_ID : ",result.get('tracking_id',""))
                st.write("Agent_ID : ",result.get("agent_id",""))
                st.write("Prompt_ID : ",result.get("prompt_id",""))
                st.write("Chat : ",result.get("chat",""))
                st.header("✅ Detailed Evaluation Result")
                st.write("Score : ",result.get("score","")) 
                for out in result['output_response']["dimensions_result"]:
                    with st.expander(f"📌 {out["dimension"]}", expanded=False):
                        st.metric("Benchmark Score", out["benchmarkScore"])
                        st.markdown("**Reason**")
                        st.write(out["worker_llm_response"]["reason"])
                        if len(out["worker_llm_response"]["chat_issue"])>0 :
                            st.markdown("**Chat Issue**")
                            for chat_issue in out["worker_llm_response"]["chat_issue"]:
                                st.write(chat_issue['evidence'])
                                st.write(chat_issue['explanation'])
                        if len(out["worker_llm_response"]["prompt_issue"]) > 0:
                            st.markdown("**Prompt Issue**")
                            for prompt_issue in out["worker_llm_response"]["prompt_issue"]:
                                st.write(prompt_issue['evidence'])
                                st.write(prompt_issue['explanation'])
                        st.markdown("**Recommended Prompt Improvements**")
                        st.write(out["worker_llm_response"]["recommended_prompt_improvements"])
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Tracking ID")


# =========================
# 3. VIEW ALL EVALUATIONS FOR AGENT
# =========================
elif menu == "View All Evaluations for Agent":
    st.subheader("📋 ALL Evaluations for Agent")

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

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Agent ID")


# =========================
# 4. VIEW Latest EVALUATION FOR AGENT
# =========================
elif menu == "View latest Evaluation of Agent":
    st.subheader("📋 Latest Evaluations for Agent")

    agent_id = st.text_input("Agent ID")

    if st.button("Fetch Evaluations"):
        if agent_id:
            try:
                result = get_latest_evaluation_for_agent(agent_id)
                st.success("Evaluations fetched successfully!")
                st.success("Evaluation result fetched!")
                st.header("✅ Response")
                st.write("Tracking_ID : ",result.get('tracking_id',""))
                st.write("Agent_ID : ",result.get("agent_id",""))
                st.write("Prompt_ID : ",result.get("prompt_id",""))
                st.write("Chat : ",result.get("chat",""))
                st.header("✅ Detailed Evaluation Result")
                st.write("Score : ",result.get("score","")) 
                for out in result['output_response']["dimensions_result"]:
                    with st.expander(f"📌 {out["dimension"]}", expanded=False):
                        st.metric("Benchmark Score", out["benchmarkScore"])
                        st.markdown("**Reason**")
                        st.write(out["worker_llm_response"]["reason"])
                        if len(out["worker_llm_response"]["chat_issue"])>0 :
                            st.markdown("**Chat Issue**")
                            for chat_issue in out["worker_llm_response"]["chat_issue"]:
                                st.write(chat_issue['evidence'])
                                st.write(chat_issue['explanation'])
                        if len(out["worker_llm_response"]["prompt_issue"]) > 0:
                            st.markdown("**Prompt Issue**")
                            for prompt_issue in out["worker_llm_response"]["prompt_issue"]:
                                st.write(prompt_issue['evidence'])
                                st.write(prompt_issue['explanation'])
                        st.markdown("**Recommended Prompt Improvements**")
                        st.write(out["worker_llm_response"]["recommended_prompt_improvements"])
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Agent ID")