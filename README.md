# 🧠 NLP Studio — Hugging Face Pipeline App

An interactive Streamlit app powered by 🤗 Hugging Face Transformers featuring **three** production-ready NLP pipelines.

---

## 🚀 Pipelines Included

| Pipeline | Model | What it does |
|---|---|---|
| **Sentiment Analysis** | `distilbert-base-uncased-finetuned-sst-2-english` | Classifies text as POSITIVE or NEGATIVE with confidence score |
| **Text Generation** | `distilgpt2` | Continues any prompt with controllable length & temperature |
| **Question Answering** | `distilbert-base-cased-distilled-squad` | Extracts precise answers from a given context paragraph |

---

## 🛠 Local Setup

```bash
# 1. Clone / download the project
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repo & `app.py`
4. Click **Deploy** — done! Share the URL 🎉

> Models are downloaded automatically on first run and cached by Streamlit's `@st.cache_resource`.

---

## 📁 File Structure

```
.
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🎨 Design Highlights

- Dark-mode UI with a bold typographic system (Syne + DM Mono)
- Lime-green / cyan accent palette  
- Animated confidence bars on results
- Responsive pipeline selector with radio tabs
- Built-in example prompts for quick demos
