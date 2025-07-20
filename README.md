---
title: Gadget Guide
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
app_port: 8501
tags:
  - streamlit
  - rag
  - llm
  - chatbot
  - firebase
pinned: true
short_description: Electronic Products AI Assistant
license: mit
---



# Gadget Guide: Your Electronic Products AI Assistant 🤖

An intelligent RAG-based chatbot for troubleshooting e-commerce products.


**[>> View the Live Demo Here <<](https://1prarthana14-e-commerce-chatbot.hf.space/)**


App Screenshot

![image/png](https://cdn-uploads.huggingface.co/production/uploads/687bcbbe904a3aafd0f04c29/wJ33AvVQXZgUWGlCLDKOR.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/687bcbbe904a3aafd0f04c29/f_7-bWk68JPbIAZNMWaeE.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/687bcbbe904a3aafd0f04c29/VqtZxxePJMicGuarD0sxu.png)




## 📖 Project Overview

This project is a full-stack web application that leverages Large Language Models (LLMs) to create a conversational AI assistant. The chatbot is equipped with a knowledge base built from product manuals, allowing it to answer specific user questions, provide troubleshooting steps, and offer detailed product support. The system features distinct roles for users and administrators, secure authentication, and persistent, context-aware conversation histories.

## ✨ Key Features

* **👥 Dual-Role System**: Separate interfaces for **Users** (chatting with the bot) and **Admins** (managing the knowledge base).
* **🔐 Secure Authentication**: Robust login system using **Google OAuth 2.0** managed by Firebase Authentication.
* **🧠 Intelligent RAG Pipeline**: Utilizes a FAISS vector store and Sentence Transformer embeddings to retrieve relevant information from product manuals before generating answers.
* **💬 Conversational AI**: Powered by the **Mistral** LLM and managed by the **LangChain** framework for stateful, context-aware conversations.
* **☁️ Persistent, Product-Specific History**: Chat histories are saved for each user and are unique for each product, stored securely in **Cloud Firestore**.
* **🔧 Admin Knowledge Base Management**: Admins can upload new PDF manuals or delete existing ones directly through the UI, with changes reflected instantly.
* **🚀 Deployed & Containerized**: The application is containerized with **Docker** and deployed on **Hugging Face Spaces**.

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend & Auth**: Firebase (Authentication, Firestore)
* **AI / LLM Framework**: LangChain
* **Vector Store**: FAISS (Facebook AI Similarity Search)
* **Embeddings Model**: Sentence Transformers (`intfloat/e5-small-v2`)
* **LLM Provider**: OpenRouter (Mistral 7B)
* **Deployment**: Hugging Face Spaces, Docker
* **Core Language**: Python

## 🚀 Local Setup and Installation

To run this project on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Prarthanaa-G/Gadget_Guide.git
    ```
2.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Up Credentials**
    * Create a file at `.streamlit/secrets.toml` and add your credentials:
        ```toml
        # .streamlit/secrets.toml
        client_id = "YOUR_GOOGLE_CLIENT_ID"
        client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
        admin_emails = ["your.admin@gmail.com"]
        OPENROUTER_API_KEY = "YOUR_OPENROUTER_KEY"
        FIREBASE_JSON_KEY = """
        {
          "type": "service_account",
          ...
        }
        """
        ```
    * Place your Firebase service account JSON file in the root directory for the app to initialize Firebase correctly.

5.  **Run the Streamlit App**
    ```bash
    streamlit run app.py
    ```
