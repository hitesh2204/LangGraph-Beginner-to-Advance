"""
Docstring for problem2
1️⃣ Validate user age
2️⃣ Categorize user
3️⃣ Print final result
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict

### creating the state for graph.
class MyState(TypedDict):
    age:int
    is_valid:bool
    category:str

### creating the node
def validate_age(state:MyState):
    return{'is_valid':state['age']>=18}

def categorized_age(state:MyState):
    category = "Adult" if state["is_valid"] else "No Adult"
    return{"category":category}

def final_note(state:MyState):
    print(f"The age is {state['age']},is valid {state['is_valid']},category is {state['category']}")
    return {}
### creating the grapg object.
graph = StateGraph(MyState)

## creating the node inside graph.
graph.add_node("validate_age",validate_age)
graph.add_node("categorized_age",categorized_age)
graph.add_node("print_note",final_note)

## creating the edge of node.
graph.add_edge(START,"validate_age")
graph.add_edge("validate_age","categorized_age")
graph.add_edge("categorized_age","print_note")
graph.add_edge("print_note",END)

graph = graph.compile()

initial_input={'age':10}
final_output = graph.invoke(initial_input)
print(final_output)