"""LangGraph routing for the three-agent customer feedback application."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents import sentiment_agent, positive_agent, negative_agent


class FeedbackState(TypedDict):
    feedback: str
    sentiment: str
    response: str


def classify(state: FeedbackState) -> dict:
    return {"sentiment": sentiment_agent(state["feedback"])}


def respond_positive(state: FeedbackState) -> dict:
    return {"response": positive_agent(state["feedback"])}


def respond_negative(state: FeedbackState) -> dict:
    return {"response": negative_agent(state["feedback"])}


def route(state: FeedbackState) -> str:
    sentiment = state["sentiment"]
    if sentiment == "Positive":
        return "positive"
    if sentiment == "Negative":
        return "negative"
    raise ValueError(f"Cannot route unexpected sentiment: {sentiment!r}")


builder = StateGraph(FeedbackState)
builder.add_node("classify", classify)
builder.add_node("positive", respond_positive)
builder.add_node("negative", respond_negative)
builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify", route, {"positive": "positive", "negative": "negative"}
)
builder.add_edge("positive", END)
builder.add_edge("negative", END)
graph = builder.compile()


def run_workflow(feedback: str) -> FeedbackState:
    return graph.invoke({"feedback": feedback, "sentiment": "", "response": ""})
