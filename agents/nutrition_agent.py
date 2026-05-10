import json
import logging
from typing import Optional
from agents.base_agent import BaseAgent
from prompts.nutrition_prompt import (
    build_nutrition_estimation_prompt,
    build_nutrition_reasoning_prompt,
)

logger = logging.getLogger("zomato-food-recommendation")


class NutritionAgent(BaseAgent):

    def __init__(self, llm):
        self.llm = llm

    def _clean_llm_response(self, raw: str) -> str:
        """
        FIX: Extracted repeated markdown-stripping logic into one reusable method.
        Both _estimate_nutrition and _assess_suitability had the exact same
        raw.split() block copy-pasted — now it lives in one place.

        FIX: raw.split('```')[1] crashes with IndexError if there is only one
        backtick fence or none at all. Now safely checks list length before indexing.
        """
        raw = raw.strip()
        if raw.startswith("```"):
            parts = raw.split("```")
            if len(parts) >= 2:
                raw = parts[1]
                if raw.startswith("json"):
                    raw = raw[4:]
        return raw.strip()

    def _estimate_nutrition(self, dish_name: str) -> Optional[dict]:
        """
        Calls Ollama to estimate nutrition for the dish.
        Returns a dict with calories/protein/carbs/fat, or None on failure.

        FIX: Return type changed from 'dict | None' to Optional[dict].
        The union syntax (dict | None) requires Python 3.10+.
        Optional[dict] works from Python 3.7+ — broader compatibility.
        """
        prompt = build_nutrition_estimation_prompt(dish_name)
        try:
            response = self.llm.invoke(prompt)
            cleaned = self._clean_llm_response(response.content)
            nutrition = json.loads(cleaned)
            logger.debug("Nutrition estimated for '%s': %s", dish_name, nutrition)
            return nutrition
        except (json.JSONDecodeError, AttributeError) as e:
            logger.warning("Failed to parse nutrition estimate for '%s': %s", dish_name, e)
            return None

    def _assess_suitability(self, goal: str, dish_name: str, nutrition: dict) -> dict:
        """
        Calls Ollama to judge whether the dish suits the user's health goal.
        Returns dict with suitable_for_goal (bool) and reason (str).
        """
        prompt = build_nutrition_reasoning_prompt(goal, {"dish": dish_name, **nutrition})
        try:
            response = self.llm.invoke(prompt)
            cleaned = self._clean_llm_response(response.content)
            return json.loads(cleaned)
        except (json.JSONDecodeError, AttributeError) as e:
            logger.warning("Failed to parse suitability for '%s': %s", dish_name, e)
            return {
                "suitable_for_goal": False,
                "reason": "Unable to confidently determine suitability",
            }

    def execute(self, state: dict) -> dict:
        nutrition_result = []

        for item in state["restaurant"]:
            dish_name = item.get("dish")
            restaurant_name = item.get("restaurant_name", "Unknown Restaurant")

            if not dish_name:
                logger.warning("Skipping item with no dish name: %s", item)
                continue

            logger.info("Analysing nutrition for '%s' @ %s", dish_name, restaurant_name)

            nutrition = self._estimate_nutrition(dish_name)
            if not nutrition:
                logger.warning("Skipping '%s' — nutrition estimation failed", dish_name)
                continue

            suitability = self._assess_suitability(state["goal"], dish_name, nutrition)

            nutrition_result.append({
                "dish": dish_name,
                "restaurant_name": restaurant_name,
                "calories": nutrition.get("calories"),
                "protein": nutrition.get("protein"),
                "carbs": nutrition.get("carbs"),
                "fat": nutrition.get("fat"),
                "suitable_for_goal": suitability.get("suitable_for_goal", False),
                "reason": suitability.get("reason", "No reasoning available"),
                "source": "Ollama (estimated)",
            })

        logger.info(
            "Nutrition analysis complete: %d/%d dishes processed",
            len(nutrition_result),
            len(state["restaurant"]),
        )
        state["nutrition_result"] = nutrition_result
        return state

    def run(self, state: dict) -> dict:
        return self.execute(state)