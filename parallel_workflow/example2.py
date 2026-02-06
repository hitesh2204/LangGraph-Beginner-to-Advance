"""
Node A → compute sum

Node B → compute max

Node C → compute min

2️⃣ Merge results into a single list
3️⃣ Final node → compute average of (sum, max, min)
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List,Annotated
from operator import add
import numpy as np

## creating thhe state for the graph.
class MyState(TypedDict):

    number:List[int]
    num_sum:int
    max_num:int
    min_num:int
    merge_num:Annotated[List[float],add]
    avg_num:float

## creating the node of graph.
def num_sum_node(state:MyState):
    """
    This function ius used to  find the sum of number inside list.
    """
    number_sum = sum(state["number"])
    return{"num_sum":number_sum,"merge_num":[number_sum]}

def max_num_node(state:MyState):
    """
    This function is used to find out the maximum number from list.
    """
    max_number = max(state["number"])
    return{"max_num":max_number,"merge_num":[max_number]}

def min_num_node(state:MyState):
    """
    This function is used tofind out the minimum number from list.
    """
    min_number = min(state["number"])
    return{"min_num":min_number,"merge_num":[min_number]}

def avg_num_node(state:MyState):
    """
    This function is used tofind out the average of the list.
    """
    avg_number = np.mean(state["merge_num"])
    return{"avg_num":avg_number}

### creating the graph object.
graph = StateGraph(MyState)

## adding the node inside the graph.
graph.add_node("num_sum_node",num_sum_node)
graph.add_node("max_num_node",max_num_node)
graph.add_node("min_num_node",min_num_node)
graph.add_node("avg_num_node",avg_num_node)

### creating the parallel edges of graph.
graph.add_edge(START,"num_sum_node")
graph.add_edge(START,"max_num_node")
graph.add_edge(START,"min_num_node")


graph.add_edge("num_sum_node","avg_num_node")
graph.add_edge("max_num_node","avg_num_node")
graph.add_edge("min_num_node","avg_num_node")

graph.add_edge("avg_num_node",END)

### compile the graph.
graph = graph.compile()

initial_input = {"number":[10,20,15,12,21,23,24,30,35]}
final_output = graph.invoke(initial_input)
print(final_output)




