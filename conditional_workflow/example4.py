from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ---------------- STATE ----------------
class LoanState(TypedDict):
    credit_score: int
    decision: str

# ---------------- ROUTER ----------------
def credit_router(state: LoanState):
    score = state["credit_score"]

    if score < 600:
        return "reject"
    elif 600 <= score < 750:
        return "review"
    else:
        return "approve"

# ---------------- NODES ----------------
def reject_loan_node(state: LoanState):
    return {"decision": "Loan Rejected"}

def manual_review_node(state: LoanState):
    return {"decision": "Manual Review Required"}

def approved_loan_node(state: LoanState):
    return {"decision": "Loan Approved"}

def final_loan_summary(state: LoanState):
    print(
        f"Credit Score: {state['credit_score']} | "
        f"Decision: {state['decision']}"
    )
    return state

# ---------------- GRAPH ----------------
graph = StateGraph(LoanState)

graph.add_node("reject_loan_node", reject_loan_node)
graph.add_node("manual_review_node", manual_review_node)
graph.add_node("approved_loan_node", approved_loan_node)
graph.add_node("final_loan_summary", final_loan_summary)

graph.add_conditional_edges(
    START,
    credit_router,
    {
        "reject": "reject_loan_node",
        "review": "manual_review_node",
        "approve": "approved_loan_node",
    }
)

graph.add_edge("reject_loan_node", "final_loan_summary")
graph.add_edge("manual_review_node", "final_loan_summary")
graph.add_edge("approved_loan_node", "final_loan_summary")
graph.add_edge("final_loan_summary", END)

graph = graph.compile()

# ---------------- RUN ----------------
graph.invoke({"credit_score": 550})  # Rejected
graph.invoke({"credit_score": 650})  # Manual Review
graph.invoke({"credit_score": 800})  # Approved