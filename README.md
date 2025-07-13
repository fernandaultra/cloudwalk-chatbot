# 🤖 CloudWalk Chatbot – RAG Assistant com FAISS + Flask

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de **Data Alchemist** na CloudWalk. Ele implementa um chatbot com **RAG (Retrieval-Augmented Generation)** verdadeiro, utilizando **FAISS** para recuperação semântica de contexto a partir de documentos institucionais da empresa.

---

## 🚀 Funcionalidades

- 🔍 RAG verdadeiro com FAISS + Embeddings da OpenAI
- 📚 Corpus institucional da CloudWalk indexado localmente
- 💬 Interface web com Flask
- 🧠 Respostas contextualizadas com suporte a Markdown
- 🕘 Histórico de conversas
- ☁️ Pronto para deploy via Render ou Railway

---

## 🧠 Arquitetura e Tecnologias

```mermaid
graph TD;
    A[Usuário] --> B[Interface Flask];
    B --> C[Pipeline RAG];
    C --> D[FAISS Index];
    C --> E[OpenAI GPT-3.5];
    D --> F[cloudwalk_corpus.txt];
    E --> G[Resposta com Markdown];
    G --> B;


Exemplos de Conversas
🔹 Exemplo 1
Usuário: O que é a InfinitePay?
Chatbot:

InfinitePay é uma plataforma da CloudWalk no Brasil que oferece uma variedade de soluções de pagamento e serviços financeiros para pequenos e médios negócios. Entre os principais recursos estão:

Maquininhas de cartão

Conta digital PJ

Cashback

Pix ilimitado

Loja online

InfiniteTap
A proposta é facilitar as operações financeiras com tecnologia de ponta, promovendo a inclusão financeira.

🔹 Exemplo 2
Usuário: O que é o projeto Stratus?
Chatbot:

O Stratus é a infraestrutura descentralizada desenvolvida pela CloudWalk baseada em blockchain. Ele conecta comerciantes, consumidores e desenvolvedores em uma rede global, permitindo transações rápidas, seguras e de baixo custo. O Stratus também dá suporte à moeda digital BRLC, usada dentro do ecossistema da CloudWalk.

🔹 Exemplo 3
Usuário: Como a CloudWalk utiliza inteligência artificial?
Chatbot:

A CloudWalk aplica Inteligência Artificial (IA) para criar soluções mais eficientes, personalizadas e escaláveis para o ecossistema financeiro. Entre os usos estão:

Automatização de atendimentos

Análise preditiva de crédito

Customização de experiências de pagamento

Geração de conteúdo para assistentes
Tudo isso alinhado à missão de democratizar o acesso a tecnologias avançadas."


