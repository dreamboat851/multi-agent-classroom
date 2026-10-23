"""LangGraph routing: classifier -> positive OR negative response."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents import sentiment_agent, positive_agent, negative_agent

class FeedbackState(TypedDict, total=False):
    feedback: str
    sentiment: str
    response: str
    path: list[str]

def classify(state: FeedbackState) -> dict:
    return {"sentiment": sentiment_agent(state["feedback"]), "path": ["Classifier"]}

def route(state: FeedbackState) -> str:
    return {"Positive": "positive", "Negative": "negative"}.get(state["sentiment"], "uncertain")

def positive(state: FeedbackState) -> dict:
    return {"response": positive_agent(state["feedback"]), "path": state["path"] + ["Positive agent"]}

def negative(state: FeedbackState) -> dict:
    return {"response": negative_agent(state["feedback"]), "path": state["path"] + ["Negative agent"]}

def uncertain(state: FeedbackState) -> dict:
    return {"response": "I couldn't confidently classify this feedback. Please review it manually.",
            "path": state["path"] + ["Human review"]}

def build_graph():
    graph = StateGraph(FeedbackState)
    graph.add_node("classify", classify)
    graph.add_node("positive", positive)
    graph.add_node("negative", negative)
    graph.add_node("uncertain", uncertain)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges("classify", route, {"positive": "positive", "negative": "negative", "uncertain": "uncertain"})
    for name in ("positive", "negative", "uncertain"):
        graph.add_edge(name, END)
    return graph.compile()
