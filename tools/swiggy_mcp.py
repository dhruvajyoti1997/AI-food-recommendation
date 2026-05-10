import asyncio
import json
import logging
from typing import Optional
from langchain_mcp_adapters import client
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger("swiggy-food-recommendation")


class SwiggyMCP:

    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url
        self.server_config = {
            "swiggy-food": {
                "transport": "http",
                "url": self.mcp_url,
            }
        }

    def _run_async(self, coro):
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        except RuntimeError:
            return asyncio.run(coro)

    async def _call_tool_async(self, tool_name: str, tool_args: dict) -> Optional[str]:
            logger.debug("Calling MCP tool '%s' with args: %s", tool_name, tool_args)
            client = MultiServerMCPClient(self.server_config)
            tools = await client.get_tools()
            logger.debug("Available Swiggy MCP tools: %s", [t.name for t in tools])

            tool = next((t for t in tools if t.name == tool_name), None)
            if not tool:
                logger.error(
                    "Tool '%s' not found on MCP server. Available tools: %s",
                    tool_name,
                    [t.name for t in tools],
                )
                return None

            result = await tool.ainvoke(tool_args)
            logger.debug("MCP tool '%s' raw result: %s", tool_name, result)
            return result

    def _parse_result(self, raw) -> list:
        if not raw:
            logger.warning("MCP returned empty/None result")
            return []

        if isinstance(raw, list):
            return raw

        if isinstance(raw, dict):
            # Check if result is wrapped under a common key
            for key in ("restaurants", "results", "data", "items"):
                if key in raw and isinstance(raw[key], list):
                    return raw[key]
            return [raw]

        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                return self._parse_result(parsed)
            except json.JSONDecodeError:
                logger.error(
                    "Failed to parse MCP response as JSON. First 300 chars: %s", raw[:300]
                )
                return []

        logger.error("Unexpected MCP result type: %s", type(raw))
        return []

    def search_healthy_food(
        self,
       ## location: dict,
        budget: int,
        distance_km: float,
        keyword: str = "healthy food",
    ) -> list:
        logger.info(
            "Searching healthy food | location: %s | budget: Rs.%s | radius: %skm",
           ## location, budget, distance_km,
        )

        tool_args = {
            "keyword": keyword,
            "address_id": "",
            "filter": {
                "max_price": budget,
                "distance": distance_km,
            },
        }

        try:
            raw = self._run_async(
                self._call_tool_async("get_restaurants_for_keyword", tool_args)
            )
            result = self._parse_result(raw)
            logger.info("Found %d results from Swiggy MCP", len(result))
            return result

        except Exception as e:
            logger.error("search_healthy_food failed: %s", e, exc_info=True)
            return []