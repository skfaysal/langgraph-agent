import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMProvider:
    def __init__(self, llm_type: str, model_name: str, **kwargs):
        self.llm_type = llm_type.lower()
        self.model_name = model_name
        self.kwargs = kwargs

    def get_llm(self):
        if self.llm_type == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            return ChatAnthropic(model=self.model_name, api_key=api_key, **self.kwargs)
        # elif self.llm_type == "vertexai":
        #     return VertexAI(model_name=self.model_name, **self.kwargs)
        # elif self.llm_type == "google":
        #     return ChatGoogleGenerativeAI(model=self.model_name, **self.kwargs)
        elif self.llm_type == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            return ChatOpenAI(model=self.model_name, api_key=api_key, **self.kwargs)
        else:
            raise ValueError(f"Unsupported LLM type: {self.llm_type}")

# Example usage:
# provider = LLMProvider("openai", "gpt-4o", max_tokens=512)
# llm = provider.get_llm()