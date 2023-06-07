import os
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd

# Load environment variables
load_dotenv()

# Define API endpoint
API_ENDPOINT = os.getenv("API_ENDPOINT")  # get the API endpoint from .env file

def display_users():
    response = requests.get(f'{API_ENDPOINT}/users')
    if response.status_code == 200:
        users = response.json()

        # Create a pandas dataframe from the user data
        df = pd.DataFrame(users)

        # Create a list to hold the delete buttons
        delete_buttons = []

        # Add a search bar
        search_query = st.text_input('Search', value='')

        # Filter the dataframe based on the search query
        if search_query:
            df = df[df['username'].str.contains(search_query, case=False)]

        for index, user in enumerate(df.to_dict('records')):
            delete_button = st.button(f'Delete User {user["id"]}', key=f'delete_{index}')
            delete_buttons.append(delete_button)

            if delete_button:
                response = requests.delete(f'{API_ENDPOINT}/users/{user["id"]}')
                if response.status_code == 200:
                    st.success("User deleted successfully!")
                else:
                    st.error("Failed to delete user!")

        # Display the dataframe as a table in Streamlit
        st.table(df)

        # Add a refresh button
        if st.button('Refresh'):
            display_users()

def main():
    st.title("User Management Dashboard")
    st.subheader("List of Users")
    display_users()

if __name__ == "__main__":
    main()
