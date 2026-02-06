from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import string

class MyState(TypedDict):
    text: str
    clean_text: str
    word_count: int


def clean_text_node(state: MyState):
    lower = state["text"].lower()
    no_punct = lower.translate(str.maketrans("", "", string.punctuation))
    return {"clean_text": no_punct}


def word_count_node(state: MyState):
    count = len(state["clean_text"].split())
    return {"word_count": count}


def text_summary_node(state: MyState):
    print({
        "text": state["text"],
        "clean_text": state["clean_text"],
        "word_count": state["word_count"]
    })
    return {}


graph = StateGraph(MyState)

graph.add_node("clean_text_node", clean_text_node)
graph.add_node("word_count_node", word_count_node)
graph.add_node("text_summary_node", text_summary_node)

graph.add_edge(START, "clean_text_node")
graph.add_edge("clean_text_node", "word_count_node")
graph.add_edge("word_count_node", "text_summary_node")
graph.add_edge("text_summary_node", END)

graph = graph.compile()

initial_input = {"text": "Hello, Hitesh!! Welcome to LangGraph."}
output = graph.invoke(initial_input)

print(output)