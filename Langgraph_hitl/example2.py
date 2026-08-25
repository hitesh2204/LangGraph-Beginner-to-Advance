from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver


class NameState(TypedDict, total=False):
    name: str
    is_valid: bool
    message: str


def ask_name(state: NameState):
    return {"name": state["name"]}


def validate_name(state: NameState):
    confirmation = interrupt(
        {"message": f"Is the name '{state['name']}' valid? (yes/no)"}
    )

    is_valid = confirmation.lower() == "yes"

    if is_valid:
        message = f"{state['name']} is a valid name."
    else:
        message = f"{state['name']} is NOT a valid name."

    return {"is_valid": is_valid, "message": message}


graph = StateGraph(NameState)

graph.add_node("ask_name", ask_name)
graph.add_node("validate_name", validate_name)

graph.add_edge(START, "ask_name")
graph.add_edge("ask_name", "validate_name")
graph.add_edge("validate_name", END)

app = graph.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "1"}}


# ---- First Invoke ----
name = input("Enter the user name = ")
result = app.invoke({"name": name}, config=config)

# Extract interrupt message properly
# Extract interrupt message
interrupt_list = result["__interrupt__"]
interrupt_obj = interrupt_list[0]
interrupt_message = interrupt_obj.value["message"]

print("\nInterrupt message:")
print(interrupt_message)

# ---- Resume ----
user_input = input("Enter yes/no: ")

final_result = app.invoke(
    Command(resume=user_input),
    config=config
)

print("\nFinal Result:")
print(final_result['message'])