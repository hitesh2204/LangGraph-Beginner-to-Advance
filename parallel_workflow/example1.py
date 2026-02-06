"""
Extract even numbers

Extract odd numbers

Merge both into a single list
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List

### creating the state of graph.
class MyState(TypedDict):
    
    number:List[int]
    even_number:List[int]
    odd_number:List[int]

### Creating the node of graph.
def even_num_node(state:MyState):
    """
    This function is used to find out the even number from list.
    """    
    even_num = [n for n in state["number"] if n % 2==0]
    return{"even_number":even_num}

def odd_num_node(state:MyState):
    """
    This function is used to return odd number in list.
    """
    odd_num = [n for n in state["number"] if n % 2 !=0]
    return{"odd_number":odd_num}

### creating the graph object.
graph = StateGraph(MyState)

### creating the node inside graph.
graph.add_node("even_num_node",even_num_node)
graph.add_node("odd_num_node",odd_num_node)

### creating the edges of graph.
graph.add_edge(START,"even_num_node")
graph.add_edge(START,"odd_num_node")
graph.add_edge("even_num_node",END)
graph.add_edge("odd_num_node",END)

## compile the graph.
graph = graph.compile()

initial_input ={"number":[10,20,15,12,21,23,24,30,35]}
final_output = graph.invoke(initial_input)
print(final_output)