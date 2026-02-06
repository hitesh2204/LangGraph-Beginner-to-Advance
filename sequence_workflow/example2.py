from langgraph.graph import StateGraph,END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

class AppState(TypedDict,total=False):
    name:str
    age:int
    language:str


def input_node(state):
    print("Input received",state)
    return state

def age_node(state):
    age =state.get('age',34)
    print(f"age is {age}")
    return{**state,"age":age}

def language_node(state):
    language =state.get("language","Python")
    print(f"Language is {language}")
    return {**state,"language":language}

builder =StateGraph(AppState)

### creating the node
builder.add_node("input_node",RunnableLambda(input_node))
builder.add_node("age_node",RunnableLambda(age_node))
builder.add_node("language_node",RunnableLambda(language_node))

### connecting the node by edges.

builder.set_entry_point("input_node")
builder.add_edge("input_node","age_node")
builder.add_edge("age_node","language_node")
builder.add_edge("language_node",END)

###Compiling the graph
graph =builder.compile()

### Run the graph.
input_user={
    "name":"Hitesh",
    "age":34,
    "language":"Python"
}
output = graph.invoke(input_user)
print("Final output is -",output)