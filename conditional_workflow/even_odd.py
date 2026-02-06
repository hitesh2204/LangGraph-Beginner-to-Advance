from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# -------- STATE --------
class MyState(TypedDict):
    number: int
    category: str

# -------- ROUTER (NOT A NODE) --------
def number_router(state: MyState):
    if state["number"] > 0:
        return "positive"
    return "negative"

# -------- NODES --------
def positive_number_node(state: MyState):
    return {"category": "positive number"}

def negative_number_node(state: MyState):
    return {"category": "negative number"}

def summary(state: MyState):
    print(f"The number is {state['number']} and the category is {state['category']}")
    return state

# -------- GRAPH --------
graph = StateGraph(MyState)

graph.add_node("positive_number_node", positive_number_node)
graph.add_node("negative_number_node", negative_number_node)
graph.add_node("final_summary", summary)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    number_router,
    {
        "positive": "positive_number_node",
        "negative": "negative_number_node",
    }
)

graph.add_edge("positive_number_node", "final_summary")
graph.add_edge("negative_number_node", "final_summary")
graph.add_edge("final_summary", END)

graph = graph.compile()

print(graph.invoke({"number": 10}))