# 📄 Chat With Any PDF (RAG Pipeline)

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live%20Demo-blue)](https://huggingface.co/spaces/Mutahir1717/Chat-With-Any-PDF)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange)](https://www.gradio.app/)

A local **Retrieval-Augmented Generation (RAG)** application that allows users to perform semantic search and Q&A on unstructured PDF documents without relying on paid APIs like OpenAI.

## 🚀 Features
* **Privacy First:** Runs entirely on CPU/GPU without sending data to external paid APIs.
* **Model:** Uses `MBZUAI/LaMini-T5-738M` for high-quality, efficient text generation.
* **Vector DB:** Uses **ChromaDB** for fast semantic retrieval.
* **User Interface:** Built with **Gradio** for a clean, chat-like experience.

## 🛠️ Tech Stack
* **LLM:** LaMini-T5 (738M parameters)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Orchestration:** LangChain / Custom Python Pipeline
* **Frontend:** Gradio

## 📦 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/Mutahir1717/Chat-With-PDF-RAG.git](https://github.com/Mutahir1717/Chat-With-PDF-RAG.git)
