from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from operator import add

# ---------------- STATE ----------------
class MyState(TypedDict):
    marks: List[int]
    pass_stud: int
    fail_stud: int
    max_marks: int
    merge_result: Annotated[List[int], add]
    summary: dict


# ---------------- PARALLEL NODES ----------------
def count_pass_student_node(state: MyState):
    count = len([m for m in state["marks"] if m >= 40])
    return {
        "pass_stud": count,
        "merge_result": [count]
    }


def count_fail_student_node(state: MyState):
    count = len([m for m in state["marks"] if m < 40])
    return {
        "fail_stud": count,
        "merge_result": [count]
    }


def maximum_marks_node(state: MyState):
    maximum = max(state["marks"])
    return {
        "max_marks": maximum,
        "merge_result": [maximum]
    }


# ---------------- FINAL NODE ----------------
def summary_node(state: MyState):
    summary = {
        "Marks": state["marks"],
        "Pass Students": state["pass_stud"],
        "Fail Students": state["fail_stud"],
        "Merged Metrics (pass, fail, max)": state["merge_result"]
    }
    print(summary)
    return {"summary": summary}


# ---------------- GRAPH ----------------
graph = StateGraph(MyState)

graph.add_node("pass_node", count_pass_student_node)
graph.add_node("fail_node", count_fail_student_node)
graph.add_node("max_node", maximum_marks_node)
graph.add_node("summary_node", summary_node)

# 🔥 Parallel fan-out
graph.add_edge(START, "pass_node")
graph.add_edge(START, "fail_node")
graph.add_edge(START, "max_node")

# 🔥 Fan-in
graph.add_edge("pass_node", "summary_node")
graph.add_edge("fail_node", "summary_node")
graph.add_edge("max_node", "summary_node")

graph.add_edge("summary_node", END)

graph = graph.compile()

# ---------------- RUN ----------------
result = graph.invoke({"marks": [20, 35, 25, 10, 40, 42, 55, 60, 70, 50, 30]})
print(result)