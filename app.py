import sys

# WARNING: The following two lines are ONLY for Streamlit.
# Remove them from local install!!
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os


# from embedchain import App
from embedchain.pipeline import Pipeline as App

# from embedchain.loaders.github import GithubLoader

@st.cache_resource
def embedchain_bot():
    #loader = GithubLoader(
    #config={
    #    "token":st.secrets["GHPAT_TOKEN"]
    #    }
    #)
    app = App.from_config(config_path="config.yaml")
    
    # Put any github repo you can then refer as templates!
    # app.add("repo:goldzulu/coinweb-hello-world type:repo", data_type="github", loader=loader)
    # pp.add("repo:goldzulu/coinweb-string-processor type:repo", data_type="github", loader=loader)
    
    return app

# Add a sidebar
st.sidebar.title("St Jamie")
st.sidebar.write("Your Friendly AI Club Chatbot!")

st.title("St Jamie")
st.caption("Your Friendly AI Club Chatbot! 🤖")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are St James Senior Girls AI Club ChatBot called StJamie \n
            You primary task is a companion for an AI Club member as they explore and learn about.\n
            all aspects of AI including LLMs, Generative Art, AI assisted game development, AI In game development. Also anything about AI overlapping with blockchain would also help.\n
            Help explain concepts, prepare personalised course plan whenever they want to learn about something. Their age is between 13-18 years old.\n
            Be as friendly as possible and fit into the Gen Z culture if possible while remaining respectful and follow guidelines on UK standards on safe use of computer and safeguarding policies for students.
            """,
            "role": "assistant",
            "content": """
            Hi! I'm StJamie, your St James Senior Girls AI Club Chatbot companion.\n
            I will also be your 2nd brain and memory enhancer on anything you want to learn! \n          
            I can also learn new things regarding coinweb from pdfs, webpages, etc just type\n
            `/add <source>`.\n\n
            I will try my best to learn it and help you with it.\n
            """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    app = embedchain_bot()

    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            app.add(prompt)
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        for response in app.chat(prompt):
            msg_placeholder.empty()
            full_response += response

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
