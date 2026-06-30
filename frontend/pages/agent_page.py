import streamlit as st
import requests
import pandas as pd

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000"  


# =========================
# API HELPERS
# =========================
def get_agents(project_id):
    response= requests.get(f"{API_BASE_URL}/projects/{project_id}/agents")
    response.raise_for_status()
    return response.json()


def create_agent(project_id, agent_name):
    payload = {"agent_name": agent_name}
    response= requests.post(f"{API_BASE_URL}/projects/{project_id}/agents", json=payload)
    response.raise_for_status()
    return response.json()


def get_agent(agent_id):
    response= requests.get(f"{API_BASE_URL}/agents/{agent_id}")
    response.raise_for_status()
    return response.json()


def update_agent(agent_id, new_name):
    payload = {"agent_new_name": new_name}
    response= requests.put(f"{API_BASE_URL}/agents/{agent_id}", json=payload)
    response.raise_for_status()
    return response.json()


def delete_agent(agent_id):
    response= requests.delete(f"{API_BASE_URL}/agents/{agent_id}")
    response.raise_for_status()
    return response.json()


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
                st.markdown("### 🗂️ Agents Table")

                # If data is a list or tuple, display as a table
                if "columns" in data and "rows" in data:
                    df = pd.DataFrame(data["rows"], columns=data["columns"])
                    st.table(df)         
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
                st.write("### Agent Details")
                st.write(f"**Agent ID:** {result['agent_id']}")
                st.write(f"**Agent Name:** {result['agent_name']}")
                st.write(f"**Project ID:** {result['project_id']}")
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
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
                st.write("### Agent Details")
                st.write(f"**Agent ID:** {result['agent_id']}")
                st.write(f"**Agent Name:** {result['agent_name']}")
                st.write(f"**Project ID:** {result['project_id']}")
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
                st.write("### Agent Details")
                st.write(f"**Agent ID:** {result['agent_id']}")
                st.write(f"**Agent Name:** {result['agent_name']}")
                st.write(f"**Project ID:** {result['project_id']}")
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
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
                st.write("### Agent Details")
                st.write(f"**Agent ID:** {result['agent_id']}")
                st.write(f"**Agent Name:** {result['agent_name']}")
                st.write(f"**Project ID:** {result['project_id']}")
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