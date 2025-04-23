import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import re
import datetime
import pyrebase

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

st.set_page_config(page_title="AI Test Data Generator", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "rows" not in st.session_state:
    st.session_state["rows"] = [{"Column Header": "", "Value Constraint": "", "Column Relation": ""}]
if "generated_script" not in st.session_state:
    st.session_state['generated_script'] = ""
if "prompt" not in st.session_state:
    st.session_state['prompt'] = ""
def parse_firebase_error(e):
    # Print error details for debugging
    print(f"Exception arguments: {e.args}")
    
    error_str = e.args[1] if len(e.args) > 1 else e.args[0] if len(e.args) > 0 else ""
    
    if 'EMAIL_EXISTS' in error_str:
        return "The email address is already in use by another account."
    elif 'INVALID_EMAIL' in error_str:
        return "The email address is badly formatted."
    elif 'WEAK_PASSWORD' in error_str:
        return "The password is too weak. It must be at least 8 characters long, include at least one uppercase letter and one special character."
    elif 'EMAIL_NOT_FOUND' in error_str:
        return "The email address is not found. Please register first."
    elif 'INVALID_PASSWORD' in error_str:
        return "The password is invalid. Please try again."
    else:
        return f"An unknown error occurred: {error_str}"



def signup():
    st.subheader("Create a New Account")
    new_email = st.text_input("Email", key="signup_email")
    new_password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    signup_button = st.button("Sign Up")

    if signup_button:
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[A-Z])(?=.*\W).{8,}$'
        
        if not re.match(email_pattern, new_email):
            st.error("Invalid email format.")
        elif not re.match(password_pattern, new_password):
            st.error("Password must be at least 8 characters long, include at least one uppercase letter and one special character.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                user = auth.create_user_with_email_and_password(new_email, new_password)
                st.success("Account created successfully! Please log in.")
                st.info("Switch to the Login option below.")
            except Exception as e:
                error_message = parse_firebase_error(e)
                st.error(f"Error creating account: {error_message}")

def login():
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    if login_button:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Logged in successfully!")
            st.rerun()

        except Exception as e:
            error_message = parse_firebase_error(e)
            st.error(f"Error logging in: {error_message}")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.success("Logged out successfully!")
    st.rerun()


def authentication():
    auth_option = st.selectbox("Select Option", ["Login", "Sign Up"])

    if auth_option == "Login":
        login()
        st.markdown("Don't have an account? **Sign Up** below.")
    else:
        signup()
        st.markdown("Already have an account? **Login** below.")

def get_response_from_gemini(prompt, model_name):
    model = genai.GenerativeModel(model_name, safety_settings=safety_settings)
    response = model.generate_content(prompt)
    return response.text

def extract_python_code(text):
    pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()

def add_new_row():
    st.session_state["rows"].append({"Column Header": "", "Value Constraint": "", "Column Relation": ""})

def main_app():
    st.title("AI Test Data Generator")
    add_row = st.button("Add New Row")
    if add_row:
        add_new_row()

    with st.form(key='faker_form'):
        st.subheader("Column Definitions:")

        for idx, row in enumerate(st.session_state["rows"]):
            col1, col2, col3 = st.columns(3)
            row["Column Header"] = col1.text_input(f"Column Header {idx + 1}", row["Column Header"], key=f"header_{idx}")
            row["Value Constraint"] = col2.text_input(f"Value Constraint {idx + 1}", row["Value Constraint"], key=f"constraint_{idx}")
            row["Column Relation"] = col3.text_area(f"Column Relation {idx + 1}", row["Column Relation"], key=f"relation_{idx}")

        num_records = st.number_input("Number of Records", min_value=1, max_value=10000000, value=10)
        additional_instructions = st.text_area("Additional Instructions", "")
        data_type = st.selectbox("Select Data Type to Generate:", ["Positive Data (Valid)", "Negative Data (Invalid)"])
        submit_button = st.form_submit_button(label='Generate Script')

    if submit_button:
        if any(not row["Column Header"] for row in st.session_state["rows"]):
            st.error("Please provide a Column Header for all columns.")
            st.stop()

        column_headers = [row["Column Header"] for row in st.session_state["rows"]]
        value_constraints = [row["Value Constraint"] for row in st.session_state["rows"]]
        column_relations = [row["Column Relation"] for row in st.session_state["rows"]]

        if "Negative" in data_type:
            data_instruction = "Generate data that intentionally violates the following constraints."
        else:
            data_instruction = "Generate data that complies with the following constraints."

        prompt = f"""
You are to generate a Python script using the Faker library that generates synthetic data.

{data_instruction}

The data should have the following specifications:

Column Definitions:
"""
        for idx, row in enumerate(st.session_state["rows"]):
            prompt += f"""
- Column {idx + 1}:
    Header: {row['Column Header']}
    Value Constraint: {row['Value Constraint']}
    Relationship: {row['Column Relation']}
"""
        prompt += f"""
Number of Records: {num_records}

Additional Instructions:
{additional_instructions}

Requirements:
- Ensure that value constraints and relationships are respected.
- Use appropriate Faker providers for data generation.
- The script should be executable and well-commented.

Provide the script enclosed in triple backticks, and specify the language after the first three backticks like this: ```python
"""

        try:
            script_response = get_response_from_gemini(prompt, "gemini-1.5-pro")
            generated_script = extract_python_code(script_response)
            st.session_state['generated_script'] = generated_script
            st.session_state['prompt'] = prompt
        except Exception as e:
            st.error(f"An error occurred while generating the script: {e}")
            st.stop()

    if st.session_state['generated_script']:
        st.subheader("Generated Python Script")
        st.code(st.session_state['generated_script'], language='python')
        st.download_button("Download Script", st.session_state['generated_script'], file_name="generated_script.py")
        feedback = st.slider("Rate the quality of the generated data (1 = Poor, 5 = Excellent):", 1, 5, 3, key='feedback_slider')
        feedback_submit = st.button("Submit Feedback", key='feedback_submit')

        if feedback_submit:
            feedback_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "prompt": st.session_state['prompt'],
                "feedback": feedback
            }

            feedback_file = 'feedback_log.json'
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(feedback_data)

            with open(feedback_file, 'w') as f:
                json.dump(data, f, indent=4)

            st.success("Thank you for your feedback!")

    st.header("We Value Your Feedback!")
    automation_feedback = st.text_area("Would you be interested in automated solutions? Please share your thoughts or specific areas where automation could help you.")

    if st.button("Submit Feedback", key='automation_feedback_submit'):
        feedback_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "automation_feedback": automation_feedback
        }

        automation_feedback_file = 'automation_feedback_log.json'
        if os.path.exists(automation_feedback_file):
            with open(automation_feedback_file, 'r') as f:
                data = json.load(f)
        else:
            data = []

        data.append(feedback_data)

        with open(automation_feedback_file, 'w') as f:
            json.dump(data, f, indent=4)

        st.success("Thank you for your feedback!")

    show_logs = st.checkbox("Show Feedback Logs")
    if show_logs:
        st.subheader("Generated Data Feedback")
        feedback_file = 'feedback_log.json'
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
            st.json(feedback_data)
        else:
            st.write("No feedback submitted yet.")

        st.subheader("Automation Feedback")
        automation_feedback_file = 'automation_feedback_log.json'
        if os.path.exists(automation_feedback_file):
            with open(automation_feedback_file, 'r') as f:
                automation_data = json.load(f)
            st.json(automation_data)
        else:
            st.write("No automation feedback submitted yet.")

    if st.sidebar.button("Clear All"):
        st.session_state["rows"] = [{"Column Header": "", "Value Constraint": "", "Column Relation": ""}]
        st.session_state['generated_script'] = ""
        st.session_state['prompt'] = ""
        st.success("App data cleared successfully!")

def main():
    if st.session_state.logged_in:
        main_app()
        if st.sidebar.button("Logout"):
            logout()
    else:
        st.sidebar.title("Welcome")
        authentication()

if __name__ == "__main__":
    main()
