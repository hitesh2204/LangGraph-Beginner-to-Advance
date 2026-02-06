from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

class AppState(TypedDict, total=False):
    name: str
    final_output: str

# ✅ Node 1: Input pass-through
def input_node(state):
    print("🟢 Input received:", state)
    return state

# ✅ Node 2: Generate greeting
def greeting_node(state):
    name = state["name"]

    # ✅ Setup HuggingFaceEndpoint
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        temperature=0.7,
        max_new_tokens=100
    )

    # ✅ Proper PromptTemplate usage
    prompt = PromptTemplate(
        template='Create congratulations message for {name}',
        input_variables=['name']
    )
    response = prompt.invoke({'name':name})

    # ✅ Invoke the LLM
    result = llm.invoke(response)

    return {**state, "final_output": result}

# ✅ Graph Definition
builder = StateGraph(AppState)
builder.add_node("input_node", RunnableLambda(input_node))
builder.add_node("greeting_node", RunnableLambda(greeting_node))

builder.set_entry_point("input_node")
builder.add_edge("input_node", "greeting_node")
builder.add_edge("greeting_node", END)

graph = builder.compile()

# ✅ Run the graph
input_data = {"name": "Rohit"}
output = graph.invoke(input_data)

print("\n🎉 Greeting message:", output["final_output"])
