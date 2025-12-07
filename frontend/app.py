"""
Chat App for Langgraph Agents using Streamlit.

Final fixed version:
- Streaming stays visible after rerun
- No raw message dict displayed
- Only clean assistant text appears
- Works with LangGraph thread state + message_history
"""

import streamlit as st
from api import (
    get_assistants,
    create_thread,
    search_threads,
    get_thread_state,
    run_thread_stream,
    delete_thread,
)
import yaml
from pathlib import Path
import os


#################################
# LLM Config Loading
#################################

CONFIG_PATH = os.path.join(Path(os.getcwd()).parent, "LLM_CONFIG.yaml")


def load_llm_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for llm_type, params in config["llms"].items():
        if params.get("enabled"):
            llm_config = {"llm_type": llm_type}
            llm_config.update({k: v for k, v in params.items() if k != "enabled"})
            return llm_config

    raise ValueError("No enabled LLM found in config.")


#################################
# Session State Management
#################################

def initialize_session_state(user_id: str):

    if "user_id" not in st.session_state:
        st.session_state.user_id = user_id

    if "assistants" not in st.session_state:
        assistants_list = get_assistants()
        st.session_state.assistants = {
            assistant["name"]: assistant["assistant_id"] for assistant in assistants_list
        }

    if "active_assistant_id" not in st.session_state:
        st.session_state.active_assistant_id = list(st.session_state.assistants.values())[0]

    if "thread_ids" not in st.session_state:
        threads = search_threads(st.session_state.user_id)
        st.session_state.thread_ids = [t["thread_id"] for t in threads]

    if "selected_thread_id" not in st.session_state:
        st.session_state.selected_thread_id = (
            st.session_state.thread_ids[-1] if st.session_state.thread_ids else None
        )

    if "thread_state" not in st.session_state:
        st.session_state.thread_state = {}

    if "message_history" not in st.session_state:
        st.session_state.message_history = {}  # store streamed messages


def create_new_thread(user_id: str):
    thread = create_thread(user_id)
    thread_id = thread["thread_id"]

    st.session_state.thread_ids.append(thread_id)
    st.session_state.thread_state = get_thread_state(thread_id)

    st.session_state.message_history[thread_id] = []
    st.session_state.selected_thread_id = thread_id
    st.rerun()


def delete_thread_and_update_state(thread_id: str):
    delete_thread(thread_id)

    if thread_id in st.session_state.thread_ids:
        st.session_state.thread_ids.remove(thread_id)

    if thread_id in st.session_state.message_history:
        del st.session_state.message_history[thread_id]

    st.session_state.thread_state = {}
    st.rerun()


#################################
# Initialize
#################################

initialize_session_state(user_id="fays")


#################################
# Sidebar UI
#################################

with st.sidebar:
    st.write("User ID: " + st.session_state.user_id)

    assistant = st.selectbox(
        "Select Assistant",
        list(st.session_state.assistants.keys())
    )
    st.session_state.active_assistant_id = st.session_state.assistants[assistant]

    st.title("Conversations")

    if st.button("Create New Conversation"):
        create_new_thread(st.session_state.user_id)

    def _on_select_thread():
        st.session_state.thread_state = get_thread_state(st.session_state.selected_thread_id)

    if st.session_state.thread_ids:
        st.radio(
            "Select Conversation",
            options=st.session_state.thread_ids,
            format_func=lambda tid: tid[:8],
            key="selected_thread_id",
            on_change=_on_select_thread,
        )

    if st.button("Delete Conversation", type="primary"):
        if st.session_state.selected_thread_id:
            delete_thread_and_update_state(st.session_state.selected_thread_id)


#################################
# Main Chat UI
#################################

st.title(f"Chatting with {assistant}")

selected_thread = st.session_state.selected_thread_id

if selected_thread:
    st.session_state.thread_state = get_thread_state(selected_thread)


#################################
# 1️⃣ SHOW MESSAGES FROM THREAD_STATE
#################################

if st.session_state.thread_state:
    values = st.session_state.thread_state.get("values", {})

    # User question (from LangGraph state)
    if values.get("question"):
        with st.chat_message("user"):
            st.markdown(values["question"])

    # Assistant prediction (cleaned)
    if values.get("model_prediction"):
        pred = values["model_prediction"]

        # Extract only clean content
        if isinstance(pred, str):
            content = pred
        elif hasattr(pred, "content"):
            content = pred.content
        elif isinstance(pred, dict) and "content" in pred:
            content = pred["content"]
        else:
            content = None

        if content:
            with st.chat_message("assistant"):
                st.markdown(content)


#################################
# 2️⃣ SHOW STREAMED MESSAGES (NOT YET SAVED IN THREAD_STATE)
#################################

if selected_thread in st.session_state.message_history:
    for msg in st.session_state.message_history[selected_thread]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


#################################
# 3️⃣ USER INPUT → STREAM RESPONSE
#################################

if prompt := st.chat_input("Send a message..."):

    # Show user's message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    if selected_thread not in st.session_state.message_history:
        st.session_state.message_history[selected_thread] = []

    # STREAMING
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        llm_config = load_llm_config(CONFIG_PATH)
        input_data = {"question": prompt, "llm_config": llm_config}

        stream = run_thread_stream(
            st.session_state.active_assistant_id,
            selected_thread,
            input_data
        )

        for chunk in stream:
            full_response += str(chunk)
            placeholder.markdown(full_response)

    # Save streamed assistant message locally
    st.session_state.message_history[selected_thread].append({
        "role": "assistant",
        "content": full_response
    })

    st.rerun()


#################################
# Debug
#################################

with st.expander("<DEBUG> Session State"):
    st.write(st.session_state)
