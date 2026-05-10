import time

def build_recommendation_prompt(goal, budget, nutritional_info):
    timestamp = int(time.time())
    return f"""
You are a diet recommendation expert.

Goal: {goal}
Budget: {budget}
Nutrition Data:
{nutritional_info}

Choose ONLY ONE best meal.
Explain:
1. Why this is best
2. Why others are weaker choices

Return final recommendation clearly.

Timestamp: {timestamp}
"""