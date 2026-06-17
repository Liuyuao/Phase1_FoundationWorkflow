import os
import sys
# Add parent folder to Python import path so config.py can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import boto3
# Import the finalized prompt and KB ID from your central config
import config 

bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name=config.REGION)

def test_claims_prompt(question):
    response = bedrock_runtime.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": config.KB_IDS["claims"], # Uses central ID
                "modelArn": config.MODEL_ARN,
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": config.PROMPTS["claims"] # Uses central prompt!
                    },
                    # Inject the inference configuration here
                    "inferenceConfig": config.INFERENCE_CONFIG
                }
            }
        }
    )
    return response["output"]["text"]

if __name__ == "__main__":
    questions = [
        #"What should I do immediately after a car accident?",
        "My friend borrowed my car and got into an accident. Am I covered?",
        #"What documents do I need to file a claim?",
        #"How long does the claims process take?",
        #"What happens if my car is declared a total loss?",
        #"Can I choose my own repair shop?",
        #"What is the difference between an estimate and an actual repair cost?",
        #"How long do I have to report an accident to Travelers?",
        "Will my insurance rates go up if I file a claim?",
        #"What is a deductible and when do I pay it?",
        #"What does 'subrogation' mean in the claims process?"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        answer = test_claims_prompt(q)
        print(f"Answer: {answer}")