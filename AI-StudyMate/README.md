# AI StudyMate – Adaptive RAG Learning Copilot

A no-API-key adaptive learning app using RAG, FAISS, a public pretrained local LLM, quizzes, knowledge-gap detection, personalized study plans and SQLite learning history.

## Model
Default: `Qwen/Qwen2.5-1.5B-Instruct` from Hugging Face. It is a pretrained instruction model under Apache 2.0; weights are downloaded on first generation. No OpenAI/Gemini key is needed.

https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

Embeddings: `sentence-transformers/all-MiniLM-L6-v2`.

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
First model load can be slow on CPU.

## Trial demo
Upload `data/sample_materials/machine_learning_trial.md`, ask a question, generate a quiz, submit answers, then view Knowledge Gaps and Study Plan.

## Streamlit deployment
Push to GitHub and deploy `app.py` with `requirements.txt`. Free hosted CPU environments can run the app but local 1.5B inference may be slow and model startup downloads several GB. For a reliable college demo, run locally on CPU or use a hosted CPU with enough RAM.

## Core innovation
RAG → Assessment → Knowledge Gap → Personalized Plan → Practice → Updated Progress.
