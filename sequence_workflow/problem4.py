"""Input a list of numbers

Filter only even numbers

Square them

Compute sum
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List
from operator import add

### creating the state.
class Mystate(TypedDict):

    number: List[int]
    even_number: List[int]
    squared_number: List[int]
    total: int

## creating the node of graph.
def even_number_node(state:Mystate):
    """
    This function is used to find outthe even number inside the list.
    """
    even_num = [n for n in state['number'] if n% 2 ==0]
    return {"even_number":even_num}

def sqaure_number_node(state:Mystate):
    """
    This funtion is used to sqaure the even number inside the list.
    """
    sqaure_num = [n**2 for n in state["even_number"]]
    return{"squared_number":sqaure_num}

def compute_number_node(state:Mystate):
    """
    This function is used to return ths calculation of all sqwaure number inside the list.
    """
    total_num = sum(state["squared_number"])
    return{"total":total_num}


### creating the graph object.
graph = StateGraph(Mystate)

### creating the node inside the graph.
graph.add_node("even_number_node",even_number_node)
graph.add_node("square_number_node",sqaure_number_node)
graph.add_node("compute_number_node",compute_number_node)

### creating the node of graph.
graph.add_edge(START,"even_number_node")
graph.add_edge("even_number_node","square_number_node")
graph.add_edge("square_number_node","compute_number_node")
graph.add_edge("compute_number_node",END)

## compile the graph.
graph = graph.compile()

initial_input = ({"number":[2,6,3,7,8,10,12,15,20]})
final_output = graph.invoke(initial_input)
print(final_output)