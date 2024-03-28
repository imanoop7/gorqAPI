import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
import time
from dotenv import load_dotenv

load_dotenv()  #

groq_api_key = os.environ['GROQ_API_KEY']


embeddings = OllamaEmbeddings()
loader = WebBaseLoader("https://paulgraham.com/greatwork.html")
docs = st.session_state.loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = st.session_state.text_splitter.split_documents( st.session_state.docs)
vector = FAISS.from_documents(st.session_state.documents, st.session_state.embeddings)

llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name='mixtral-8x7b-32768'
    )

prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer. 
I will tip you $200 if the user finds the answer helpful. 
<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever =vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

prompt = input("Input your prompt here")
