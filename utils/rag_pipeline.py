import os
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document

# Inicializa o modelo e embeddings
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# Caminhos
CORPUS_FILE = "utils/cloudwalk_corpus.txt"
INDEX_PATH = "utils/vector_store/faiss_index"

# Função para carregar documentos
def load_documents():
    with open(CORPUS_FILE, "r", encoding="utf-8") as file:
        text = file.read()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([text])
    return docs

# Cria o vetor FAISS se não existir
def create_vector_store():
    docs = load_documents()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)

# Carrega o FAISS já salvo
def load_vector_store():
    return FAISS.load_local(INDEX_PATH, embeddings)

# Pipeline de pergunta e resposta
def ask_question(query):
    if not os.path.exists(INDEX_PATH):
        create_vector_store()
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)
    result = qa_chain.run(query)
    return result
