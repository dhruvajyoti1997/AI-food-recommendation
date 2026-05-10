import json
import logging
from agents.base_agent import BaseAgent

logger = logging.getLogger("swiggy-food-recommendation")


class FoodDiscoveryAgent(BaseAgent):

    def __init__(self, swiggy_tool):
        self.swiggy_tool = swiggy_tool

    def _normalise_restaurants(self, raw: list) -> list:
        self._log_raw_shape(raw)

        normalised = []
        for entry in raw:
            restaurant_name = (
                entry.get("name")
                or entry.get("restaurant_name")
                or "Unknown Restaurant"
            )
            rating = entry.get("rating")
            distance_km = entry.get("distance_km") or entry.get("distance")
            menu_items = (
                entry.get("menu")
                or entry.get("dishes")
                or entry.get("items")
                or []
            )

            if menu_items:
                for menu_item in menu_items:
                    dish_name = (
                        menu_item.get("dish")
                        or menu_item.get("name")
                        or menu_item.get("item_name")
                        or ""
                    )
                    if not dish_name:
                        continue
                    normalised.append({
                        "dish": dish_name,
                        "restaurant_name": restaurant_name,
                        "price": menu_item.get("price") or menu_item.get("cost"),
                        "rating": rating,
                        "distance_km": distance_km,
                    })
            elif entry.get("dish") or entry.get("item_name"):
                normalised.append({
                    "dish": entry.get("dish") or entry.get("item_name"),
                    "restaurant_name": restaurant_name,
                    "price": entry.get("price") or entry.get("cost"),
                    "rating": rating,
                    "distance_km": distance_km,
                })

            else:
                logger.warning(
                    "Unrecognised entry shape — keys found: %s", list(entry.keys())
                )

        logger.debug(
            "Normalised %d raw entries → %d dish entries", len(raw), len(normalised)
        )
        return normalised

    def _log_raw_shape(self, raw: list):
        logger.info("=" * 60)
        logger.info("RAW SWIGGY MCP RESPONSE — inspect to confirm shape:")
        logger.info(json.dumps(raw[:2], indent=2, default=str))  # log first 2 entries only
        logger.info("=" * 60)

    def execute(self, state: dict) -> dict:
        raw = self.swiggy_tool.search_healthy_food(
            ##location=state["location"],
            budget=state["budget"],
            distance_km=state["distance_km"],
        )
        if not raw:
            logger.warning(
                "Swiggy MCP returned no results. "
                "Check: (1) OAuth approved? (3) budget sufficient?"
            )
            state["restaurant"] = []
            return state

        state["restaurant"] = self._normalise_restaurants(raw)
        logger.info("FoodDiscoveryAgent: %d dishes found", len(state["restaurant"]))
        return state

    def run(self, state: dict) -> dict:
        return self.execute(state)