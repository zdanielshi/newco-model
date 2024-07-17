import streamlit as st
import pandas as pd
import numpy as np
from utils.active_rates import active_rate_scenarios

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
st.write("Explainer text here")

# Set up columns
col1, col2 = st.columns([1,3])

with col1:
    # Total addressable population
    total_adressable_population = st.number_input(
        "Total Addressable Customers", 
        value = 1000000, 
        min_value= 0,
        step = 1,
        format = "%d",
        help = "What is the total number of customers in the market"
        )
    
    # Stable penetration
    stable_penetration_perc = st.number_input(
        "Stable Penetration Percent",
        value = 10.0,
        min_value = 0.0,
        max_value = 100.0,
        step = 1.0,
        format = "%.2f",
        help = "At stable, what is the maximum market share NewCo will have?"
        ) / 100
    
    # The starting number of customers
    starting_customers = st.number_input(
        "Starting Number of Customers",
        value = 100,
        min_value = 1,
        step = 1,
        format = "%d",
        help = "How many customers do you start with?"
        )
    
    # Midpoint year
    midpoint_year = st.number_input(
        "Midpoint year",
        value = 3,
        min_value = 1,
        max_value = 10,
        step = 1,
        format = "%d",
        help = "Logistic functions require a 'midpoint' for when growth slows down. Assume some year where growth slows."
    )

    # Initial growth rate
    initial_growth_rate = st.number_input(
        "Initial growth rate percent",
        value = 200.0,
        min_value = 0.0,
        step = 1.0,
        format = "%.2f",
        help = "What is the growth rate in the initial period?"
    ) / 100
    # Converting the initial growth rate into an intrinsic growth rate for the logistic function
    intrinsic_growth_rate = np.log(1 + initial_growth_rate)

    min_growth_rate = st.number_input(
        "Minimum growth rate percent",
        value = 3.0,
        min_value = 0.0,
        step = 1.0,
        format = "%.2f",
        help = "What is the minimum growth rate for the company? For example: 3% to match population growth in the US."
    )

    active_rate_scenario = st.selectbox(
        "Active rate scenario",
        (list(active_rate_scenarios.keys())),
        index = None,
        help = "Pick an active rate rate scenario. This is the active rate of acquired customers in different periods"
    )

