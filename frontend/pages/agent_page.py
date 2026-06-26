import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000"  # change to your backend URL


# =========================
# API HELPERS
# =========================
def get_agents(project_id):
    res = requests.get(f"{API_BASE_URL}/projects/{project_id}/agents")
    return res.json()


def create_agent(project_id, agent_name):
    payload = {"agent_name": agent_name}
    res = requests.post(f"{API_BASE_URL}/projects/{project_id}/agents", json=payload)
    return res.json()


def get_agent(agent_id):
    res = requests.get(f"{API_BASE_URL}/agents/{agent_id}")
    return res.json()


def update_agent(agent_id, new_name):
    payload = {"agent_new_name": new_name}
    res = requests.put(f"{API_BASE_URL}/agents/{agent_id}", json=payload)
    return res.json()


def delete_agent(agent_id):
    res = requests.delete(f"{API_BASE_URL}/agents/{agent_id}")
    return res.json()


# =========================
# UI
# =========================
st.set_page_config(page_title="Agent Manager", layout="wide")

st.title("🤖 Agent Management Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "List Agents by Project",
        "Create Agent",
        "View Agent Details",
        "Update Agent",
        "Delete Agent",
    ],
)


# =========================
# 1. LIST AGENTS
# =========================
if menu == "List Agents by Project":
    st.subheader("📋 List All Agents in a Project")

    project_id = st.text_input("Enter Project ID")

    if st.button("Fetch Agents"):
        if project_id:
            try:
                data = get_agents(project_id)
                st.success("Agents fetched successfully!")

                if isinstance(data, list):
                    st.table(data)
                else:
                    st.json(data)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Project ID")


# =========================
# 2. CREATE AGENT
# =========================
elif menu == "Create Agent":
    st.subheader("➕ Create New Agent")

    project_id = st.text_input("Project ID")
    agent_name = st.text_input("Agent Name")

    if st.button("Create Agent"):
        if project_id and agent_name:
            try:
                result = create_agent(project_id, agent_name)
                st.success("Agent created successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all fields")


# =========================
# 3. VIEW AGENT DETAILS
# =========================
elif menu == "View Agent Details":
    st.subheader("🔍 View Agent Details")

    agent_id = st.text_input("Agent ID")

    if st.button("Get Agent"):
        if agent_id:
            try:
                result = get_agent(agent_id)
                st.success("Agent details fetched!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID")


# =========================
# 4. UPDATE AGENT
# =========================
elif menu == "Update Agent":
    st.subheader("✏️ Update Agent Name")

    agent_id = st.text_input("Agent ID")
    new_name = st.text_input("New Agent Name")

    if st.button("Update Agent"):
        if agent_id and new_name:
            try:
                result = update_agent(agent_id, new_name)
                st.success("Agent updated successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all fields")


# =========================
# 5. DELETE AGENT
# =========================
elif menu == "Delete Agent":
    st.subheader("🗑️ Delete Agent")

    agent_id = st.text_input("Agent ID")

    if st.button("Delete Agent"):
        if agent_id:
            try:
                result = delete_agent(agent_id)
                st.success("Agent deleted successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Agent ID")