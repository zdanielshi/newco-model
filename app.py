import streamlit as st
import pandas as pd

# Universal settings
st.set_page_config(
    page_title = "Simple NewCo Model",
    page_icon = "🧮",
    layout = "wide",
    initial_sidebar_state = "expanded"
)
# Sidebar
with st.sidebar:
    st.write("Enter Text Here")

# Title of the app
st.title("Simple NewCo Model")

total_adressable_population = st.number_input(
    "Total Addressable Customers", 
    value = 1000, 
    min_value=0,
    step = 1,
    format = "%d"
    )

starting_penetration = st.number_input(
    "Starting Number of Customers",
    value = 1,
    min_value = 1,
    step = 1,
    format = "%d"
    )

