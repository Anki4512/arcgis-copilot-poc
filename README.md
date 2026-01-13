# 🗺️ ArcGIS Copilot (POC)

A Generative AI Assistant that automates ArcGIS Online workflows using Natural Language Processing.

## 🚀 Overview
This tool allows GIS Analysts to perform spatial queries (e.g., *"Find wildfire layers in California"*) using natural language. It acts as a bridge between **Llama 3 (LLM)** and the **Esri ArcGIS API for Python**.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (React-style Dark Mode UI)
* **AI Engine:** LangChain + Ollama (Llama 3 Local Inference)
* **Geospatial:** ArcGIS API for Python (`arcgis`)
* **Security:** "Self-Healing" logic to prevent API hallucinations and credential leaks.

## ✨ Key Features
* **Natural Language to ArcPy:** Translates English commands into executable Python code.
* **Self-Healing Agent:** Middleware that detects invalid code (e.g., fake credentials) and sanitizes it before execution.
* **Interactive Workspace:** Split-screen UI separating Chat (Intent) from Workspace (Execution Logs).

## 📸 Usage
1. Clone the repo.
2. Run `pip install -r requirements.txt`.
3. Launch with `streamlit run app.py`.
