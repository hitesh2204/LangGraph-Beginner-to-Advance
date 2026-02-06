from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# -------------------------
# Define State
# -------------------------
class OrderState(TypedDict):
    payment_status: str
    in_stock: bool
    is_serviceable: bool
    decision: str

# -------------------------
# Nodes (perform actions / update state)
# -------------------------
def payment_node(state: OrderState):
    return state

def warehouse_node(state: OrderState):
    return state

def shipping_node(state: OrderState):
    return state

def cancel_order_node(state: OrderState):
    return {"decision": "Order Cancelled"}

def ship_order_node(state: OrderState):
    return {"decision": "Order Shipped"}

def final_summary(state: OrderState):
    print(
        f"""
Order Summary
-------------
Payment    : {state['payment_status']}
In Stock   : {state['in_stock']}
Serviceable: {state['is_serviceable']}
Decision   : {state['decision']}
"""
    )
    return state

# -------------------------
# Routers (decide next node)
# -------------------------
def payment_router(state: OrderState):
    return "cancel" if state["payment_status"] == "failed" else "warehouse"

def warehouse_router(state: OrderState):
    return "cancel" if not state["in_stock"] else "shipping"

def shipping_router(state: OrderState):
    return "cancel" if not state["is_serviceable"] else "ship"

# -------------------------
# Build Graph
# -------------------------
graph = StateGraph(OrderState)

# Add nodes
graph.add_node("payment", payment_node)
graph.add_node("warehouse", warehouse_node)
graph.add_node("shipping", shipping_node)
graph.add_node("cancel", cancel_order_node)
graph.add_node("ship", ship_order_node)
graph.add_node("summary", final_summary)

# Start
graph.add_edge(START, "payment")

# Conditional edges
graph.add_conditional_edges("payment", payment_router, {"warehouse": "warehouse", "cancel": "cancel"})
graph.add_conditional_edges("warehouse", warehouse_router, {"shipping": "shipping", "cancel": "cancel"})
graph.add_conditional_edges("shipping", shipping_router, {"ship": "ship", "cancel": "cancel"})

# Final edges
graph.add_edge("cancel", "summary")
graph.add_edge("ship", "summary")
graph.add_edge("summary", END)

# Compile
order_graph = graph.compile()

# -------------------------
# Test Example
# -------------------------
result = order_graph.invoke({
    "payment_status": "unavailable",
    "in_stock": True,
    "is_serviceable": True,
    "decision": ""
})

