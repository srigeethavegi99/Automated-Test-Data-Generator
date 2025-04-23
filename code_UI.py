import streamlit as st
import os
import uuid
from datetime import datetime

# Streamlit app layout
st.title("Automated Test Data Generator")

st.write("Fill out the form below to generate Test Data:")

# Function to add a new row to the table
def add_new_row():
    if "rows" not in st.session_state:
        st.session_state["rows"] = [{"Column Header": "", "Value Constraint": "", "Column Relation": ""}]
    else:
        st.session_state["rows"].append({"Column Header": "", "Value Constraint": "", "Column Relation": ""})

# Initialize rows in session state if not already initialized
if "rows" not in st.session_state:
    st.session_state["rows"] = [{"Column Header": "", "Value Constraint": "", "Column Relation": ""}]

# Add a new row button (outside the form)
if st.button("Add New Row"):
    add_new_row()

# User input form
with st.form(key='faker_form'):
    st.write("Column Definitions:")

    # Display the current rows
    for idx, row in enumerate(st.session_state["rows"]):
        col1, col2, col3 = st.columns(3)
        row["Column Header"] = col1.text_input(f"Column Header {idx + 1}", row["Column Header"], key=f"header_{idx}")
        row["Value Constraint"] = col2.text_input(f"Value Constraint {idx + 1}", row["Value Constraint"],
                                                  key=f"constraint_{idx}")
        row["Column Relation"] = col3.text_input(f"Column Relation {idx + 1}", row["Column Relation"],
                                                 key=f"relation_{idx}")

    lan_id = st.text_input("LAN ID", "")
    num_records = st.number_input("Number of Records", min_value=1, max_value=10000000, value=10)
    additional_instructions = st.text_area("Additional Instructions", "")

    submit_button = st.form_submit_button(label='Generate Script')

# Placeholder for future functionality
if submit_button:
    st.success("Script generation functionality is not yet implemented. Please check back later.")
