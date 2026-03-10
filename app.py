import streamlit as st
from transformers import pipeline
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NLP Studio",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:        #0b0c0f;
    --surface:   #13151a;
    --border:    #23262e;
    --accent:    #c8f135;
    --accent2:   #5ee7ff;
    --text:      #e8eaf0;
    --muted:     #5a5e6b;
    --radius:    12px;
}

/* global reset */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    background: var(--accent);
    color: #0b0c0f;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: clamp(2.4rem, 7vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin: 0 0 0.5rem;
}
.hero h1 span { color: var(--accent); }
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    max-width: 420px;
    margin: 0 auto;
}

/* ── Pipeline cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 2rem 0;
}
.p-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem;
    cursor: pointer;
    transition: border-color .2s, transform .15s;
    text-align: center;
}
.p-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.p-card.active {
    border-color: var(--accent);
    background: linear-gradient(135deg, #1a1f0a 0%, #13151a 100%);
}
.p-card .icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.p-card .label { font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em; color: var(--text); }

/* ── Input area ── */
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    resize: vertical !important;
    transition: border-color .2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,241,53,.08) !important;
}
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,241,53,.08) !important;
}

/* ── Run button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0b0c0f !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: opacity .15s, transform .1s !important;
    cursor: pointer !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Result card ── */
.result-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem;
    margin-top: 1.4rem;
    position: relative;
    overflow: hidden;
}
.result-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 2px 2px 0 0;
}
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
.result-main {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.result-main.positive { color: var(--accent); }
.result-main.negative { color: #ff6b6b; }
.result-main.neutral  { color: var(--accent2); }
.result-main.generated { font-size: 1rem; font-weight: 400; font-family: 'DM Mono', monospace; color: var(--text); line-height: 1.7; }

.conf-bar-bg {
    height: 6px;
    background: var(--border);
    border-radius: 100px;
    margin-top: 0.6rem;
    overflow: hidden;
}
.conf-bar {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.6s cubic-bezier(.4,0,.2,1);
}

/* ── Selectbox & slider ── */
.stSelectbox > div > div,
.stSlider { color: var(--text) !important; }

/* ── Section label ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 1.6rem 0;
}

/* ── Model chip ── */
.model-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--border);
    border-radius: 100px;
    padding: 3px 12px 3px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    margin-top: 1rem;
}
.model-chip span { color: var(--accent2); }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤗 Hugging Face · Powered</div>
    <h1>NLP <span>Studio</span></h1>
    <p>Production-grade language model pipelines in your browser.</p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline selector ─────────────────────────────────────────────────────────
PIPELINES = {
    "Sentiment Analysis": {"icon": "💬", "desc": "Detect tone & emotion"},
    "Text Generation":    {"icon": "✍️", "desc": "Continue any prompt"},
    "Question Answering": {"icon": "🔍", "desc": "Extract answers from context"},
}

choice = st.radio(
    "Choose a pipeline",
    list(PIPELINES.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── Cached pipeline loaders ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@st.cache_resource(show_spinner=False)
def load_generation():
    return pipeline("text-generation", model="distilgpt2")

@st.cache_resource(show_spinner=False)
def load_qa():
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


# ══════════════════════════════════════════════════════════════════════════════
# ── SENTIMENT ANALYSIS ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if choice == "Sentiment Analysis":
    st.markdown('<div class="section-label">Input text</div>', unsafe_allow_html=True)
    text = st.text_area(
        "text",
        placeholder="Type something… e.g. 'The product exceeded all my expectations!'",
        height=130,
        label_visibility="collapsed",
    )

    examples = [
        "The food was absolutely incredible — best meal I've had in years.",
        "I waited 45 minutes and the service was appalling.",
        "It's okay, nothing special.",
    ]
    with st.expander("💡 Try an example"):
        for ex in examples:
            if st.button(ex, key=ex):
                text = ex

    if st.button("Analyse Sentiment →"):
        if not text.strip():
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Running model…"):
                pipe   = load_sentiment()
                result = pipe(text)[0]

            label = result["label"]       # POSITIVE / NEGATIVE
            score = result["score"]
            css_cls = "positive" if label == "POSITIVE" else "negative"
            emoji   = "😊" if label == "POSITIVE" else "😞"

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-label">Result</div>
                <div class="result-main {css_cls}">{emoji} {label}</div>
                <div style="color:var(--muted);font-size:.85rem;margin-top:.2rem">
                    Confidence: <strong style="color:var(--text)">{score*100:.1f}%</strong>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar" style="width:{score*100:.1f}%"></div>
                </div>
            </div>
            <div class="model-chip">🤖 Model: <span>distilbert-sst2</span></div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── TEXT GENERATION ───────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif choice == "Text Generation":
    st.markdown('<div class="section-label">Prompt</div>', unsafe_allow_html=True)
    prompt = st.text_area(
        "prompt",
        placeholder="Start a sentence… e.g. 'In the year 2150, humanity had finally'",
        height=120,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        max_new = st.slider("Max new tokens", 20, 200, 80, 10)
    with col2:
        temperature = st.slider("Temperature", 0.1, 1.5, 0.9, 0.05)

    if st.button("Generate Text →"):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Generating…"):
                pipe   = load_generation()
                result = pipe(
                    prompt,
                    max_new_tokens=max_new,
                    do_sample=True,
                    temperature=temperature,
                    pad_token_id=50256,
                )[0]["generated_text"]

            generated_only = result[len(prompt):]

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-label">Generated continuation</div>
                <div class="result-main generated"><span style="color:var(--muted)">{prompt}</span>{generated_only}</div>
            </div>
            <div class="model-chip">🤖 Model: <span>distilgpt2</span></div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── QUESTION ANSWERING ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif choice == "Question Answering":
    st.markdown('<div class="section-label">Context paragraph</div>', unsafe_allow_html=True)
    context = st.text_area(
        "context",
        value=(
            "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. "
            "It was constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair. "
            "The tower is 330 metres tall and was the world's tallest man-made structure for 41 years. "
            "It is named after the engineer Gustave Eiffel, whose company designed and built the tower."
        ),
        height=160,
        label_visibility="collapsed",
    )

    st.markdown('<div class="section-label" style="margin-top:1rem">Your question</div>', unsafe_allow_html=True)
    question = st.text_input(
        "question",
        placeholder="e.g. How tall is the Eiffel Tower?",
        label_visibility="collapsed",
    )

    if st.button("Find Answer →"):
        if not context.strip() or not question.strip():
            st.warning("Please provide both a context and a question.")
        else:
            with st.spinner("Extracting answer…"):
                pipe   = load_qa()
                result = pipe(question=question, context=context)

            answer = result["answer"]
            score  = result["score"]

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-label">Extracted answer</div>
                <div class="result-main neutral">"{answer}"</div>
                <div style="color:var(--muted);font-size:.85rem;margin-top:.5rem">
                    Confidence: <strong style="color:var(--text)">{score*100:.1f}%</strong>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar" style="width:{score*100:.1f}%"></div>
                </div>
            </div>
            <div class="model-chip">🤖 Model: <span>distilbert-squad</span></div>
            """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-bottom:2rem">
    <p style="color:var(--muted);font-size:.75rem;font-family:'DM Mono',monospace">
        Built with 🤗 Transformers · Streamlit · Distil* models
    </p>
</div>
""", unsafe_allow_html=True)
