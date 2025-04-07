import os

from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain_openai import ChatOpenAI

from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.chat_models import ChatOllama

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import os
from langchain.chat_models import ChatOllama
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine



# setup the tools
# @tool
# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b
#
# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b
#
# @tool
# def square(a) -> int:
#     """Calculates the square of a number."""
#     a = int(a)
#     return a * a
#
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", """You are a mathematical assistant.
#         Use your tools to answer questions. If you do not have a tool to
#         answer the question, say so.
#
#         Return only the answers. e.g
#         Human: What is 1 + 1?
#         AI: 2
#         """),
#         MessagesPlaceholder("chat_history", optional=True),
#         ("human", "{input}"),
#         MessagesPlaceholder("agent_scratchpad"),
#     ]
# )

MODEL = "qwen2.5-coder:0.5b"

# Initialize a language model (LLM)
# llm = ChatOllama(model=MODEL)
#
# # setup the toolkit
# toolkit = [add, multiply, square]
#
# # Construct the OpenAI Tools agent
# agent = create_openai_tools_agent(llm, toolkit, prompt)
#
# # Create an agent executor by passing in the agent and tools
# agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)
#
# result = agent_executor.invoke({"input": "what is 56.9032* 23.347?"})
#
# print(result['output'])


# MySQL Connection Details
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "JesusChrist"
MYSQL_HOST = "localhost"  # e.g., "localhost" or IP
MYSQL_PORT = "3306"  # Default MySQL port
MYSQL_DATABASE = "openmrs-ai"

# Create MySQL connection URI
mysql_uri = f"mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Initialize MySQL Database Connection
db = SQLDatabase.from_uri(mysql_uri)



# Initialize LLM Model (Using Ollama)
# MODEL = "llama3.2"
llm = ChatOllama(model=MODEL, streaming=True)

# SQL Query Executor Tool
sql_tool = Tool(
    name="SQL Query Executor",
    func=db.run,
    description="Executes SQL queries and retrieves results from MySQL."
)

# Example Query Execution
query = "SELECT COUNT(*) FROM orders ;"
result = sql_tool.run(query)
print("Total Count"+ result)