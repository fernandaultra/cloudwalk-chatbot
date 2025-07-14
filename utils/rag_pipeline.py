import os
from dotenv import load_dotenv

# 🔐 Carrega variáveis de ambiente do .env
load_dotenv()

# ✅ Importações atualizadas e compatíveis com LangChain 0.1+
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🤖 Inicializa LLM e Embeddings com API Key
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
    return splitter.create_documents([text])

# 🧠 Cria índice vetorial com FAISS se ainda não existir
def create_vector_store():
    docs = load_documents()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)

# 🔁 Carrega índice FAISS salvo
def load_vector_store():
    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

# 💬 Pipeline principal de pergunta e resposta
def ask_question(query):
    # ⚠️ Verifica se o índice existe
    if not os.path.exists(INDEX_PATH):
        create_vector_store()

    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever()

    # 📝 Prompt com Markdown estruturado
    prompt_inicial = f"""
Responda à pergunta abaixo com clareza e organização, seguindo estas instruções:

- Use **negrito** para destacar conceitos importantes
- Liste benefícios ou itens com `-`
- Quando citar links, use a sintaxe: [Texto do link](https://exemplo.com)
- Evite blocos grandes de texto corrido. Use tópicos!

📌 Pergunta:
{query}
    """

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    resposta = qa_chain.run(prompt_inicial)
    return resposta
