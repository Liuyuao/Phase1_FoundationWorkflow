import os
import sys
# Add parent folder to Python import path so config.py can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import boto3
# Import the finalized prompt and KB ID from your central config
import config 

bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name=config.REGION)

def test_policy_prompt(question):
    response = bedrock_runtime.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": config.KB_IDS["policy"], # Uses central ID
                "modelArn": config.MODEL_ARN,
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": config.PROMPTS["policy"] # Uses central prompt!
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
        "What does liability coverage cover?",
        #"What's the difference between collision and comprehensive coverage?",
        #"What is a deductible? Give me an example.",
        "My friend borrowed my car and got into an accident. Am I covered?",
        #"What discounts does Travelers offer to save money?",
        #"Does comprehensive coverage cover a tree falling on my car?", 
        #"What is gap insurance? Who needs it?",
        #"I just bought a new car. How long do I have to tell my insurance company?",
        #"What factors determine my premium?",
        #"I drive for Uber. Does my personal auto policy cover me?"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        answer = test_policy_prompt(q)
        print(f"Answer: {answer}")