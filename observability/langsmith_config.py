import os
from dotenv import load_dotenv
load_dotenv()
def setup_langsmith():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "swiggy-food-recommendation"
    os.environ["LANGCHAIN_API_KEY"] =  os.getenv("LANGSMITH_API_KEY")