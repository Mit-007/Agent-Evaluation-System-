import streamlit as st

with st.sidebar:
    if st.button == "Home":
        st.write("🏠 Home Page Content")

    elif st.button == "Project":
        st.switch_page("project_page")

    elif st.button == "Dimensions":
        st.switch_page("dimensions_page")

    elif st.button == "Agent":
        st.switch_page("agent_page")

    elif st.button == "Prompt":
        st.switch_page("prompt_page")

    elif st.button == "Evaluation":
        st.switch_page("evaluation_page")

st.set_page_config(
    page_title="Agent Evaluation System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agent Evaluation System")

st.markdown("""
Welcome to the **Agent Evaluation System**, a platform designed to evaluate the quality,
accuracy, and reliability of AI agents using configurable evaluation dimensions.

This application enables you to manage projects, agents, prompts, and evaluation results
through a simple interface.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Projects", "📁")
    st.write("Organize multiple AI evaluation projects.")

with col2:
    st.metric("Agents", "🤖")
    st.write("Create and manage AI agents for each project.")

with col3:
    st.metric("Prompts", "💬")
    st.write("Maintain prompt versions for every agent.")

st.divider()

st.header("✨ Features")

feature1, feature2 = st.columns(2)

with feature1:
    st.markdown("""
### 📁 Project Management

- Create Projects
- View Project List
- Project Details
""")

    st.markdown("""
### 🤖 Agent Management

- Create Agents
- Update Agents
- Delete Agents
- View Agent Details
""")

    st.markdown("""
### 💬 Prompt Management

- Prompt Versioning
- Latest Prompt
- Prompt History
""")

with feature2:
    st.markdown("""
### 📊 Evaluation

- Run Evaluations
- Store Tracking History
- View Previous Results
""")

    st.markdown("""
### 📏 Evaluation Dimensions

- Instruction Adherence
- Hallucination Detection
- Tool Usage Correctness
- Missing Information Detection
- Policy Violations
- Conversation Quality
""")

    st.markdown("""
### 📈 Analytics

- Dimension-wise Scores
- Overall Score
- Historical Tracking
""")

st.divider()

st.header("📋 Evaluation Workflow")

st.markdown("""
1. **Create a Project**
2. **Create one or more Agents**
3. **Assign Prompts to each Agent**
4. **Configure Evaluation Dimensions**
5. **Run an Evaluation**
6. **View Reports and Analytics**
""")

st.divider()

st.header("🛠 Navigation")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("""
📁 **Projects**

Create and manage evaluation projects.
""")

with c2:
    st.info("""
🤖 **Agents**

Manage AI agents belonging to projects.
""")

with c3:
    st.info("""
💬 **Prompts**

Maintain prompt versions.
""")

c4, c5, c6 = st.columns(3)

with c4:
    st.success("""
📊 **Evaluation**

Run new evaluations.
""")

with c5:
    st.warning("""
📏 **Dimensions**

Configure evaluation dimensions.
""")

st.divider()

st.caption("Agent Evaluation System • Version 1.0")