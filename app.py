import streamlit as st
import pandas as pd
import numpy as np
from utils.model_functions import logistic_function, calculate_actives
from utils.active_rates import active_rate_scenarios
from utils.text_content import sidebar, help_texts, explainer, customer_model_explainer, pl_model_explainer

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
st.markdown(explainer)

with st.container(border = True):
    "_**Customer Model Assumptions**_"
    st.markdown(customer_model_explainer)
    default_cap_pop = 100000
    default_init_pop = 5
    default_growth_rate = 0.1
    default_min_growth = 3.0
    default_years = 10
    default_midpoint = 6
    default_ar_scen = '50% asymptote'
    default_init_pop_scen = 50.0

    customer_assumptions = pd.DataFrame(columns = ['Addressable Customers', 'Starting Customers', 'Intrinsic Growth Rate', 'Minimum Growth Rate', 'Years', 'Midpoint', 'Active Rate Scenario', 'Starting Customers Active Rate'])
    customer_assumptions.loc[0] = [default_cap_pop, default_init_pop, default_growth_rate, default_min_growth, default_years, default_midpoint, default_ar_scen, default_init_pop_scen]
    default_customer_assumptions = st.data_editor(
        customer_assumptions, 
        use_container_width=True, 
        hide_index=True,
        column_config = {
            'Addressable Customers': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 0,
                step = 1,
                format = "%d customers"
            ),
            'Starting Customers': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 0,
                step = 1,
                format = "%d customers"
            ),
            'Intrinsic Growth Rate': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 0.0,
                format = '%.2f'
            ),
            'Minimum Growth Rate': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 0.0,
                step = 1.0,
                format = "%.2f%%"
            ),
            'Years': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 5,
                max_value = 10,
                step = 1,
                format = '%d years'
            ),
            'Midpoint': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 1,
                step = 1,
                format = '%d years'
            ),
            'Active Rate Scenario': st.column_config.SelectboxColumn(
                help = "Enter Later",
                options = list(active_rate_scenarios.keys())
            ), 
            'Starting Customers Active Rate': st.column_config.NumberColumn(
                help = "Enter Later",
                min_value = 0.0,
                step = 1.0,
                format = "%.2f%%"
            )
        }
    )

    # Modifying the assumptions to be used in the customer model
    model_cap_pop = default_customer_assumptions['Addressable Customers'].iloc[0]
    model_init_pop = default_customer_assumptions['Starting Customers'].iloc[0]
    model_growth = default_customer_assumptions['Intrinsic Growth Rate'].iloc[0]
    model_min_growth = (1 + (default_customer_assumptions['Minimum Growth Rate'].iloc[0] / 100)) ** (1/12) - 1
    model_months = default_customer_assumptions['Years'].iloc[0] * 12 # Modify to convert to a monthly calculation
    model_midpoint = default_customer_assumptions['Midpoint'].iloc[0] * 12 # Modify to convert to a monthly calculation
    model_ar_scen = default_customer_assumptions['Active Rate Scenario'].iloc[0]
    model_init_pop_ar = default_customer_assumptions['Starting Customers Active Rate'].iloc[0] / 100
    months_list = np.arange(1, model_months + 1)

    # Initialize the customer model dataframe with months and years
    customers = pd.DataFrame({'Months': months_list})
    customers['Year'] = ((customers['Months'] - 1) // 12) + 1

    # Apply the logistic function to calculate cumulative customers
    customers['Cume Customers'] = round(logistic_function(model_growth, model_init_pop, model_cap_pop, customers['Months'], model_midpoint))
    # Apply a minimum growth rate, to account for residual growth of customers
    for i in range(1, len(customers)):
        prev_period_cume = customers.loc[i-1, 'Cume Customers']
        min_cume = prev_period_cume * (1+model_min_growth)
        customers.loc[i, 'Cume Customers'] = max(customers.loc[i, 'Cume Customers'], round(min_cume))
    # Calculate New Customers
    customers['New Customers'] = customers['Cume Customers'].diff().fillna(0)
    # Set the 'New Customers' for the first year
    customers.loc[0, 'New Customers'] = customers.loc[0, 'Cume Customers'] - model_init_pop
    # Ensure 'New Customers' for the first year is not negative
    customers.loc[0, 'New Customers'] = max(0, customers.loc[0, 'New Customers'])

    # Calculate Active Customers
    customers["Active Customers"] = round(calculate_actives(customers, active_rate_scenarios, model_ar_scen, model_init_pop, model_init_pop_ar))

    transposed_customers = customers.T

with st.container(border=True):
    "_**P&L Model Assumptions**_"
    st.markdown(pl_model_explainer)
    default_arpu = 100
    default_gross_margin = 75
    default_cac = 100
    default_support_cost = 5
    default_per_hc_cost = 175000
    default_hc_cost_inflation_pa = 3
    default_other_fixed_exp_ratio = 5

    pl_assumptions = pd.DataFrame(columns = ['Monthly ARPU', 'Gross Margin', 'CAC', 'Support Cost / Active', 'Per Headcount Cost', 'HC Inflation Rate', 'Other Fixed Expense Ratio'])
    pl_assumptions.loc[0] = [default_arpu, default_gross_margin, default_cac, default_support_cost, default_per_hc_cost, default_hc_cost_inflation_pa, default_other_fixed_exp_ratio]

    #Laying out the headcount assumptions
    # Define the hc_assumptions DataFrame and transpose it
    hc_assumptions = pd.DataFrame({
        'Year 1': [5],
        'Year 2': [10],
        'Year 3': [15],
        'Year 4': [15],
        'Year 5': [15],
        'Year 6': [15],
        'Year 7': [15],
        'Year 8': [15],
        'Year 9': [15],
        'Year 10': [15]
    }).T
    hc_assumptions.columns = ['Headcount']

    # Display the transposed DataFrame using Streamlit's data editor
    default_pl_assumptions = st.data_editor(
        pl_assumptions,
        hide_index=True,
        use_container_width=True
    )
    default_hc_assumptions = st.data_editor(
        hc_assumptions.T,
        hide_index=False,
        use_container_width=True
    )

    #Modifying the assumptions to the be used in the P&L model
    model_arpu = default_pl_assumptions['Monthly ARPU'].iloc[0]
    model_gross_margin = default_pl_assumptions['Gross Margin'].iloc[0] / 100
    model_cac = default_pl_assumptions['CAC'].iloc[0]
    model_support_cost = default_pl_assumptions['Support Cost / Active'].iloc[0]
    model_per_hc_cost = default_pl_assumptions['Per Headcount Cost'].iloc[0]
    model_hc_cost_inflation_pa = default_pl_assumptions['HC Inflation Rate'].iloc[0] / 100
    model_other_fixed_exp_ratio = default_pl_assumptions['Other Fixed Expense Ratio'].iloc[0] / 100

    pl_model = customers[['Months', 'Year', 'Cume Customers', 'New Customers', 'Active Customers']].copy()
    pl_model['Revenue'] = pl_model['Active Customers'] * model_arpu
    pl_model['COGS'] = pl_model['Revenue'] * (1 - model_gross_margin)
    pl_model['Gross Profit'] = pl_model['Revenue'] - pl_model['COGS']
    pl_model['Marketing Expense'] = pl_model['New Customers'] * model_cac
    pl_model['Support Expense'] = pl_model['Active Customers'] * model_support_cost
    pl_model['Fixed OPEX'] = pl_model['Marketing Expense'] + pl_model['Support Expense']
    pl_model['Contribution Profit'] = pl_model['Gross Profit'] - pl_model['Fixed OPEX']
    pl_model['GP per Active'] = pl_model['Gross Profit'] / pl_model['Active Customers']

    #Calculating Payback
    pl_model['Cumulative Gross Profit per Customer'] = pl_model['GP per Active'].cumsum()
    payback_period = pl_model[pl_model['Cumulative Gross Profit per Customer'] >= model_cac]['Months'].min()

    pl_model_annual = pl_model.groupby('Year').agg({
        'New Customers': 'sum',
        'Active Customers': 'last',
        'Revenue': 'sum',
        'COGS': 'sum',
        'Gross Profit': 'sum',
        'Marketing Expense': 'sum',
        'Support Expense': 'sum',
        'Fixed OPEX': 'sum',
        'Contribution Profit': 'sum'
    })

    pl_model_annual['Headcount'] = default_hc_assumptions.T['Headcount'].values
    pl_model_annual['Headcount Expense'] = pl_model_annual['Headcount'] * (model_per_hc_cost * ((1 + model_hc_cost_inflation_pa)**pl_model_annual.index))
    pl_model_annual['Other Fixed Expense'] = pl_model_annual['Headcount'] * model_other_fixed_exp_ratio
    pl_model_annual['Operating Profit'] = pl_model_annual['Contribution Profit'] - pl_model_annual['Headcount Expense'] - pl_model_annual['Other Fixed Expense']
    pl_model_annual['Revenue Growth Rate'] = pl_model_annual['Revenue'].pct_change()
    pl_model_annual['Operating Margin'] = pl_model_annual['Operating Profit'] / pl_model_annual['Revenue']  

# Divider between assumptions and output

st.divider()

# Display the DataFrame using Streamlit's dataframe
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("## P&L Model")
    st.dataframe(pl_model_annual.T, use_container_width=True, on_select='ignore', height = 800)

with col2:
    st.metric(label = "Payback", value = f"{payback_period} Months")
    with st.container(border = True):
        st.markdown('#### Revenue and Operating Profit')
        st.line_chart(pl_model_annual[['Revenue', 'Operating Profit']])
        st.markdown('#### Customers')
        st.line_chart(pl_model_annual[['New Customers', 'Active Customers']])

# st.metric(label = "Payback",value = f'{payback_period} months')
# st.write(pl_model_annual.T)

# st.write(transposed_customers.head())
# st.write(transposed_customers.tail())

# st.line_chart(data = customers[['Cume Customers', 'New Customers', 'Active Customers']])