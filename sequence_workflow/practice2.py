"""
Docstring for practice2
Node 1 → calculates square

Node 2 → calculates cube

Node 3 → prints a summary

Final output should keep all values in state.
"""
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

### creating the state.
class MyState(TypedDict):
    number :int
    square :int
    cube :int 

### creating the node 
def num_square(state:MyState):
    num = state['number']**2
    return{"square":num}

def num_cube(state:MyState):
    cube = state['number']**3
    return{"cube":cube}

def summary(state:MyState):
   print(f"The  number is {state['number']} the square of number is {state['square']},the cube of number is {state['cube']}")
   return{}

## creating the object of graph.
graph = StateGraph(MyState) 

## creating the node of graph.
graph.add_node("num_square",num_square)
graph.add_node("num_cube",num_cube)
graph.add_node("Summary",summary)

## adding the nmode edge.
graph.add_edge(START,"num_square")
graph.add_edge("num_square","num_cube")
graph.add_edge("num_cube","Summary")
graph.add_edge("Summary",END)

graph = graph.compile()
print(graph.get_graph().draw_mermaid())

initial_input={"number":3}
final_output = graph.invoke(initial_input)
print(final_output)