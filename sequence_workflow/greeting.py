## importing all libraries.
from langgraph.graph import StateGraph,END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

class AppState(TypedDict, total=False):
    name: str
    greeting: str
    

## Define Node 1 – take input.
def input_node(state):
    print("Input node receive",state)
    return state

###  Define Node 2 – greet the user.
def greet_user(state):
    name = state['name']
    greeting = f"Hello {name},How are you buddy!"
    return {**state,"greeting":greeting}

### Build the graph
builder = StateGraph(AppState)

## Initializing the node.
builder.add_node("input_node",RunnableLambda(input_node))
builder.add_node("greet_user",RunnableLambda(greet_user))

## conneting node with each other in sequence.
builder.set_entry_point("input_node")
builder.add_edge("input_node", "greet_user")
builder.add_edge("greet_user", END)


### creating the graph.
graph=builder.compile()

### Run the graph
input_user={"name":"Hitesh"}
responce= graph.invoke(input_user)
print("final response is - ",responce['greeting'])
