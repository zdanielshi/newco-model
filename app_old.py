import streamlit as st
import pandas as pd
import numpy as np
from utils.model_functions import calculate_customers, calculate_active_customers
from utils.active_rates import active_rate_scenarios
from utils.text_content import sidebar

# Universal settings
st.set_page_config(
    page_title = "Simple NewCo Model",
    page_icon = "🧮",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

# Sidebar
with st.sidebar:
    st.write(sidebar)

# Title of the app
st.title("Simple NewCo Model")
st.write("Explainer text here")

# Set up columns
col1, col2, col3 = st.columns([1,1, 2])

with col1:
    with st.expander("**_Customer Model Assumptions_**",expanded=True, icon = "👥"):
        # Customer Model Assumptions
        ## Years of model
        years = np.arange(1,11,1)

        ## Total addressable population
        total_adressable_population = st.number_input(
            "Total Addressable Customers (#)", 
            value = 1000000, 
            min_value= 0,
            step = 1,
            format = "%d",
            help = "What is the total number of customers in the market"
            )
        
        ## The starting number of customers
        starting_customers = st.number_input(
            "Starting Number of Customers (#)",
            value = 100,
            min_value = 1,
            step = 1,
            format = "%d",
            help = "How many customers do you start with?"
            )
        
        ## Starting customers active rate
        starting_customer_active_rate = st.number_input(
            "Starting Customers Active Rate (%)",
            value = 50.0,
            min_value = 0.0,
            max_value = 100.0,
            step = 1.0,
            format = "%.2f",
            help = "How active are the initial set of customers acquired?"
        )
        
        ## Stable penetration
        stable_penetration_perc = st.number_input(
            "Stable Penetration (%)",
            value = 10.0,
            min_value = 0.0,
            max_value = 100.0,
            step = 1.0,
            format = "%.2f",
            help = "At stable, what is the maximum market share NewCo will have?"
            ) / 100
        
        ## Midpoint year
        midpoint_year = st.number_input(
            "Midpoint Year",
            value = 3,
            min_value = 1,
            max_value = 10,
            step = 1,
            format = "%d",
            help = "Logistic functions require a 'midpoint' for when growth slows down. Assume some year where growth slows."
        )

        ## Initial growth rate
        initial_growth_rate = st.number_input(
            "Initial growth rate (%)",
            value = 200.0,
            min_value = 0.0,
            step = 1.0,
            format = "%.2f",
            help = "What is the growth rate in the initial period?"
        ) / 100
        ### Converting the initial growth rate into an intrinsic growth rate for the logistic function
        intrinsic_growth_rate = np.log(1 + initial_growth_rate)

        min_growth_rate = st.number_input(
            "Minimum growth rate (%))",
            value = 3.0,
            min_value = 0.0,
            step = 1.0,
            format = "%.2f",
            help = "What is the minimum growth rate for the company? For example: 3% to match population growth in the US."
        )

        ## Active rate scenarios
        active_rate_scenario = st.selectbox(
            "Active rate scenario",
            (list(active_rate_scenarios.keys())),
            index = None,
            help = "Pick an active rate rate scenario. This is the active rate of acquired customers in different periods"
        )

with col2:
    with st.expander("_**P&L Model Assumptions**_", expanded=True, icon="💵"):
        # Monthly ARPU
        arpu = st.number_input(
            "Montly Avg Revenue per Active User ($)",
            value = 25.0,
            min_value = 0.0,
            step = 1.0,
            format = "%.2f",
            help = "The average revenue from an active customer per month. For ex. A SaaS company with a $15 subscription, the ARPU would be $15."
        ) * 12 # Multiply by 12 to annualize the monthly ARPU

        # Gross Margin
        gross_margin = st.number_input(
            "Gross Margin (%)",
            value = 50.0,
            min_value = 0.0,
            max_value = 100.0,
            format = "%.2f",
            help = "How much gross profit (divided by revenue) are you making on selling each individual unit of product?"
        ) / 100

        # Customer Acquisition Cost
        cac = st.number_input(
            "Customer Acquisition Cost ($)",
            value = 100.0,
            min_value = 0.0,
            format = "%.2f",
            help = "How much does it cost to acquire every new customer?"
        )
        
        # Per headcount cost
        support_cost_per_active = st.number_input(
            "Support Cost Per Active ($)",
            value = 5.0,
            min_value = 0.0,
            format = "%.2f",
            help = "How much will it take to support each active customer? For ex. You have $150,000 in support cost, and 15,000 active customers. Then your support cost per active is $10."
        )

        # Per headcount cost
        per_hc_cost = st.number_input(
            "Per Headcount Cost ($)",
            value = 150000,
            min_value = 0,
            format = "%d",
            help = "How much is the fully loaded cash cost per employee? Try to include the value of all cash costs medical insurance, payroll taxes, etc."
        )

        # Headcount inflation cost
        hc_inflation_rate = st.number_input(
            "Headcount Inflation Rate (%)",
            value = 3.0,
            min_value = 0.0,
            format = "%.2f",
            help = "Headcount inflation can really catch up with over time. Make sure to include a factor for inflation and raises you need to give employees."
        )

        # Other fixed cost ratio
        other_fixed_cost_ratio = st.number_input(
            "Other Fixed Cost Ratio (%)",
            value = 5.0,
            min_value = 0.0,
            format = "%.2f",
            help = "Assume some ratio of other fixed costs, relative to your headcount cost. This can include things like software licenses, office rent, etc."
        )

        # Headcount per year
        hc_df = pd.DataFrame(
            [
                {"Year": 1, "Headcount": 5},
                {"Year": 2, "Headcount": 10},
                {"Year": 3, "Headcount": 15},
                {"Year": 4, "Headcount": 20},
                {"Year": 5, "Headcount": 20},
                {"Year": 6, "Headcount": 20},
                {"Year": 7, "Headcount": 20},
                {"Year": 8, "Headcount": 20},
                {"Year": 9, "Headcount": 20},
                {"Year": 10, "Headcount": 20}
            ]
        )

        "Headcount per Year"
        edited_hc_df = st.data_editor(
            hc_df, 
            hide_index=True, 
            use_container_width=True,
            disabled = ["Year"],
            column_config={
                "Year": st.column_config.Column(
                ),
                "Headcount": st.column_config.NumberColumn(
                    min_value = 1,
                    format = "%d",
                    help = "help"
                )
            }
        )

# Customer Model Calculations
customers_df = []
customers_df_with_actives = []

customers_df = calculate_customers(total_adressable_population, stable_penetration_perc, starting_customers, midpoint_year, intrinsic_growth_rate, min_growth_rate, years)
customers_df_with_actives = calculate_active_customers(customers_df,active_rate_scenario, starting_customers, starting_customer_active_rate)

# P&L Model Calculations

with col3:
    calculate = st.button("Calculate")
    if calculate:
        with st.container(border=True):
            "_**Customer Model**_"
            st.dataframe(customers_df_with_actives, hide_index=True, height = 425)
    
