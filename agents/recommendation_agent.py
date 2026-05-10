from agents.base_agent import BaseAgent
from prompts.recommendation_prompt import build_recommendation_prompt


class RecommendationAgent(BaseAgent):

    def __init__(self, llm):
        self.llm = llm

    def execute(self, state):
        if not state["nutrition_result"]:
            state["final_recommendation"] = "No restaurant data available from Swiggy MCP. Please check your MCP server configuration and try again."
            return state

        prompt = build_recommendation_prompt(
            state["goal"],
            state["budget"],
            state["nutrition_result"]
        )

        response = self.llm.invoke(prompt)
        state["final_recommendation"] = response.content
        return state
    def run(self, state):
        return self.execute(state)