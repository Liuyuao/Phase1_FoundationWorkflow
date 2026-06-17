import boto3
import operator
from typing import Literal, TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
import config

# Initialize a single, shared Bedrock client
bedrock_client = boto3.client('bedrock-agent-runtime', region_name=REGION)

def call_knowledge_base(question: str, domain: str) -> str:
    """Helper function to call Bedrock KB using central configs"""
    try:
        response = bedrock_client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_IDS[domain],
                    "modelArn": MODEL_ARN,
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": PROMPTS[domain]
                        },
                        # Inject the inference configuration here
                        "inferenceConfig": INFERENCE_CONFIG
                    }
                }
            }
        )
        return response["output"]["text"]
    except Exception as e:
        return f"Error querying {domain} agent: {str(e)}"

# Define Shared State
class AgentState(TypedDict):
    question: str
    active_agent: str
    final_answer: str
    messages: Annotated[list, operator.add]

# Nodes
def policy_node(state: AgentState) -> dict:
    answer = call_knowledge_base(state["question"], "policy")
    return {"final_answer": answer, "active_agent": "Policy Agent", "messages": [{"role": "assistant", "content": answer}]}

def claims_node(state: AgentState) -> dict:
    answer = call_knowledge_base(state["question"], "claims")
    return {"final_answer": answer, "active_agent": "Claims Agent", "messages": [{"role": "assistant", "content": answer}]}

def product_node(state: AgentState) -> dict:
    answer = call_knowledge_base(state["question"], "product")
    return {"final_answer": answer, "active_agent": "Product Agent", "messages": [{"role": "assistant", "content": answer}]}

# Routing Workflow (Your explicit supervisor logic)
def router_workflow(state: AgentState) -> Literal["policy_node", "claims_node", "product_node"]:
    question = state["question"].lower()
    
    policy_keywords = ["premium", "coverage", "deductible", "limit", "liability", "collision", "comprehensive", "policy", "term"]
    claims_keywords = ["claim", "accident", "crash", "damage", "repair", "total loss", "file", "report", "settlement"]
    products_keywords = ["discount", "save", "offer", "multi-policy", "multi-car", "student", "driver"]
    
    if any(kw in question for kw in claims_keywords):
        return "claims_node"
    elif any(kw in question for kw in products_keywords):
        return "product_node"
    else:
        return "policy_node"  # Fallback router destination

# Construct LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("router", lambda s: s)
workflow.add_node("policy_node", policy_node)
workflow.add_node("claims_node", claims_node)
workflow.add_node("product_node", product_node)

workflow.add_edge(START, "router")
workflow.add_conditional_edges(
    "router",
    router_workflow,
    {
        "policy_node": "policy_node",
        "claims_node": "claims_node",
        "product_node": "product_node"
    }
)
workflow.add_edge("policy_node", END)
workflow.add_edge("claims_node", END)
workflow.add_edge("product_node", END)

# Compile the executable system
agent_app = workflow.compile()