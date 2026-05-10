# Swiggy Food Recommendation System

An **agentic AI system** leveraging **multi-agent orchestration** and **Model Context Protocol (MCP)** to provide personalized food recommendations based on nutritional goals, budget constraints, and location preferences.

## 🎯 Project Overview

This project implements an intelligent food discovery and recommendation pipeline that:
- **Discovers** healthy restaurant options via Swiggy MCP tool integration
- **Analyzes** nutritional profiles using local LLM inference (Ollama)
- **Recommends** cuisine choices aligned with user health objectives

The system orchestrates multiple autonomous agents through a **LangGraph-based state machine workflow**, enabling complex multi-step reasoning with structured state management and observability.

---

## 🏗️ Architecture & Design Patterns

### 1. **Multi-Agent Architecture**
The system employs a specialized **agent-based reasoning** pattern where each agent encapsulates domain-specific logic:

- **FoodDiscoveryAgent**: Searches and normalizes restaurant data
- **NutritionAgent**: Estimates nutritional content and evaluates suitability
- **RecommendationAgent**: Synthesizes findings into user-facing recommendations

Each agent inherits from `BaseAgent` (Abstract Base Class pattern), enforcing a consistent `run()` interface.

### 2. **Agentic Workflow Orchestration (LangGraph)**
The project uses **LangGraph** to construct a **Directed Acyclic Graph (DAG)** workflow:

```
food_discovery → nutrition_analysis → recommendation → END
```

This implements the **State Machine** pattern with:
- **StateGraph**: Defines node topology and control flow
- **Typed State (TypedDict)**: Ensures type safety across agent transitions
- **Compiled Workflow**: Optimized execution with lazy evaluation

### 3. **Model Context Protocol (MCP) Integration**
External tool access is abstracted via **MCP** standard, enabling:
- **Pluggable Tool Integration**: Swiggy data exposed as callable tools via HTTP
- **MultiServerMCPClient**: Dynamic tool discovery and invocation
- **Async Tool Calling**: Non-blocking tool execution via `ainvoke()`

### 4. **Prompt Engineering & Template Pattern**
LLM behavior is controlled through structured **prompt templates**:
- **Nutrition Estimation Prompt**: Guides JSON-formatted output
- **Nutrition Reasoning Prompt**: Elicits goal-alignment reasoning
- **Recommendation Prompt**: Orchestrates final synthesis

### 5. **Language Model Integration (Ollama)**
Local LLM execution via **Ollama** using **llama3** model:
- **Zero-Temperature Sampling**: Deterministic outputs for consistency
- **Structured Output**: JSON parsing for programmatic access
- **In-Process Inference**: No external API dependencies

### 6. **State Management & Data Flow**
Central state object (`FoodRecommendationState`) manages:
- **User Inputs**: query, budget, distance, health goal
- **Intermediate Results**: restaurant list, nutrition analysis
- **Final Output**: synthesized recommendation

Agents are **pure functions** (state-in, state-out) enabling:
- Replay and checkpointing
- Distributed execution
- Composable reasoning

### 7. **Observability & Tracing**
**LangSmith** integration provides:
- **Execution Traces**: Track agent decisions and LLM invocations
- **Token Accounting**: Monitor API costs and latency
- **Debug Logs**: Comprehensive logging at DEBUG/INFO levels

### 8. **MCP Tool Integration Pattern**
External data access via Model Context Protocol:
- Tools discovered dynamically from MCP server at runtime
- Agents invoke tools via async client: `MultiServerMCPClient`
- Results integrated into agent reasoning pipeline

---

## 📋 Project Structure

