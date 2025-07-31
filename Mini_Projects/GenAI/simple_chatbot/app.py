import streamlit as st
from dotenv import load_dotenv
import os 
from langchain_openai import ChatOpenAI

# Load environ variables 
load_dotenv()

# Default settings of the page
st.set_page_config(page_title="My AI Assistent", page_icon="🗨️" , layout= "centered")

st.title("My smart  AI Assistent")
st.write("Welcome! Im here to help you")

# Initialize the model 
def initialize_model(key):
    try:
        model = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.7, api_key=key)
        return model 
    except Exception as e:
        print(f"Error in initialize model : {e}")
        return None 
        
key = os.getenv("OPENAI_API_KEY")
model = initialize_model(key)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role":"assistent",
        "content":"Hello! How can i help you today."
    }) 

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# User input 
if prompt := st.chat_input("What you want to know about?"):
    # Add user message to chat history 
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })
    
    # Display user message 
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking ....."):
            response = model.invoke(prompt)
            st.write(response.content)
    
    # Add AI response to chat history 
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })
    
    # Sidebar with information 
    with st.sidebar:
        st.header("About this chatbot")
        st.info("This is basic chatbot build using Langchain and OpenAIs GPT models")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.experimental_return()