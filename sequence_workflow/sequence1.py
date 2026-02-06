from langgraph.graph import StateGraph,START,END
from typing import TypedDict

### creating the state.

class MyState(TypedDict):
    name : str
    age : int
    language : str

## creating the nname node.
def get_name(state : MyState):

    return {"name":f"Hello {state['name']}"}

# creating the node for age.
def get_age(state : MyState):
    print(f"The age of {state['name']} is {state['age']}")
    return {"age":state['age']}

## creating the node for language.
def get_language(state : MyState):
    print(f"{state['name']} are know the {state['language']} language.")
    return {"language":state['language']}

## creating the graph object
graph = StateGraph(MyState)

## adding the node into graph.
graph.add_node("get_name",get_name)
graph.add_node("get_age",get_age)
graph.add_node("get_language",get_language)

### creatung the edge between node.
graph.add_edge(START,"get_name")
graph.add_edge("get_name","get_age")
graph.add_edge("get_age","get_language")
graph.add_edge("get_language",END)

graph = graph.compile()
print(graph.get_graph().draw_mermaid())

result ={
    "name": "Hitesh",
    "age": 34,
    "language":"Python"
}

output = graph.invoke(result)
print(output)
