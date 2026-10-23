# Multi-Agent Feedback Lab (Advanced AI classroom)

A three-agent, free/open-source demonstration based on a customer-feedback workflow. A shared local Qwen2.5 0.5B model supplies all agent completions; LangGraph routes between nodes. No paid inference API is needed.

## Files
- `app.py`: Streamlit UI and execution trace
- `agents.py`: shared local Qwen model and role-specific agent functions
- `workflow.py`: LangGraph state, nodes, and conditional edges
- `requirements.txt`: Python dependencies
- `packages.txt`: native build dependencies for llama-cpp-python

## Local setup
Use Python 3.11 or 3.12, with a C++ build toolchain installed.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The first request downloads the GGUF model from Hugging Face. The model is cached after downloading.

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload these project files (not the model weights).
2. Sign in at https://share.streamlit.io/ and select **Create app**.
3. Select the repository, branch, and `app.py` as the entry point.
4. Choose Python 3.11 if that option is available, and deploy.
5. Watch build logs. The native `llama-cpp-python` package may need compilation and could exceed free build time/memory. If the app does not build, first test locally; for a classroom backup, use Colab or a hosted inference service with a free quota.

**Important:** This project is designed for the free CPU tier but is not guaranteed to fit Streamlit Community Cloud's variable resource limits. Free instances may sleep when idle. Performance and model availability depend on the hosting environment.

## Classroom lesson plan (45–60 minutes)
1. **5 min:** Explain classification vs generation and what an agent is.
2. **10 min:** Inspect `agents.py`: prompts and shared model.
3. **10 min:** Inspect `workflow.py`: state, nodes, edges, and conditional routing.
4. **10 min:** Run positive, negative, and ambiguous examples in Streamlit.
5. **10 min:** Change prompts and observe different replies.
6. **10 min:** Discuss model mistakes, escalation, safety, and evaluation.

### Student exercises
- Add a `Neutral` route and a neutral-response node.
- Add a `confidence` field, but do not treat an LLM's self-reported confidence as calibrated probability.
- Log each node's execution time.
- Create 20 labelled examples and compute a confusion matrix.
- Require a human approval step before any coupon or refund is issued.

## Limitations
- Three *role-specialized nodes* share one model; they are not three separately trained models.
- 0.5B parameters may yield incorrect labels or poor wording.
- The demo handles one request at a time, with no database or persistent memory.
- Do not paste real private customer data into a public classroom demo.
- No paid token charges, but cloud compute, bandwidth, and hosting availability are not unlimited guarantees.
- The original supplied PDF displayed an apparent API key: rotate it if real; this implementation requires none.
