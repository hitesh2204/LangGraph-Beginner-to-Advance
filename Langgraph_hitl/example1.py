"""
Start → Ask Human → End
"""
from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver

### defining the state of graph.
class NameState(TypedDict):

    name:str
## adding the node in graph.
def ask_name(state:NameState):
    """
    This function is used to get the name of user from user input by using interrupt.
    """
    name = interrupt({"message":"what is your name ?"})
    return{"name":name}

### defining the graph object.
graph = StateGraph(NameState)

graph.add_node("ask_name",ask_name)

graph.add_edge(START,"ask_name")
graph.add_edge("ask_name",END)

### creating the object of InMemorySaver class.
checkpointer = InMemorySaver()

### compiling the graph.
app = graph.compile(checkpointer=checkpointer)

config = {"configurable":{"thread_id":"1"}}

result = app.invoke({},config=config)
print("First result ",result)

#### taking user input.
user_input = input("enter your name =")

final_result = app.invoke({"name":user_input},config=config)
print("Final Name =",final_result['name'])