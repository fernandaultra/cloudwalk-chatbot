import openai
import os
import markdown

# Inicializa o cliente OpenAI com sua chave
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carrega o corpus com informações da CloudWalk
with open("data/cloudwalk_corpus.txt", "r", encoding="utf-8") as file:
    context = file.read()

def ask_question(question):
    """
    Usa Retrieval-Augmented Generation simples com contexto estático do arquivo.
    Gera uma resposta do modelo da OpenAI com suporte a Markdown.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ou gpt-4, se você tiver acesso
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente da CloudWalk. "
                    "Responda de forma clara e didática, usando Markdown sempre que possível "
                    "(**negrito**, *itálico*, listas, links etc). Use linguagem natural. "
                    "Baseie-se no contexto abaixo:\n\n"
                    + context
                ),
            },
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=800,
    )

    answer = response.choices[0].message.content
    return markdown.markdown(answer)

