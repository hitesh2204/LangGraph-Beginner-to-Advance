"""
Docstring for problem1
Tasks

Node 1: uppercase text

Node 2: print text

Node 3: append " DONE"
OUTPUT :- {"text": "HELLO DONE"}
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict

###  creating the state.

class MyState(TypedDict):

    text : str

### creating the node.
def get_text(state:MyState):
    text = state['text'].upper()
    return {"text":text}

def final_text(state:MyState):
    final_text = state['text'] +" "+"DONE"
    return{"text":final_text}


## creating the graph object.
graph =  StateGraph(MyState)

### adding the node in graph.
graph.add_node("get_text",get_text)
graph.add_node("final_text",final_text)

## creating the graph edge.
graph.add_edge(START,"get_text")
graph.add_edge("get_text","final_text")
graph.add_edge("final_text",END)

## compile the graph.
graph = graph.compile()
print(graph.get_graph().draw_mermaid())

initial_input={"text":'Hitesh'}
final_output = graph.invoke(initial_input)
print(final_output)



