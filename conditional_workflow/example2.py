"""
Route based on marks:

< 40 → "fail"

40–59 → "pass"

>= 60 → "distinction"
"""
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List

### creating the state for graph.
class MyState(TypedDict):

    marks:int
    result:str

## creating the node.
def marks_node(state:MyState):
    """
    This node is used to return the another node base on marks.
    """
    if (state["marks"] >= 40) | (state["marks"]<59):
        return "pass"
    if state["marks"]<40:
        return "fail"
    if state["marks"]>=60:
        return "distinction"

def pass_node(state:MyState):
    """
    This function is used to return the student is pass or not.
    """ 
    return{"result":"Pass"}

def fail_node(state:MyState):
    """
    This functiuon is used to return the fail result.
    """
    return{"result":"Fail"}

def distinction_node(state:MyState):
    """
    This function is used to return the distinction result.
    """
    return{"result":"Distinction"}

def report_card_node(state:MyState):
    """
    This node is used to return the final report card of student.
    """
    print(f"The marks of student is {state['marks']} and the result of student is {state['result']}")   
 
### creating the graph object
graph = StateGraph(MyState)

### creating the node for graph
graph.add_node("marks_node",marks_node)
graph.add_node("pass_node",pass_node)
graph.add_node("fail_node",fail_node)
graph.add_node("distinction_node",distinction_node)
graph.add_node("report_card",report_card_node)

graph.add_conditional_edges(START,marks_node,{

     "pass":"pass_node",
     "fail":"fail_node",
     "distinction":"distinction_node"
})
graph.add_edge("pass_node","report_card")
graph.add_edge("fail_node","report_card")
graph.add_edge("distinction_node","report_card")

graph.add_edge("report_card",END)

## compile graph.
graph = graph.compile()

initial_input = {"marks":56}
final_output = graph.invoke(initial_input)
print(final_output)

