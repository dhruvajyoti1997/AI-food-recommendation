import logging

logger = logging.getLogger("zomato-food-recommendation")


def build_nutrition_estimation_prompt(dish_name: str) -> str:
    return f"""
You are a nutrition database expert with deep knowledge of food composition.

Estimate the nutritional content for ONE serving of: "{dish_name}"

Think step by step:
- Consider typical portion size for this dish
- Factor in common ingredients and cooking method
- Provide realistic estimates based on standard recipes

Return ONLY this strict JSON with no explanation, no markdown, no preamble:
{{
  "calories": <integer>,
  "protein": "<number>g",
  "carbs": "<number>g",
  "fat": "<number>g"
}}
"""


def build_nutrition_reasoning_prompt(goal: str, nutritional_info: dict) -> str:
    logger.debug(
        "Building nutrition reasoning prompt | goal: %s | info: %s",
        goal,
        nutritional_info,
    )
    return f"""
You are a nutrition expert.

Goal: {goal}
Nutrition Data:
{nutritional_info}

Use ReAct reasoning internally:
Thought -> Understand whether meal fits goal
Observation -> Analyze calories/protein/carbs/fat
Final Answer -> Return STRICT JSON ONLY

Return JSON in this format:
{{
  "suitable_for_goal": true,
  "reason": "short explanation"
}}
"""