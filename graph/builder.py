from langgraph.graph import StateGraph, END
from graph.state import FoodRecommendationState
from tools.zomato_mcp import ZomatoMCP
from llm.ollama_client import get_llm
from agents.food_discovery_agent import FoodDiscoveryAgent
from agents.nutrition_agent import NutritionAgent
from agents.recommendation_agent import RecommendationAgent


def build_food_recommendation_graph(mcp_url: str):
    zomato_tool = ZomatoMCP(mcp_url)
    llm = get_llm()

    food_agent = FoodDiscoveryAgent(zomato_tool)
    nutrition_agent = NutritionAgent(llm)
    recommendation_agent = RecommendationAgent(llm)

    workflow = StateGraph(FoodRecommendationState)

    workflow.add_node("food_discovery", food_agent.run)
    workflow.add_node("nutrition_analysis", nutrition_agent.run)
    workflow.add_node("recommendation", recommendation_agent.run)

    workflow.set_entry_point("food_discovery")
    workflow.add_edge("food_discovery", "nutrition_analysis")
    workflow.add_edge("nutrition_analysis", "recommendation")
    workflow.add_edge("recommendation", END)

    return workflow.compile()