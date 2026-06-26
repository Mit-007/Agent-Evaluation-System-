import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000"  # change this

# =========================
# API HELPERS
# =========================
def create_project(project_name):
    payload = {"project_name": project_name}
    res = requests.post(f"{API_BASE_URL}/projects", json=payload)
    return res.json()


def get_all_projects():
    res = requests.get(f"{API_BASE_URL}/projects")
    return res.json()


def get_project(project_id):
    res = requests.get(f"{API_BASE_URL}/projects/{project_id}")
    return res.json()


# =========================
# UI
# =========================
st.set_page_config(page_title="Project Manager", layout="wide")

st.title("📁 Project Management Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "Create Project",
        "View All Projects",
        "View Project Details",
    ],
)

# =========================
# 1. CREATE PROJECT
# =========================
if menu == "Create Project":
    st.subheader("➕ Create New Project")

    project_name = st.text_input("Project Name")

    if st.button("Create Project"):
        if project_name:
            try:
                result = create_project(project_name)
                st.success("Project created successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter project name")


# =========================
# 2. VIEW ALL PROJECTS
# =========================
elif menu == "View All Projects":
    st.subheader("📋 All Projects")

    if st.button("Fetch Projects"):
        try:
            data = get_all_projects()
            st.success("Projects fetched successfully!")

            if isinstance(data, list):
                st.table(data)
            else:
                st.json(data)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# 3. VIEW SINGLE PROJECT
# =========================
elif menu == "View Project Details":
    st.subheader("🔍 View Project Details")

    project_id = st.text_input("Project ID")

    if st.button("Get Project"):
        if project_id:
            try:
                result = get_project(project_id)
                st.success("Project fetched successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Project ID")