import streamlit as st
from sqlalchemy import create_engine

# Streamlit UI Components
st.title("Database Interaction Agent")
st.subheader("Interact with the MySQL Database and Agent")

# Input fields for MySQL Connection Details
st.sidebar.header("Database Configuration")
mysql_host = st.sidebar.text_input("MySQL Host", "localhost")
mysql_user = st.sidebar.text_input("MySQL User", "root")
mysql_password = st.sidebar.text_input("MySQL Password", type="password")
mysql_db = st.sidebar.text_input("Database Name", "test_db")
mysql_port = st.sidebar.number_input("Port", 3306, format="%d")

# Establishing connection using the sql_engine function
if st.sidebar.button("Connect to Database"):
    try:
        engine = create_engine(
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
        )
        connection_test = engine.connect()
        st.sidebar.success("Connected to the Database successfully!")
        connection_test.close()
    except Exception as e:
        st.sidebar.error(f"Error connecting to the Database: {str(e)}")

# Display available features
st.header("Features")
feature_selection = st.radio(
    "Select Action",
    ["View Tables", "Query Data", "Describe Table", "Use Agent"],
    index=0,
)

# Functionality for "View Tables"
if feature_selection == "View Tables":
    try:
        inspector = engine.inspect()
        tables = inspector.get_table_names()
        st.write("Available Tables:")
        st.write(tables)
    except Exception as e:
        st.error(f"Error fetching tables: {str(e)}")

# Functionality for "Query Data"
if feature_selection == "Query Data":
    query = st.text_area("Enter SQL Query")
    if st.button("Execute Query"):
        try:
            with engine.connect() as connection:
                result = connection.execute(query)
                st.write("Query Result:")
                if result.returns_rows:
                    st.write(result.fetchall())
                else:
                    st.write("Query executed successfully.")
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

# Functionality for "Describe Table"
if feature_selection == "Describe Table":
    table_name = st.text_input("Enter Table Name")
    if st.button("Describe Table"):
        try:
            inspector = engine.inspect()
            columns_info = inspector.get_columns(table_name)
            st.write(f"Columns in {table_name}:")
            for col in columns_info:
                st.write(f"{col['name']} ({col['type']}) - {col['comment'] or 'No description'}")
        except Exception as e:
            st.error(f"Error describing table: {str(e)}")

# Functionality for "Use Agent"
if feature_selection == "Use Agent":
    agent_action = st.text_area("Enter Agent Action or Command")
    if st.button("Send to Agent"):
        try:
            # Placeholder for agent interaction
            # e.g., result = agent(agent_action)
            result = f"Simulated agent response for action: {agent_action}"
            st.write("Agent Response:")
            st.write(result)
        except Exception as e:
            st.error(f"Error interacting with agent: {str(e)}")
