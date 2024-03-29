import streamlit as st
from pymongo import MongoClient
from bson import json_util

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['streamlit']
collection = db['user']

# Streamlit Login and Registration Page
page = st.sidebar.radio("Navigation", ['Login', 'Register'])

if page == 'Login':
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Query MongoDB for user
        user = collection.find_one({"username": username})

        if user:
            if user["password"] == password:
                st.success("Logged in as {}".format(username))
                page = 'chat'
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")

    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Create Account"):
        page = 'Register'

elif page == 'Register':
    st.title("Registration Page")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    conf_password = st.text_input("Confirm Password", type='password')

    if st.button("Register"):
        # Check if username already exists
        existing_user = collection.find_one({"username": new_username})
        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        elif new_password != conf_password:
            st.error("Password doesn't match")
        else:
            
            # Insert new user into MongoDB
            new_user = {"username": new_username, "password": new_password}
            collection.insert_one(new_user)
            st.success("Account created successfully!")

    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Login if you have account"):
        page = 'Login'

elif page == "chat" :
    st.header('Chat app')
    st.subheader("Welcome to chatapp")