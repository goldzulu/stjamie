import sys
import time
from chromadb.errors import ChromaError  # Change this line

# WARNING: The following two lines are ONLY for Streamlit.
# Remove them from local install!!
try:
    sys.modules['sqlite3'] = __import__('pysqlite3')
    sys.modules.pop('pysqlite3')
except ImportError:
    # pysqlite3 is not available, do nothing or handle the situation
    pass

import streamlit as st
import os
from chromadb.config import Settings
from streamlit.components.v1 import html  # Add this import

# from embedchain import App
from embedchain.pipeline import Pipeline as App

# from embedchain.loaders.github import GithubLoader

# Initialize session state variables
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False

if 'app' not in st.session_state:
    st.session_state.app = None

@st.cache_resource
def embedchain_bot():
    if st.session_state.app is None:
        try:
            app = App.from_config(config_path="config.yaml")
            # Try to access the database to check if it's properly initialized
            app.db.get(where={}, limit=1)
            st.session_state.app = app
            st.session_state.db_initialized = True
        except (ChromaError, StopIteration) as e:
            st.warning(f"Database not properly initialized: {str(e)}. Initializing...")
            app = App.from_config(config_path="config.yaml")
            init_database(app)
            st.session_state.app = app
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"Error initializing database: {str(e)}")
            st.session_state.app = None
            st.session_state.db_initialized = False
    return st.session_state.app

def reset_database(app):
    client = app.db.client
    collections = client.list_collections()
    for collection in collections:
        client.delete_collection(collection.name)
    return "Database reset successfully. All collections have been deleted."

def init_database(app):
    # Add the KaPlay sources to the knowledge base
    sources = [
        "https://kaplayjs.com/guides/creating_your_first_game/",
        "https://kaplayjs.com/guides/starting/",
        "https://kaplayjs.com/guides/components/",
        "https://kaplayjs.com/guides/sprites/",
        "https://kaplayjs.com/guides/audio/",
        "https://kaplayjs.com/guides/input/",
        "https://kaplayjs.com/guides/debug_mode/",
        "https://kaplayjs.com/guides/optimization/",
        "https://kaplayjs.com/guides/pathfinding/",
        "https://kaplayjs.com/guides/physics/",
        "https://kaplayjs.com/guides/shaders/",
        "https://kaplayjs.com/doc/kaplay/"
    ]
    
    total_sources = len(sources)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, source in enumerate(sources):
        status_text.text(f"Initializing database: adding source {i+1} of {total_sources}")
        try:
            app.add(source, data_type="web_page")
        except Exception as e:
            st.error(f"Error adding source {source}: {str(e)}")
        progress_bar.progress((i + 1) / total_sources)
        time.sleep(0.1)  # Small delay to make the progress visible
    
    progress_bar.empty()
    return f"Database initialized with {total_sources} KaPlay sources."

def get_source_list(app):
    try:
        client = app.db.client
        collections = client.list_collections()
        
        all_sources = []
        for collection in collections:
            try:
                coll = client.get_collection(collection.name)
                results = coll.get()
                
                for i, meta in enumerate(results['metadatas']):
                    url = meta.get('url', 'No URL available')
                    if url == 'No URL available':
                        description = f"Source {i+1}: "
                        description += f"Type: {meta.get('data_type', 'Unknown')} | "
                        description += f"Chunk: {meta.get('chunk_id', 'Unknown')} | "
                        for key, value in meta.items():
                            if key not in ['url', 'data_type', 'chunk_id']:
                                description += f"{key}: {value} | "
                        all_sources.append(description.rstrip(' | '))
                    else:
                        all_sources.append(url)
            except Exception as e:
                st.error(f"Error accessing collection {collection.name}: {str(e)}")
        
        return all_sources
    except Exception as e:
        st.error(f"Error retrieving sources: {str(e)}")
        return []

