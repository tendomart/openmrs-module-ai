import configparser
from sqlalchemy import (
    create_engine,
    MetaData,
    inspect,
    text,
)
from smolagents import tool, LiteLLMModel, HfApiModel
from smolagents import CodeAgent
from huggingface_hub import login
from DatabaseTables import openmrs_tables

# using Ollama
# model = LiteLLMModel(
#     model_id="ollama_chat/qwen2.5-coder:1.5b",  # ID of the model you are using
#     api_key=None,  # No API key required for local Ollama usage
#     endpoint="http://localhost:11434", # Default local server endpoint for Ollama
#     provider="ollama"
# )

model=LiteLLMModel(model_id="qwen2.5-coder"
                   api_key="ollama",
                   )


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


# Log in to Hugging Face Hub
# login("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")
# login(config["DEFAULT"]["hugging_face_login_key"])

# Dynamic SQL engine description update
updated_description = """Allows you to perform SQL queries on the database. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:"""

# Fetch table metadata dynamically
inspector = inspect(engine)
# for table in ["users", "person", "patient", "orders", "program"]:
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

# Initialize the CodeAgent with the SQL engine tool and Hugging Face model
# Using HuggingFace hosted model Qwen/Qwen2.5-72B-Instruct
# agent = CodeAgent(
#     tools=[sql_engine],
#     # model=HfApiModel("Qwen/Qwen2.5-72B-Instruct"),
#     model=HfApiModel("Qwen/QwQ-32B"),
# )

# Run the agent with an SQL query
# agent.run("Which waiter got more total money from tips?")
# agent.run("Display all users")
# agent.run("Get me the program name whose id is 4")
# agent.run("What is the name of the patient whose id is 1?")
# response = agent.run("What's the description of the role whose uuid is 8d94f280-c2cc-11de-8d13-0010c6dffd0f ?")

# Agent two using model hosted locally by Ollama
agent = CodeAgent(
    tools=[sql_engine],
    model=model,
    # add_base_tools=True
)

response = agent.run("What's the description of the role whose uuid is 93a9c2f8-9296-488f-9451-43667e1c4d7f ?")
print(response)