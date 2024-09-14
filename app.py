import os
import gradio as gr
import pandas as pd
from sqlalchemy import create_engine, text
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# Set up your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# Connect to the SQLite database
db_path = 'olympics.db'
engine = create_engine(f'sqlite:///{db_path}')
db = SQLDatabase(engine)

# Initialize OpenAI language model
llm = OpenAI(temperature=0)

# Create an SQLDatabaseChain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

def get_schema():
    with engine.connect() as conn:
        tables = engine.table_names()
        schema = []
        for table in tables:
            columns = [col['name'] for col in conn.execute(text(f"PRAGMA table_info('{table}')")).fetchall()]
            schema.append(f"Table: {table}")
            schema.append("Columns: " + ", ".join(columns))
        return "\n".join(schema)

def answer_query(query):
    schema = get_schema()
    full_query = f"""
    Given the following SQL schema:
    {schema}

    Human: {query}
    AI: To answer this question, I'll need to query the database. Let me write an SQL query to get the information we need.

    """
    try:
        result = db_chain.run(full_query)
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=answer_query,
    inputs=gr.Textbox(lines=2, placeholder="Ask a question about the Olympics data..."),
    outputs="text",
    title="LLM-powered Olympics Data Chatbot",
    description="Ask questions about medal counts, top performing countries, etc. using natural language.",
    examples=[
        ["Which country won the most gold medals?"],
        ["What are the top 5 countries by total medal count?"],
        ["How many silver medals did Japan win?"],
        ["Compare the performance of United States and China in terms of medal count."],
        ["Which country has the most balanced medal distribution among gold, silver, and bronze?"]
    ]
)

# Launch the interface
iface.launch()