```
swiggy-food-recommendation/
├── main.py                          # Entry point & orchestration
├── requirements.txt                 # Python dependencies
│
├── agents/                          # Agent implementations
│   ├── base_agent.py               # Abstract base class (Template Method)
│   ├── food_discovery_agent.py     # Restaurant & menu discovery
│   ├── nutrition_agent.py          # Nutritional analysis & suitability
│   └── recommendation_agent.py     # Final recommendation synthesis
│
├── graph/                           # Workflow graph definition
│   ├── builder.py                  # DAG construction & compilation
│   └── state.py                    # StateGraph TypedDict schema
│
├── llm/                            # Language model interface
│   └── ollama_client.py            # ChatOllama configuration
│
├── tools/                          # External tool integration
│   └── swiggy_mcp.py              # MCP client for Swiggy tools
│
├── prompts/                        # Prompt templates
│   ├── nutrition_prompt.py         # Nutrition estimation & reasoning prompts
│   └── recommendation_prompt.py    # Final recommendation prompt
│
└── observability/                  # Monitoring & telemetry
    └── langsmith_config.py         # LangSmith tracing setup
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Ollama running locally on `http://localhost:11434`
- Swiggy MCP server accessible and running
- (Optional) LangSmith API key for observability

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd swiggy-food-recommendation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file with:
   LANGSMITH_API_KEY=your_key_here
   LANGSMITH_PROJECT=your_project
   ```

5. **Configure MCP Server**
   - Update `.vscode/mcp.json` with your Swiggy MCP server URL:
     ```json
     {
       "servers": {
         "swiggy-food": {
           "transport": "http",
           "url": "http://your-mcp-server:port"
         }
       }
     }
     ```

6. **Start Ollama Service**
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull llama3 model
   ollama pull llama3
   
   # Start Ollama server (default: http://localhost:11434)
   ollama serve
   ```

---

## ⚙️ Setup Requirements

Before running the application, ensure:

