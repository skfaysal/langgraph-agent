
from omniassistant.chains.llm_provider import LLMProvider

def simple_chat_chain(input_dict):
    # Expect input_dict to have 'question' and 'llm_config'
    question = input_dict["question"]
    llm_config = input_dict["llm_config"]

    llm = LLMProvider(**llm_config).get_llm()

    # Format prompt for chat
    prompt_msg = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question,
                }
            ],
        }
    ]

    return llm.invoke(prompt_msg)




