import configparser
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    inspect,
    text,
)
from smolagents import tool, LiteLLMModel
from smolagents import CodeAgent, DuckDuckGoSearchTool
from DatabaseTables import openmrs_tables
from smolagents.utils import AgentGenerationError
from smolagents.agents import ToolCallingAgent
from typing import Optional
import requests
import time


# Define a validation function to ensure Ollama server connectivity
def validate_server(endpoint: str) -> bool:
    """
    Validates the connection to a given endpoint.
    Returns True if the server is reachable, otherwise False.
    """
    try:
        response = requests.get(f"{endpoint}/health")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Ollama server: {e}")
        return False


# Replace the following values with your MySQL database credentials
config = configparser.ConfigParser()
config.read("db_config.properties")

mysql_user = config["DEFAULT"]["mysql_user"]
mysql_password = config["DEFAULT"]["mysql_password"]
mysql_host = config["DEFAULT"]["mysql_host"]
mysql_port = int(config["DEFAULT"]["mysql_port"])
mysql_db = config["DEFAULT"]["mysql_db"]

# Create the SQLAlchemy engine for MySQL using the PyMySQL driver
engine = create_engine(
    f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
)
metadata_obj = MetaData()

metadata_obj.create_all(engine)  # Create the table in the MySQL database


# Define the sql_engine tool
@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the database. Returns a string representation of the result.
    The database contains the following tables (All Tables in the OpenMRS Database):
        - users
        - person
        - patient
        - orders
        - program
        - e.t.c

    Args:
        query: The query to perform. This should be correct SQL.
    """
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output


# Dynamic SQL engine description update
updated_description = """Allows you to perform SQL queries on the database. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:"""

# Fetch table metadata dynamically
inspector = inspect(engine)
for table in openmrs_tables:
    columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]
    table_description = f"Table '{table}':\n"
    table_description += "Columns:\n" + "\n".join(
        [f"  - {name}: {col_type}" for name, col_type in columns_info]
    )
    updated_description += "\n\n" + table_description
print(updated_description)

# Attach updated description to the tool
sql_engine.description = updated_description

# Use LiteLLMModel with Ollama
# ollama_endpoint = "127.0.0.1:11434"

# Validate server
# if not validate_server(ollama_endpoint):
#     raise ConnectionError(f"Cannot connect to Ollama server at {ollama_endpoint}. Please ensure the server is running.")

# Instantiate the LiteLLMModel with Ollama parameters
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:1.5b",  # ID of the model being used
    # endpoint=ollama_endpoint,  # Ollama's endpoint
    provider="ollama"
)

# Initialize the CodeAgent with the SQL engine tool and the Ollama LLM model
agent = CodeAgent(
    tools=[sql_engine],
    model=model,
    add_base_tools=True
)

# Run the agent with an SQL query
retry_limit = 3  # Retry in case of temporary failures
for attempt in range(retry_limit):
    try:
        # Run the code agent with a sample query
        response = agent.run("What's the description of the role whose uuid is 8d94f280-c2cc-11de-8d13-0010c6dffd0f?")
        print("Response:", response)
        break
    except AgentGenerationError as e:
        print(f"AgentGenerationError on attempt {attempt + 1}/{retry_limit}: {e}")
        time.sleep(2)  # Wait between retries
    except Exception as e:
        print(f"Unexpected error on attempt {attempt + 1}/{retry_limit}: {e}")
        break
else:
    print("All attempts to query the agent failed.")
