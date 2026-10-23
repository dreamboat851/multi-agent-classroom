import time
import streamlit as st
from workflow import build_graph
from agents import get_model

st.set_page_config(page_title="Multi-Agent Feedback Lab", page_icon="🤖", layout="wide")
st.title("🤖 Multi-Agent Customer Feedback Lab")
st.caption("Advanced AI classroom | Streamlit + LangGraph + local Qwen 0.5B (no paid API)")
with st.sidebar:
    st.header("How it works")
    st.markdown("1. **Classifier agent** labels feedback.\n2. **LangGraph router** selects a branch.\n3. **Response agent** drafts the reply.\n4. Uncertain cases go to human review.")
    st.info("First run downloads the model and can take a few minutes. Free hosting has memory and CPU limits.")
    if st.button("Load local model now"):
        with st.spinner("Downloading/loading Qwen..."):
            try:
                get_model()
                st.success("Model loaded")
            except Exception as e:
                st.error(f"Model failed to load: {e}")

examples = ["I love your service! The staff were excellent.",
            "I hate your services. The delivery was late.",
            "The service was okay, but I have mixed feelings."]
example = st.selectbox("Example feedback", ["Write my own"] + examples)
feedback = st.text_area("Customer feedback", value="" if example == "Write my own" else example, height=130)
left, right = st.columns([2, 1])
with right:
    st.subheader("Workflow")
    st.code("START\n  ↓\nClassifier\n  ├─ Positive → Positive agent\n  ├─ Negative → Negative agent\n  └─ Uncertain → Human review\n  ↓\n END", language=None)
with left:
    if st.button("Run multi-agent workflow", type="primary", disabled=not feedback.strip()):
        try:
            start = time.perf_counter()
            with st.spinner("Agents are working..."):
                result = build_graph().invoke({"feedback": feedback.strip(), "path": []})
            elapsed = time.perf_counter() - start
            st.metric("Detected sentiment", result["sentiment"])
            st.subheader("Agent response")
            st.write(result["response"])
            st.subheader("Execution trace")
            st.write(" → ".join(result["path"]))
            st.caption(f"Elapsed time: {elapsed:.1f} seconds. Model output may vary; small models can make mistakes.")
        except Exception as e:
            st.error(f"Execution failed: {e}")
            st.info("Check build logs, available RAM, and model download access. See README troubleshooting.")
