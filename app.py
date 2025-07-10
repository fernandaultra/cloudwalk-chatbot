from flask import Flask, render_template, request, redirect
from utils.rag_pipeline import ask_question

app = Flask(__name__)

# Lista global para manter o histórico da sessão
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form["question"]
        answer = ask_question(question)

        # Salva no histórico
        chat_history.append((question, answer))

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        history=chat_history
    )

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)
