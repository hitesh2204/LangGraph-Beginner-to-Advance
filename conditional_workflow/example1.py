"""
Input: user age

If age < 18  → Node A (minor flow)
If age 18–60 → Node B (adult flow)
If age > 60  → Node C (senior flow)

Final node → print category message
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ---------------- STATE ----------------
class MyState(TypedDict):
    age: int
    category: str


# ---------------- ROUTER NODE ----------------
def age_node(state: MyState) -> str:
    if state["age"] < 18:
        return "teen_age_node"
    elif state["age"] <= 60:
        return "adult_node"
    else:
        return "senior_node"


# ---------------- CATEGORY NODES ----------------
def teen_age_node(state: MyState):
    return {"category": "Teen Age"}


def adult_node(state: MyState):
    return {"category": "Adult"}


def senior_node(state: MyState):
    return {"category": "Senior Citizen"}


# ---------------- FINAL NODE ----------------
def final_message(state: MyState):
    print(f"The age is {state['age']} and the category is {state['category']}")
    return {}


# ---------------- GRAPH ----------------
graph = StateGraph(MyState)

# Add nodes
graph.add_node("age_node", age_node)
graph.add_node("teen_age_node", teen_age_node)
graph.add_node("adult_node", adult_node)
graph.add_node("senior_node", senior_node)
graph.add_node("final_message", final_message)


# 🔥 CONDITIONAL ROUTING
graph.add_conditional_edges(START,age_node,
    {
        "teen_age_node": "teen_age_node",
        "adult_node": "adult_node",
        "senior_node": "senior_node",
    }
)

# Merge all paths
graph.add_edge("teen_age_node", "final_message")
graph.add_edge("adult_node", "final_message")
graph.add_edge("senior_node", "final_message")

graph.add_edge("final_message", END)

graph = graph.compile()

# ---------------- RUN ----------------
graph.invoke({"age": 65})
