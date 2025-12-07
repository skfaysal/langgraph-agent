from typing import Any, Dict

from ..chains.llm_inference_chain import simple_chat_chain
from omniassistant.agents.ChatAgent.state import GraphState


def llm_inference_node(state: GraphState) -> Dict[str, Any]:
    print("---LLM INFERENCE NODE---")
    question = state["question"]
    llm_config = state["llm_config"]

    inputs = {
        "llm_config": llm_config,
        "question": question,
    }
    result = simple_chat_chain(inputs)
    return {"model_prediction": result}
