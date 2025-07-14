from flask import Flask, render_template, request, redirect
from utils.rag_pipeline import ask_question
from markdown import markdown
from markupsafe import Markup
import os  # ✅ Importa o os para ler a variável de ambiente PORT

app = Flask(__name__)

# Lista global para manter o histórico da sessão
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer_html = None

    if request.method == "POST":
        question = request.form["question"]
        resposta = ask_question(question)

        # ✅ Converte a resposta em HTML (renderiza Markdown)
        answer_html = Markup(markdown(resposta))

        # Salva no histórico
        chat_history.append((question, answer_html))

    return render_template(
        "index.html",
        question=question,
        answer=answer_html,
        history=chat_history
    )

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    return redirect("/")

# ✅ Configura porta dinâmica para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
