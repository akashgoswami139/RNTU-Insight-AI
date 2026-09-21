import streamlit as st
from main import get_answer

# ============================================================
# RNTU Insight AI — Streamlit UI
# All retrieval + LLM logic lives in src/rag_chain.py; this file
# only handles layout, the About sidebar, and the chat widgets.
# ============================================================

st.set_page_config(
    page_title="RNTU Insight AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------
# Minimal custom styling
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 800px;
            padding-top: 2rem;
        }
        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.1rem;
        }
        .app-subtitle {
            color: #888;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Sidebar — About the Developer
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown("## 👤 About the Developer")
    st.markdown("**Akash Goswami**")
    st.caption(
        "Aspiring AI/ML Engineer | Python • Machine Learning • "
        "Deep Learning • RAG & LLMs"
    )
    st.write(
        "Final-year B.E. student in Artificial Intelligence & Machine "
        "Learning at Rabindranath Tagore University, Bhopal."
    )

    st.markdown("---")
    st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/akashgoswami-/)")
    st.markdown("💻 [GitHub](https://github.com/akashgoswami139)")
    st.markdown("📧 akashhgoswami26@gmail.com")

    st.markdown("---")
    st.caption("RNTU Insight AI — built by Akash Goswami")

# ---------------------------------------------------------------
# Main — Header
# ---------------------------------------------------------------
st.markdown('<div class="app-title">🎓 RNTU Insight AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Ask anything about Rabindranath Tagore '
    'University, Bhopal.</div>',
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------
# Chat UI (front-end only — no backend wired up yet)
# ---------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question about RNTU...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching RNTU documents..."):
            try:
                answer = get_answer(user_input)
            except Exception as e:
                answer = f"Something went wrong while answering: {e}"
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})