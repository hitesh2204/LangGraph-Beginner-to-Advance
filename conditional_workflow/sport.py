"""
START
  |
 PLAY
  |
(choice)
 ├── BADMINTON ──┐
 └── CRICKET  ───┘
        |
       END
"""

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List,Literal

### creating the state of graph.
class SportState(TypedDict):

    sport_info:str
    sport_choice:str

### building the node for graph.
def Play_info(state:SportState):
    """
    This function is used to return the informarion about sports.
    """
    print("Player wants to play")
    return state

def Cricket_info(state:SportState):
    """
    This function is used to return the information about cricket.
    """
    return{"sport_info":state["sport_info"]+" planning to play Cricket"}

def Bandminton_info(state:SportState):
    """
    This function is used to return the information about badminton.
    """
    return{"sport_info":state["sport_info"]+"planning to play Badminton"}

def sport_choice(state:SportState)->Literal["Cricket_info","Badminton_info"]:
    """
    This function is used to return the sport information as per sport choice.
    """
    if state['sport_choice']=="cricket":
        return "Cricket_info"
    if state['sport_info']=="badminton":
        return "Bandminton_info"
    else:
        return "wrong choice"

### creating the graph object.
graph = StateGraph(SportState)

### creating the node for graph.
graph.add_node("Play_info",Play_info)
graph.add_node("Cricket_info",Cricket_info)
graph.add_node("Badminton_info",Bandminton_info)

graph.add_edge(START,"Play_info")
graph.add_conditional_edges("Play_info",sport_choice)
graph.add_edge("Cricket_info",END)
graph.add_edge("Badminton_info",END)

### compile trhe graph.
sport_graph = graph.compile()


final_output = sport_graph.invoke({"sport_choice":"cricket","sport_info":"Hitesh"})
print(final_output)
print(final_output['sport_info'])


