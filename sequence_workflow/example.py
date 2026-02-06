from langgraph.graph import StateGraph,START,END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

class AppState(TypedDict,total=False):
    name:str
    age:int
    language:str


def input_node(state : AppState) -> AppState:
    name = state["name"]
    return {"name" : name}


def age_node(state : AppState)-> AppState:
    age =state["age"]
    print(f"age of {state['name']} is {state['age']}")
    return{"age":age}

def language_node(state : AppState)-> AppState:
    language =state["language"]
    print(f"{state['name']} know the {state['language']} language.")
    return {"language":language}

builder =StateGraph(AppState)

### creating the node
builder.add_node("input_node",input_node)
builder.add_node("age_node",age_node)
builder.add_node("language_node",language_node)

### connecting the node by edges.

builder.add_edge(START,"input_node")
builder.add_edge("input_node","age_node")
builder.add_edge("age_node","language_node")
builder.add_edge("language_node",END)

###Compiling the graph
graph =builder.compile()
print(graph.get_graph().draw_mermaid())


### Run the graph.
input_user={
    "name":"Hitesh",
    "age":34,
    "language":"Python"
}
output = graph.invoke(input_user)
print("Final output is -",output)