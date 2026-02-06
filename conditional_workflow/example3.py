"""
"high" → senior_agent

"medium" → regular_agent

"low" → auto_reply
"""
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List

## creating the state of graph.
class MyState(TypedDict):

    priority:str
    ticket:str
### creating the node.
def priority_node(state:MyState):
    """
    This node is responsible to decide ticket base on priority.
    """
    if state["priority"]=="high":
        return "senior_agent"
    if state["priority"]=="medium":
        return "regular_agent"
    if state["priority"]=="low":
        return "auto_reply"
    
def senior_agent_node(state:MyState):
    """
    This node is used to geenrate the ticket for senior_agent.
    """
    return{"ticket":"Senior Support Agent"}

def medium_agent_node(state:MyState):
    """"
    This node is used to return the ticket for medium level agent.
    """
    return{"ticket":"Regular Support Agent"}

def low_agent_node(state:MyState):
    """
    This node is used to return the auto generated tickets.
    """
    return{"ticket":"Automated Response"}

def ticket_generator_node(state:MyState):
    """
    This ndoe is used to return the fibnal summary for ticket generator base on the agent.
    """
    print(f"The priority is {state['priority']} and the ticket generator for {state['ticket']}")
### creating graph object.
graph = StateGraph(MyState)

## creating the node for graph.
graph.add_node("priority_node",priority_node)
graph.add_node("high_priority_node",senior_agent_node)
graph.add_node("medium_priority_node",medium_agent_node)
graph.add_node("low_priority_node",low_agent_node)
graph.add_node("ticket_generator",ticket_generator_node)

graph.add_conditional_edges(START,priority_node,{
    "senior_agent":"high_priority_node",
    "regular_agent":"medium_priority_node",
    "auto_reply":"low_priority_node"
})

graph.add_edge("high_priority_node","ticket_generator")
graph.add_edge("medium_priority_node","ticket_generator")
graph.add_edge("low_priority_node","ticket_generator")

graph.add_edge("ticket_generator",END)
## compile the graph.
graph = graph.compile()

initial_input = ({"priority":"medium"})
final_outptut = graph.invoke(initial_input)
print(final_outptut)


