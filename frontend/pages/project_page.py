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
def create_project(project_name):
    payload = {"project_name": project_name}
    response = requests.post(f"{API_BASE_URL}/projects", json=payload)
    response.raise_for_status()
    return response.json()


def get_all_projects():
    response = requests.get(f"{API_BASE_URL}/projects")
    response.raise_for_status()
    return response.json()


def get_project(project_id):
    response = requests.get(f"{API_BASE_URL}/projects/{project_id}")
    response.raise_for_status()
    return response.json()

def update_project(project_id , project_new_name):
    payload = {"project_new_name": project_new_name}
    response = requests.put(f"{API_BASE_URL}/projects/{project_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_project(project_id):
    response = requests.delete(f"{API_BASE_URL}/projects/{project_id}")
    response.raise_for_status()
    return response.json()


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
        "Update Project",
        "Delete Project",
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
                st.write("### Project Details")
                st.write(f"**Project ID:** {result['project_id']}")
                st.write(f"**Project Name:** {result['project_name']}")
                st.write(f"**Created At:** {result['created_at']}")

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
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
                st.write("### Project Details")
                st.write(f"**Project ID:** {result['project_id']}")
                st.write(f"**Project Name:** {result['project_name']}")
                st.write(f"**Created At:** {result['created_at']}")

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
# 4. UPDATE PROJECT
# =========================
elif menu == "Update Project":
    st.subheader("✏️ Update Project")

    project_id = st.text_input("Project ID")
    new_name = st.text_input("New Project Name")

    if st.button("Update Project"):
        if project_id and new_name:
            try:
                result = update_project(project_id, new_name)

                st.success("Project updated successfully!")
                st.write(f"**Project ID:** {result['project_id']}")
                st.write(f"**Updated Name:** {result['project_name']}")

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Project ID and New Name")


# =========================
# 5. DELETE PROJECT
# =========================
elif menu == "Delete Project":
    st.subheader("🗑️ Delete Project")

    project_id = st.text_input("Project ID")

    if st.button("Delete Project"):
        if project_id:
            try:
                result = delete_project(project_id)

                st.success("Project deleted successfully!")
                st.write(f"Deleted Project ID: {result.get('project_id')}")
                st.write(f"**Project Name:** {result.get('project_name')}")

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