# Add this function to handle the help command
def get_help_message():
    return """
    Available commands:
    /help - Show this help message
    /add <source> - Add a new source to the knowledge base (e.g., /add https://example.com)
    /list - List all sources currently in the database
    /db reset - Reset the database (delete all data)
    /db init - Initialize the database with default KaPlay sources
    
    You can also ask me anything about AI, game development, or related topics!
    """

# Add a sidebar
st.sidebar.title("St Jamie")
st.sidebar.write("Your Friendly AI Club Chatbot!")

# Add the Photo Editor link
st.sidebar.markdown("---")  # Add a separator
st.sidebar.markdown("### Tools")
photo_editor_html = '<a href="https://www.photopea.com/" target="_blank">Photo Editor</a>'
st.sidebar.markdown(photo_editor_html, unsafe_allow_html=True)

st.title("St Jamie v1.2")
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
            You are also to help them write games. If not specified, use KaPlayJS v3001 as the javascript game engine. Help them write code for their games step by step. Help them fix code if needed.\n
            They might want to also explore writing simple webpages. If not specified, produce as much as possible a single page that can be run in a browser and they can copy and paste to any static hosting server.\n
            Use Tailwind css for css styling unless specified otherwise.\n
            Any external webpage dependencies needed must be loaded\n
            from CDN e.g. for tailwind unless specified, use <script src='https://cdn.tailwindcss.com'></script>\n
            Be as friendly as possible and fit into the Gen Z culture if possible while remaining respectful and follow guidelines on UK standards on safe use of computer and safeguarding policies for students.
            """,
            "role": "assistant",
            "content": """
            Hi! I'm StJamie, your St James Senior Girls AI Club Chatbot companion.\n
            I'm here to help you learn about AI, game development, and more! 🚀\n
            You can ask me anything, and I'll do my best to assist you.\n
            To see available commands, type `/help`.\n
            You can also add new sources to my knowledge base using the `/add` command.\n
            Let's start exploring the exciting world of AI together!
            """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

app = embedchain_bot()

if app is None:
    st.error("Failed to initialize the application. Please check the logs and try again.")
    st.stop()

# Check if the database is empty and initialize if needed
if not st.session_state.db_initialized:
    st.info("Database is being initialized. Please wait...")
    init_message = init_database(app)
    st.success(init_message)
    st.session_state.db_initialized = True

if prompt := st.chat_input("Ask me anything!"):
    if not st.session_state.db_initialized:
        st.warning("Database initialization is still in progress. Please wait and try again.")
        st.stop()

    if prompt.startswith("/help"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            help_message = get_help_message()
            st.markdown(help_message)
            st.session_state.messages.append({"role": "assistant", "content": help_message})
        st.stop()

    elif prompt.startswith("/add"):
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

    elif prompt.startswith("/list"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Fetching the list of sources...")
            
            sources = get_source_list(app)
            if sources:
                source_list = "\n".join([f"- {source}" for source in sources])
                response = f"Here's the list of sources currently in the database:\n\n{source_list}"
            else:
                response = "The database is currently empty or there was an error retrieving the sources. You may need to initialize the database using '/db init'."
            
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.stop()

    elif prompt.startswith("/db"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Extract the parameter
        param = prompt.replace("/db", "").strip()
        
        if param.lower() == "reset":
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Resetting the database...")
                
                reset_message = reset_database(app)
                
                message_placeholder.markdown(reset_message)
                st.session_state.messages.append({"role": "assistant", "content": reset_message})
                
                # Reinitialize the app after reset
                app = embedchain_bot()
        elif param.lower() == "init":
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Initializing the database...")
                
                init_message = init_database(app)
                
                message_placeholder.markdown(init_message)
                st.session_state.messages.append({"role": "assistant", "content": init_message})
        else:
            with st.chat_message("assistant"):
                error_message = "Invalid command. Use '/db reset' to reset the database or '/db init' to initialize it with KaPlay sources."
                st.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.stop()

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        try:
            for response in app.chat(prompt):
                msg_placeholder.empty()
                full_response += response

            msg_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            error_message = f"An error occurred while processing your request: {str(e)}"
            msg_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})