import os
import sys
# Add parent folder to Python import path so config.py can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import boto3
# Import the finalized prompt and KB ID from your central config
import config 

bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name=config.REGION)

def test_product_prompt(question):
    response = bedrock_runtime.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": config.KB_IDS["product"], # Uses central ID
                "modelArn": config.MODEL_ARN,
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": config.PROMPTS["product"] # Uses central prompt!
                    },
                    # Inject the inference configuration here
                    "inferenceConfig": config.INFERENCE_CONFIG
                }
            }
        }
    )
    return response["output"]["text"]

# TESTING
if __name__ == "__main__":
    questions = [
            #"What discounts does Travelers offer?",
            "Does Travelers have a multi-policy discount?",
            #"Does Travelers have a multi-car discount?",
            "What is the good student discount?",
            "Does Travelers offer a safe driver discount?"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        answer = test_product_prompt(q)
        print(f"Answer: {answer}")