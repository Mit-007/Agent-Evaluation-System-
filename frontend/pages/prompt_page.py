import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000"  # change this


# =========================
# API HELPERS
# =========================
def create_prompt(agent_id, prompt_text):
    payload = {"prompt": prompt_text}
    res = requests.post(f"{API_BASE_URL}/agents/{agent_id}/prompts", json=payload)
    return res.json()


def get_all_prompts(agent_id):
    res = requests.get(f"{API_BASE_URL}/agents/{agent_id}/prompts")
    return res.json()


def get_latest_prompt(agent_id):
    res = requests.get(f"{API_BASE_URL}/agents/{agent_id}/prompts/latest")
    return res.json()


def get_prompt(prompt_id):
    res = requests.get(f"{API_BASE_URL}/prompts/{prompt_id}")
    return res.json()


# =========================
# UI
# =========================
st.set_page_config(page_title="Prompt Manager", layout="wide")

st.title("📝 Prompt Management Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "Create Prompt",
        "View All Prompts for Agent",
        "View Latest Prompt",
        "View Prompt Details",
    ],
)


# =========================
# 1. CREATE PROMPT
# =========================
if menu == "Create Prompt":
    st.subheader("➕ Create New Prompt for Agent")

    agent_id = st.text_input("Agent ID")
    prompt_text = st.text_area("Enter Prompt")

    if st.button("Create Prompt"):
        if agent_id and prompt_text:
            try:
                result = create_prompt(agent_id, prompt_text)
                st.success("Prompt created successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all fields")


# =========================
# 2. VIEW ALL PROMPTS
# =========================
elif menu == "View All Prompts for Agent":
    st.subheader("📋 All Prompts for Agent")

    agent_id = st.text_input("Agent ID")

    if st.button("Fetch Prompts"):
        if agent_id:
            try:
                data = get_all_prompts(agent_id)
                st.success("Prompts fetched successfully!")

                if isinstance(data,list):
                    st.table(data)
                else:
                    st.json(data)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID")


# =========================
# 3. VIEW LATEST PROMPT
# =========================
elif menu == "View Latest Prompt":
    st.subheader("🆕 Latest Prompt for Agent")

    agent_id = st.text_input("Agent ID")

    if st.button("Get Latest Prompt"):
        if agent_id:
            try:
                result = get_latest_prompt(agent_id)
                st.success("Latest prompt fetched successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID")


# =========================
# 4. VIEW PARTICULAR PROMPT
# =========================
elif menu == "View Prompt Details":
    st.subheader("🔍 View Prompt Details")

    prompt_id = st.text_input("Prompt ID")

    if st.button("Get Prompt"):
        if prompt_id:
            try:
                result = get_prompt(prompt_id)
                st.success("Prompt fetched successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Prompt ID")