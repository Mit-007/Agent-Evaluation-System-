import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://localhost:8000" 

# ========================= 
# API HELPERS
# =========================
def set_project_dimensions(project_id, dim_list):
    payload = {"dimensions_list": dim_list}
    response = requests.post(f"{API_BASE_URL}/projects/{project_id}/dimensions",json=payload)
    response.raise_for_status()
    return response.json()


def get_project_dimensions(project_id):
    response = requests.get(f"{API_BASE_URL}/projects/{project_id}/dimensions")
    response.raise_for_status()
    return response.json()

# =========================
# UI
# =========================
st.set_page_config(page_title="Dimensions Manager", layout="wide")

st.title("📐 Project Dimensions Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "Set Project Dimensions",
        "View All Project Dimensions"
    ],
)

# =========================
# 1. SET PROJECT DIMENSIONS 
# =========================
if menu == "Set Project Dimensions":
    st.subheader("➕ Set Project Dimensions")

    project_id = st.text_input("Project ID")

    if "dim_list" not in st.session_state:
        st.session_state.dim_list = []

    dimension_name = st.text_input("Dimension Name")
    dimension_description = st.text_input("Dimension Description")

    if st.button("Add Dimension"):
        if dimension_name and dimension_description:
            st.session_state.dim_list.append(
                {
                    "dimension_name": dimension_name.strip(),
                    "dimension_description": dimension_description.strip()
                }
            )

    if st.session_state.dim_list:
        st.write("### Added Dimensions")
        st.json(st.session_state.dim_list)

    if st.button("Save Dimensions"):
        if project_id and st.session_state.dim_list:
            try:
                result = set_project_dimensions(
                    project_id,
                    st.session_state.dim_list
                )

                st.write(result['message'])

                data = result['list_of_all_project_dimensions']
                if isinstance(data, list):
                    st.table(data)
                else:
                    st.json(data)

                # Clear list after saving
                st.session_state.dim_list = []

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Project ID and add at least one dimension.")


# =========================
# 2. VIEW ALL DIMENSIONS
# =========================
elif menu == "View All Project Dimensions":
    st.subheader("📋 Project Dimensions")

    project_id = st.text_input("Project ID")

    if st.button("Fetch Dimensions"):
        if project_id:
            try:
                result = get_project_dimensions(project_id)

                st.success("Dimensions fetched successfully!")

                if isinstance(result, list):
                    st.table(result)
                else:
                    st.json(result)

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