| Component | Purpose | Setup |
|-----------|---------|-------|
| **Ollama** | Local LLM execution for nutrition analysis & recommendations | Install from [ollama.ai](https://ollama.ai), pull `llama3` model, keep server running on port 11434 |
| **Swiggy MCP Server** | External tool providing restaurant & menu data | Deploy/start your Swiggy MCP server, note the URL (e.g., `http://localhost:8000`) |
| **Python Dependencies** | Required packages listed in `requirements.txt` | Install via `pip install -r requirements.txt` |
| **LangSmith (Optional)** | Observability & tracing for agent execution | Set `LANGSMITH_API_KEY` in `.env` for production monitoring |

---

## 📦 Requirements.txt Breakdown

The `requirements.txt` file contains all necessary Python dependencies:

```
langchain-mcp-adapters      # MCP client for connecting to external tool servers
langgraph                   # Workflow orchestration & state machine (DAG)
langchain                   # LLM framework & agent abstractions
langchain-community         # Community integrations (tools, utilities)
langchain-ollama            # ChatOllama integration for Ollama LLM
langsmith                   # Observability, tracing & debugging
ollama                      # Python client for Ollama
python-dotenv               # Load environment variables from .env
```

**Dependency Verification:**
- ✅ All imports used in the codebase are covered
- ✅ `langchain-ollama` added for `ChatOllama` used in `llm/ollama_client.py`
- ✅ `langchain-mcp-adapters` for MCP tool integration
- ✅ `langgraph` for workflow orchestration
- ✅ All dependencies are pinned in a consistent state

### Running the Application

```bash
python main.py
```

**Example Output:**
```
===== FINAL RECOMMENDATION =====

Based on your weight loss goal and ₹300 budget, I recommend:
1. Grilled Chicken Salad @ Healthy Eats (₹280)
   - Calories: 320 | Protein: 35g | Carbs: 15g | Fat: 8g
   - Distance: 2.3 km | Rating: 4.5/5
```

---

## 🔄 Workflow Execution Flow

### Phase 1: Food Discovery
**Agent**: `FoodDiscoveryAgent`
- **Input**: user_query, budget, distance_km
- **Operation**: Calls Swiggy MCP tool `search_healthy_food()`
- **Processing**: Normalizes heterogeneous API responses into uniform schema
- **Output**: Populates `state["restaurant"]` with filtered options

### Phase 2: Nutrition Analysis
**Agent**: `NutritionAgent`
- **Input**: restaurant list from Phase 1
- **Operation**:
  1. Estimates nutritional profile for each dish via LLM
  2. Assesses suitability against user's health goal
  3. Returns structured nutrition data + goal alignment
- **Output**: Populates `state["nutrition_result"]`

### Phase 3: Recommendation Synthesis
**Agent**: `RecommendationAgent`
- **Input**: nutrition_result + user goal/budget
- **Operation**: Synthesizes analysis into human-readable recommendation
- **Output**: Generates `state["final_recommendation"]`

---

## 🧠 Key Design Principles

### 1. **Separation of Concerns**
Each agent owns a single responsibility:
- Discovery ≠ Analysis ≠ Synthesis
- Easy to test, extend, or replace components

### 2. **Immutable State Transitions**
Agents don't mutate state in-place; each returns a new state dict:
- Enables replay, checkpointing, parallel execution
- Reduces side effects and debugging surface

### 3. **Resilience & Graceful Degradation**
- Missing Swiggy results → empty list (not crash)
- LLM JSON parsing fails → logged warning + fallback
- Tool not found → error logged, execution continues

### 4. **Explicit Data Schemas**
- `FoodRecommendationState` (TypedDict) → compile-time type checking
- Prompt templates → consistent LLM input/output format
- Normalized restaurant schema → handles API schema variations

### 5. **Composability**
- Agents are pure functions: `state → state`
- Graph is DAG-based: linear composition possible
- Tools are interchangeable via MCP standard

## 📦 Requirements.txt Breakdown

The `requirements.txt` file contains all necessary Python dependencies:

```
langchain-mcp-adapters      # MCP client for connecting to external tool servers
langgraph                   # Workflow orchestration & state machine (DAG)
langchain                   # LLM framework & agent abstractions
langchain-community         # Community integrations (tools, utilities)
langchain-ollama            # ChatOllama integration for Ollama LLM
langsmith                   # Observability, tracing & debugging
ollama                      # Python client for Ollama
python-dotenv               # Load environment variables from .env
```

**Dependency Verification:**
- ✅ All imports used in the codebase are covered
- ✅ `langchain-ollama` added for `ChatOllama` used in `llm/ollama_client.py`
- ✅ `langchain-mcp-adapters` for MCP tool integration
- ✅ `langgraph` for workflow orchestration
- ✅ All dependencies are pinned in a consistent state

### Running the Application

```bash
python main.py
```

**Example Output:**
```
===== FINAL RECOMMENDATION =====

Based on your weight loss goal and ₹300 budget, I recommend:
1. Grilled Chicken Salad @ Healthy Eats (₹280)
   - Calories: 320 | Protein: 35g | Carbs: 15g | Fat: 8g
   - Distance: 2.3 km | Rating: 4.5/5
```

---

## 🔧 Configuration

### Environment Variables (`.env`)
```env
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=swiggy-food-recommendation
OLLAMA_MODEL=llama3
OLLAMA_TEMPERATURE=0
```

### MCP Configuration (`.vscode/mcp.json`)
```json
{
  "servers": {
    "swiggy-food": {
      "transport": "http",
      "url": "http://localhost:8000"
    }
  }
}
```

---

## 🧪 Testing & Debugging

### Enable Debug Logging
```python
logging.basicConfig(level=logging.DEBUG)
```

### Inspect MCP Tools
```bash
# In swiggy_mcp.py, tools are discovered at runtime:
available_tools = await client.get_tools()
print([t.name for t in available_tools])
```

### View LangSmith Traces
1. Visit [LangSmith Dashboard](https://smith.langchain.com)
2. Navigate to your project
3. View execution traces, token usage, and latency

---

## 🚦 Common Issues & Troubleshooting

### Issue: "Swiggy MCP returned no results"
**Cause**: MCP server not running or unreachable
**Solution**: 
- Verify `.vscode/mcp.json` URL is correct
- Check MCP server is running: `curl http://your-mcp-server:port/health`

### Issue: "Tool 'search_healthy_food' not found"
**Cause**: MCP tool name mismatch or server not loaded
**Solution**:
- Run `SwiggyMCP._call_tool_async()` with logging to inspect available tools
- Ensure Swiggy MCP server has exported the tool correctly

### Issue: "Failed to parse nutrition estimate"
**Cause**: LLM returned non-JSON or malformed response
**Solution**:
- Set `OLLAMA_TEMPERATURE=0` for consistent JSON output
- Check LLM model supports structured generation
- Review prompt templates in `prompts/nutrition_prompt.py`

---

## 📖 Future Enhancements

- [ ] **Caching Layer**: Cache nutrition estimates for repeated dishes
- [ ] **Fine-tuned Models**: Domain-specific LLM fine-tuning
- [ ] **Multi-Objective Optimization**: Pareto frontier of budget/nutrition/distance
- [ ] **User Feedback Loop**: Reinforcement from user preferences
- [ ] **Async Parallelization**: Parallel agent execution for faster inference
- [ ] **A/B Testing**: Recommendation quality evaluation framework

---
