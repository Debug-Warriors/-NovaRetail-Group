"""
Central LLM configuration.
"""

import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama

load_dotenv()

# Enable LangSmith

os.environ["LANGSMITH_TRACING"] = os.getenv(
    "LANGSMITH_TRACING",
    "true"
)

os.environ["LANGSMITH_API_KEY"] = os.getenv(
    "LANGSMITH_API_KEY",
    ""
)

os.environ["LANGSMITH_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT",
    "NovaRetail-SupplyChain"
)

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)