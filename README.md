# Multi-Agent Feedback Lab — Groq hosted version

This version replaces local `llama-cpp-python` inference with Groq API calls, while keeping a genuine LangGraph conditional workflow.

## Deploy
1. Replace `app.py`, `agents.py`, `workflow.py`, and `requirements.txt` in your existing GitHub repo with these versions. **Delete the old `packages.txt`** (no CMake required). Keep `.gitignore` and this README.
2. Create a free account at https://console.groq.com/ and generate an API key at https://console.groq.com/keys . Check your account's available models and quotas.
3. In Streamlit Community Cloud, open the app settings → Secrets and enter:
   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   GROQ_MODEL = "openai/gpt-oss-20b"
   ```
   Do NOT commit this key to GitHub. The model shown was listed on Groq's free plan at preparation time; change it if your account has a different available model.
4. Reboot/redeploy the app after GitHub updates. Python 3.11 works.

## How it works
- `agents.py`: `ask_llm` calls Groq; `sentiment_agent`, `positive_agent`, and `negative_agent` are separate role-specific functions.
- `workflow.py`: LangGraph StateGraph with `classify` node and conditional edges to `positive` or `negative`.
- `app.py`: Streamlit UI and display of workflow state.

## Classroom exercises
1. Identify `START`, `END`, nodes, and conditional edges.
2. Run both example feedback messages and inspect workflow state.
3. Add a `Neutral` agent and a third conditional route.
4. Compare responses when changing system prompts.
5. Discuss why separate agent roles can share one LLM and why this is not a fully autonomous agent system.

## Limits and safety
Groq's free API is quota-limited. Two calls are made for each submitted feedback. The negative agent does not promise unauthorized coupons. This demonstration has not been live-tested with an actual Groq API key in the build environment.
