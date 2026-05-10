import logging
import json
from graph.builder import build_food_recommendation_graph as build_graph
from observability.langsmith_config import setup_langsmith

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("zomato-food-recommendation")

with open(".vscode/mcp.json", "r") as f:
    mcp_config = json.load(f)
    mcp_url = mcp_config["servers"]["zomato-mcp"]["url"]


def main():
    logger.info("Application started")
    setup_langsmith()

    app = build_graph(mcp_url)
    logger.debug("Graph built successfully")

    initial_state = {
        "user_query": "Suggest healthy food under 300 rupees",
        "budget": 300,
        "distance_km": 5,
        "goal": "weight loss",
        ##"location": {"latitude": 17.385, "longitude": 78.4867},
        "restaurant": [],
        "nutrition_result": [],
        "final_recommendation": "",
    }

    logger.debug("Initial state: %s", initial_state)

    result = app.invoke(initial_state)

    logger.info("Final recommendation generated")
    print("\n===== FINAL RECOMMENDATION =====\n")
    print(result["final_recommendation"])


if __name__ == "__main__":
    main()