import os
from dotenv import load_dotenv

# 🔐 Carrega variáveis de ambiente do .env
load_dotenv()

# ✅ Importações atualizadas
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🤖 Inicializa LLM e Embeddings com API Key do .env
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 📁 Caminhos
CORPUS_FILE = "utils/cloudwalk_corpus.txt"
INDEX_PATH = "utils/vector_store/faiss_index"

# 📄 Carrega e divide o corpus em chunks
def load_documents():
    with open(CORPUS_FILE, "r", encoding="utf-8") as file:
        text = file.read()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([text])
    return docs

# 🧠 Cria índice vetorial com FAISS se não existir
def create_vector_store():
    docs = load_documents()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)

# 🔁 Carrega índice FAISS salvo — com permissão para desserialização segura
def load_vector_store():
    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True  # ✅ Corrige o erro do Render
    )

# 💬 Pipeline principal de pergunta e resposta
def ask_question(query):
    if not os.path.exists(INDEX_PATH):
        create_vector_store()
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever()

    # 📝 Prompt com instruções de Markdown
    prompt_inicial = f"""
Responda à pergunta abaixo com linguagem clara e objetiva, usando **Markdown estruturado**:

- Use listas com "-"
- Use **negrito** para destacar
- Organize por tópicos, se necessário
- Evite parágrafos muito longos

📌 Pergunta:
{query}
    """

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    result = qa_chain.run(prompt_inicial)
    return result
