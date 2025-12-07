from dotenv import load_dotenv
import yaml
from omniassistant.agents.ChatAgent.graph import app

# Load environment variables
load_dotenv()

# Set paths using pathlib for cross-platform support


def load_llm_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    for llm_type, params in config["llms"].items():
        if params.get("enabled"):
            llm_config = {"llm_type": llm_type}
            llm_config.update({k: v for k, v in params.items() if k != "enabled"})
            return llm_config
    raise ValueError("No enabled LLM found in config.")



def main():
    # Collect all questions
    question = "How can you assist today?"
    llm_config = load_llm_config("llm_config.yaml")
    input_state = {
        "llm_config": llm_config,
        "question": question,
    }

    result = app.invoke(input_state)
    print(result["model_prediction"])
    

            

if __name__ == "__main__":
    main()
