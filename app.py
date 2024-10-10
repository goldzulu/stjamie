import sys
import time
from chromadb.errors import ChromaError  # Change this line
import logging

logging.basicConfig(level=logging.INFO)

# Define the version number as a constant
VERSION = "1.3"

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
    try:
        client = app.db.client
        collections = client.list_collections()
        for collection in collections:
            client.delete_collection(collection.name)
        st.session_state.db_initialized = False  # Reset the initialization flag
        return "Database reset successfully. All collections have been deleted."
    except Exception as e:
        return f"Error resetting database: {str(e)}"

def init_database(app):
    logging.info("Starting init_database function")
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
    
    successful_sources = 0
    failed_sources = []
    skipped_sources = []
    
    for i, source in enumerate(sources):
        status_text.text(f"Initializing database: processing source {i+1} of {total_sources}")
        try:
            logging.info(f"Processing source: {source}")
            app.add(source, data_type="web_page")
            successful_sources += 1
            st.success(f"Successfully added: {source}")
            logging.info(f"Successfully added: {source}")
        except Exception as e:
            failed_sources.append((source, str(e)))
            st.error(f"Error adding source {source}: {str(e)}")
            logging.error(f"Error adding source {source}: {str(e)}", exc_info=True)
        progress_bar.progress((i + 1) / total_sources)
        time.sleep(0.1)  # Small delay to make the progress visible
    
    progress_bar.empty()
    status_text.empty()
    
    summary = f"Database initialization completed.\n"
    summary += f"Successfully added: {successful_sources}\n"
    summary += f"Failed to add: {len(failed_sources)}\n"
    summary += f"Total sources processed: {total_sources}"
    
    if failed_sources:
        st.warning("Some sources failed to add. Check the errors above for details.")
    
    logging.info(f"init_database completed. Summary: {summary}")
    return summary

def get_source_list(app):
    logging.info("Starting get_source_list function")
    try:
        all_sources = set()  # Use a set to avoid duplicates
        
        # Get all documents from the database
        try:
            logging.info("Attempting to get documents from the database")
            documents = app.db.get(limit=1000000)  # Set a high limit to get all documents
            logging.info(f"Retrieved documents from the database: {documents}")
        except StopIteration:
            logging.warning("No documents found in the database (StopIteration)")
            return "The database is currently empty. You may need to initialize the database using '/db init'."
        except Exception as e:
            logging.error(f"Error retrieving documents: {str(e)}", exc_info=True)
            return f"An error occurred while retrieving documents: {str(e)}"
        
        if not documents or 'metadatas' not in documents or not documents['metadatas']:
            logging.warning("No documents or metadata found in the database")
            return "The database is currently empty. You may need to initialize the database using '/db init'."
        
        # Extract unique URLs from the metadata
        for metadata in documents['metadatas']:
            url = metadata.get('url')
            if url:
                all_sources.add(url)
        
        logging.info(f"Found {len(all_sources)} unique sources")
        
        if all_sources:
            source_list = "\n".join([f"- {source}" for source in sorted(all_sources)])
            response = f"Here's the list of sources currently in the database:\n\n{source_list}"
        else:
            response = "No sources found in the database. You may need to initialize the database using '/db init'."
        
        logging.info(f"Returning response: {response[:100]}...")  # Log first 100 characters of response
        return response
    except Exception as e:
        logging.error(f"Error in get_source_list: {str(e)}", exc_info=True)
        return f"An error occurred while retrieving the sources: {str(e)}"

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

# Update the title to use the VERSION constant
st.title(f"St Jamie v{VERSION}")
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
            
            response = get_source_list(app)
            
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
                
                # Reinitialize the app after populating the database
                st.session_state.app = None
                st.session_state.db_initialized = False
                app = embedchain_bot()
                
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