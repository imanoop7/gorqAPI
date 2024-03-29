import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv

load_dotenv() 

groq_api_key = os.environ['GROQ_API_KEY']


embeddings = HuggingFaceEmbeddings()
loader = PyPDFLoader("oops.pdf")
docs =loader.load_and_split()
vector = FAISS.from_documents(docs,embeddings)

llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name='mixtral-8x7b-32768'
    )

prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer.  
<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever =vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

user_input = input("Input your prompt here")

response = retrieval_chain.invoke({"input":user_input})

print(response)


