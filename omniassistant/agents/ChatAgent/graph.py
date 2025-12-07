
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from omniassistant.agents.ChatAgent.consts import LLM_INFERENCE_NODE
from omniassistant.nodes import llm_inference_node
from omniassistant.agents.ChatAgent.state import GraphState

load_dotenv()

workflow = StateGraph(GraphState)

# Add only the chat node
workflow.add_node(LLM_INFERENCE_NODE, llm_inference_node)

# Set entry point and end after chat node
workflow.set_entry_point(LLM_INFERENCE_NODE)
workflow.add_edge(LLM_INFERENCE_NODE, END)

app = workflow.compile()
