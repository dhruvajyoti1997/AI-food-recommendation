from typing import TypedDict, List, Dict, Any


class FoodRecommendationState(TypedDict):
    user_query: str
    budget: int
    distance_km: int
    goal: str
   ## location: Dict[str, float]
    restaurant: List[Dict[str, Any]]
    nutrition_result: List[Dict[str, Any]]
    final_recommendation: str