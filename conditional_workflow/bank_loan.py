from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ---------------- STATE ----------------
class LoanState(TypedDict):
    credit_score: int
    loan_amount: int
    risk_score: int
    decision: str

# ---------------- ROUTERS ----------------
def credit_score_router(state: LoanState):
    return "reject" if state["credit_score"] < 600 else "manager"

def loan_amount_router(state: LoanState):
    return "risk" if state["loan_amount"] <= 1_000_000 else "reject"

def risk_score_router(state: LoanState):
    return "approve" if state["risk_score"] <= 40 else "reject"

# ---------------- ROUTER NODES ----------------
def credit_score_node(state: LoanState): return {}
def loan_amount_node(state: LoanState): return {}
def risk_score_node(state: LoanState): return {}

# ---------------- ACTION NODES ----------------
def bank_reject_node(state: LoanState):
    return {"decision": "Rejected by Bank"}

def manager_reject_node(state: LoanState):
    return {"decision": "Rejected by Manager"}

def risk_reject_node(state: LoanState):
    return {"decision": "Rejected by Risk Team"}

def approve_node(state: LoanState):
    return {"decision": "Loan Approved"}

def final_loan_summary(state: LoanState):
    print(
        f"""
Loan Decision
-------------
Credit Score : {state['credit_score']}
Loan Amount  : {state['loan_amount']}
Risk Score   : {state['risk_score']}
Decision     : {state['decision']}
"""
    )
    return state

# ---------------- GRAPH ----------------
graph = StateGraph(LoanState)

# Add nodes
graph.add_node("credit_score_node", credit_score_node)
graph.add_node("loan_amount_node", loan_amount_node)
graph.add_node("risk_score_node", risk_score_node)
graph.add_node("bank_reject_node", bank_reject_node)
graph.add_node("manager_reject_node", manager_reject_node)
graph.add_node("risk_reject_node", risk_reject_node)
graph.add_node("approve_node", approve_node)
graph.add_node("final_loan_summary", final_loan_summary)

# Stage 1
graph.add_edge(START, "credit_score_node")
graph.add_conditional_edges(
    "credit_score_node",
    credit_score_router,
    {
        "reject": "bank_reject_node",
        "manager": "loan_amount_node",
    },
)

# Stage 2
graph.add_conditional_edges(
    "loan_amount_node",
    loan_amount_router,
    {
        "risk": "risk_score_node",
        "reject": "manager_reject_node",
    },
)

# Stage 3
graph.add_conditional_edges(
    "risk_score_node",
    risk_score_router,
    {
        "approve": "approve_node",
        "reject": "risk_reject_node",
    },
)

# Final connections
for n in ["bank_reject_node", "manager_reject_node", "risk_reject_node", "approve_node"]:
    graph.add_edge(n, "final_loan_summary")

graph.add_edge("final_loan_summary", END)
graph = graph.compile()

# ---------------- RUN ----------------
graph.invoke({
    "credit_score": 780,
    "loan_amount": 500_000,
    "risk_score": 30,
})