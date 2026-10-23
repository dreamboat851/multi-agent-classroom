"""Three role-specialized agents sharing one local Qwen model."""
import os
from functools import lru_cache
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

MODEL_REPO = "Qwen/Qwen2.5-0.5B-Instruct-GGUF"
MODEL_FILE = "qwen2.5-0.5b-instruct-q4_k_m.gguf"

@lru_cache(maxsize=1)
def get_model():
    path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
    return Llama(model_path=path, n_ctx=2048, n_threads=min(2, os.cpu_count() or 2),
                 n_gpu_layers=0, verbose=False)

def ask_llm(system_prompt: str, feedback: str, max_tokens: int = 130) -> str:
    result = get_model().create_chat_completion(
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": feedback}],
        max_tokens=max_tokens, temperature=0.0,
    )
    return result["choices"][0]["message"]["content"].strip()

def sentiment_agent(feedback: str) -> str:
    answer = ask_llm("Classify the customer feedback. Output exactly one word: Positive or Negative. No explanation.", feedback, 12)
    first = answer.lower().strip().strip('.!')
    if first == "positive":
        return "Positive"
    if first == "negative":
        return "Negative"
    # Ambiguous output must not silently become a confident classification.
    return "Uncertain"

def positive_agent(feedback: str) -> str:
    return ask_llm("You are a customer care agent. Thank the customer warmly for positive feedback. Be concise. Do not invent facts.", feedback)

def negative_agent(feedback: str) -> str:
    return ask_llm("You are a customer care agent. Apologize, acknowledge the complaint, and offer to investigate. Do not promise coupons, refunds, or actions you cannot fulfill. Be concise.", feedback)
