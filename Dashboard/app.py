import os
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd
import os

def display_user_form():
    with st.form(key='user_form'):
        st.write('Add a new user:')
        username = st.text_input('Username')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')

        submit_button = st.form_submit_button('Add User')
        if submit_button:
            if username and email and password:
                response = requests.post(f'https://flask-backend-prod.up.railway.app/register', json={
                    'username': username,
                    'email': email,
                    'password': password
                })
                if response.status_code == 201:
                    st.success("User added successfully!")
                else:
                    st.error("Failed to add user!")
            else:
                st.error("Please fill out all fields.")

def main():
    st.title("User Management Dashboard")
    display_user_form()

if __name__ == "__main__":
    main()
