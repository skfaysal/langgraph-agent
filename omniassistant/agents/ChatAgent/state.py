from typing import List, TypedDict, Optional, Dict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        model_prediction: model_prediction
        llm_config: llm_config
    """


    question: str
    model_prediction: str
    llm_config: Dict
    