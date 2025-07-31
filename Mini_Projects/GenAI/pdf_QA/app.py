import os

import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Get text from pdf 
def extract_text_from_pdf(pdf_file):
    if pdf_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error in get pdf: {e}")
            return None
    return None

# Create vector store 
def create_knowladge_base(text):
    # Split text into chunks 
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap = 50)
    chunks = text_spliter.split_text(text)
    
    # Create embeddings 
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    knowladge_base = FAISS.from_texts(chunks, embeddings)
    
    return knowladge_base

def main():
    st.header("My Research Helper")
    st.write("Upload a PDF and ask questions about its content ")
    
    # file upload
    pdf_file = st.file_uploader("Upload Your PDF", type="pdf")
    
    if pdf_file is not None:
        # Extract text 
        with st.spinner("Rendering PDF"):
            text = extract_text_from_pdf(pdf_file)
        
        if text:
            # Create knowladgebase 
            with st.spinner("Processing Document...."):
                knowladge_base = create_knowladge_base(text)
            
            st.success("PDF processed scussfully !")
            
            # Question input 
            user_question = st.text_input("Ask your Question")
            
            if user_question:
                with st.spinner("Finding Answer ...."):
                    retriver = knowladge_base.as_retriever()
                
                system_prompt = (
                    "You are expert Researcher who explains hard consepts very clearly "
                    "Use real life anologies to explain consepts"
                    "Add Simple examples and usecases to demostrate"
                    "Context:{context}"
                )
                
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        ("human","{input}")
                    ]
                )
                
                key = os.getenv("OPENAI_API_KEY")
                model = ChatOpenAI(api_key=key)
                
                QA_chain = create_stuff_documents_chain(model, prompt)
                chain = create_retrieval_chain(retriver,QA_chain)
                
                response = chain.invoke({"input":user_question})
                
                st.write("**Answer**")
                st.write(response['answer']) 
    else:
        st.error("Can't Extract text from PDF")
if __name__ == "__main__":
    main()
       
    

