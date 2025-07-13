import sys
import os
import pytest

# Garante que o diretório raiz do projeto esteja no sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.rag_pipeline import ask_question

@pytest.mark.parametrize("question, expected_keywords", [
    ("O que é InfinitePay?", ["infinitepay", "pagamentos", "maquininha"]),
    ("O que é o InfiniteTap?", ["tap", "smartphone", "maquininha"]),
])
def test_relevant_answers(question, expected_keywords):
    answer = ask_question(question)
    assert isinstance(answer, str)
    assert any(keyword in answer.lower() for keyword in expected_keywords)

def test_empty_question():
    question = ""
    answer = ask_question(question)
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0  # Espera-se alguma resposta útil mesmo em branco
