import streamlit as st
import mysql.connector
from langchain.llms import Ollama
from langchain.agents import AgentType, initialize_agent, Tool
from DatabaseTables import openmrs_tables

# Convert table names to a human-readable text description
def format_table_names(table_names):
    return "The database contains the following tables:\n- " + "\n- ".join(table_names)


# Format the table names into plain text
table_names_description = format_table_names(openmrs_tables)


# Database connection (used for running SQL queries)
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="JesusChrist",  # Replace with your MySQL password
            database="openmrs-ai"  # Replace with your MySQL database
        )
    except mysql.connector.Error as err:
        st.error(f"MySQL Connection Error: {err}")
        return None


# Execute SQL queries safely
def execute_query(query: str):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
        except Exception as e:
            st.error(f"Database Query Error: {e}")
            return []
    else:
        return []


# Initialize Ollama LLM
llm = Ollama(model="qwen2.5-coder:1.5b")  # Use an appropriate coder or reasoning model

# Define the Tool with table names
tools = [
    Tool(
        name="SQL Executor",
        func=execute_query,
        description=f"Use this tool to query the database. "
                    f"Here are the available table names:\n\n{table_names_description}\n\n"
                    f"Write SQL statements using these table names."
    )
]

# Initialize the Agent with the Tool
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# Streamlit Application Interface
st.title("OpenMRS AI Text-to-SQL Engine")
prompt = st.text_input("Enter your query in plain English (e.g., 'Get all orders for user ID 5'):", "")

if prompt:
    try:
        response = agent.run(prompt)
        if isinstance(response, list):  # If valid results are returned
            st.write("### Query Results")
            st.dataframe(response)
        else:
            st.error(f"Unexpected response: {response}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
