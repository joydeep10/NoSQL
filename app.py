from dotenv import load_dotenv

load_dotenv()  # to load all the env variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load LLM and extract SQL queries as response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt, question])
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"


# Function to retrieve query from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        return f"Database error: {e}"


# Define a prompt to feed the LLM
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has a table named STUDENT with the following columns: NAME, CLASS, SECTION, MARKS.

For example:
1. How many entries of records are present?
   SQL: SELECT COUNT(*) FROM STUDENT;

2. Tell me all the students studying in Data Science class.
   SQL: SELECT * FROM STUDENT WHERE CLASS='Data Science';
   
3. List the students who scored more than 85.
   SQL: SELECT NAME, MARKS FROM STUDENT WHERE MARKS > 85;

4. What is the average mark of students in Data Science class?
   SQL: SELECT AVG(MARKS) FROM STUDENT WHERE CLASS='Data Science';

5. How many students are there in each class?
   SQL: SELECT CLASS, COUNT(*) FROM STUDENT GROUP BY CLASS;

Please provide the SQL query without the ``` syntax or the word "sql".
"""

# Streamlit UI
st.set_page_config(page_title="NoSql", layout="centered")
st.title("NoSQL - Natural Language to SQL")

st.subheader("Ask a question in English and get the SQL query and results!")

question = st.text_input("Enter your question here:")

if st.button("Submit"):
    if question:
        with st.spinner("Generating SQL query..."):
            sql_query = get_gemini_response(question, prompt)

        if "Error" in sql_query:
            st.error(sql_query)
        else:
            st.write(f"Generated SQL Query: `{sql_query}`")

            with st.spinner("Executing SQL query..."):
                results = read_sql_query(sql_query, "student.db")

            if "Error" in results:
                st.error(results)
            else:
                if results:
                    st.subheader("Query Results:")
                    for row in results:
                        st.write(row)
                else:
                    st.info("No results found for the given query.")
    else:
        st.warning("Please enter a question.")
