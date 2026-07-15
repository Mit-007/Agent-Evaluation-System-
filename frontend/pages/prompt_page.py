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
def create_prompt(agent_id, prompt_text):
    payload = {"prompt": prompt_text}
    response = requests.post(f"{API_BASE_URL}/agents/{agent_id}/prompts", json=payload)
    response.raise_for_status()
    return response.json()


def get_all_prompts(agent_id):
    response = requests.get(f"{API_BASE_URL}/agents/{agent_id}/prompts")
    response.raise_for_status()
    return response.json()


def get_latest_prompt(agent_id):
    response = requests.get(f"{API_BASE_URL}/agents/{agent_id}/prompts/latest")
    response.raise_for_status()
    return response.json()


def get_prompt(prompt_id):
    response = requests.get(f"{API_BASE_URL}/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()

def update_prompt(prompt_id,new_prompt):
    payload = {"new_prompt": new_prompt}
    response = requests.put(f"{API_BASE_URL}/prompts/{prompt_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_prompt(prompt_id):
    response = requests.delete(f"{API_BASE_URL}/prompts/{prompt_id}")
    response.raise_for_status()
    return response.json()


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
        "Update Prompt",
        "Delete Prompt",
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
                st.write("### Prompt Details")
                st.write(f"**Prompt ID :** {result['prompt_id']}")
                st.write(f"**Agent ID :** {result['agent_id']}")
                st.write(f"**Prompt :** {result['prompt']}")
                st.write(f"**Version :** {result['version']}")

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
                st.write("### Prompt Details")
                st.write(f"**Prompt ID :** {result['prompt_id']}")
                st.write(f"**Agent ID :** {result['agent_id']}")
                st.write(f"**Prompt :** {result['prompt']}")
                st.write(f"**Version :** {result['version']}")

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
                st.write("### Prompt Details")
                st.write(f"**Prompt ID :** {result['prompt_id']}")
                st.write(f"**Agent ID :** {result['agent_id']}")
                st.write(f"**Prompt :** {result['prompt']}")
                st.write(f"**Version :** {result['version']}")

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter Prompt ID")

# =========================
# 5. UPDATE PROMPT
# =========================
elif menu == "Update Prompt":
    st.subheader("✏️ Update Prompt")

    prompt_id = st.text_input("Prompt ID")
    new_prompt = st.text_area("New Prompt Text")

    if st.button("Update Prompt"):
        if prompt_id and new_prompt:
            try:
                result = update_prompt(prompt_id, new_prompt)

                st.success("Prompt updated successfully!")
                st.write("### Updated Prompt Details")
                st.write(f"**Prompt ID :** {result['prompt_id']}")
                st.write(f"**Agent ID :** {result['agent_id']}")
                st.write(f"**Prompt :** {result['prompt']}")
                st.write(f"**Version :** {result['version']}")

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

        else:
            st.warning("Please enter Prompt ID and New Prompt")

# =========================
# 6. DELETE PROMPT
# =========================
elif menu == "Delete Prompt":
    st.subheader("🗑️ Delete Prompt")

    prompt_id = st.text_input("Prompt ID")

    if st.button("Delete Prompt"):
        if prompt_id:
            try:
                result = delete_prompt(prompt_id)

                st.success("Prompt deleted successfully!")

                if result:
                    st.write("### Deleted Prompt Details")
                    st.write(f"**Prompt ID :** {result['prompt_id']}")
                    st.write(f"**Agent ID :** {result['agent_id']}")
                    st.write(f"**Prompt :** {result['prompt']}")
                    st.write(f"**Version :** {result['version']}")
                else:
                    st.info("No data returned from API")

            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Unknown error")
                except:
                    error = e.response.text

                st.error(error)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

        else:
            st.warning("Please enter Prompt ID")