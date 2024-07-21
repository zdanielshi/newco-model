import pandas as pd
import numpy as np
from utils.active_rates import active_rate_scenarios

# Logistic function
def logistic_function(growth_rate, init_pop, cap_pop, time, midpoint):
    return init_pop + (cap_pop - init_pop) / (1 + np.exp(-growth_rate * (time - midpoint)))

# Function to calculate active customers
def calculate_actives(df, active_rates, ar_scen, init_pop, ar_init_pop):
    periods = len(df)
    active_rates = active_rate_scenarios[ar_scen]

    # Initialize the cohort DataFrame
    cohort_df = pd.DataFrame(0, index=range(periods), columns=range(1, periods + 1), dtype=float)

    # Calculate cohort actives
    for start_year in range(1, periods + 1):
        new_customers = df.loc[df['Months'] == start_year, 'New Customers'].values[0]
        rates_to_apply = active_rates[:periods - start_year + 1]
        cohort_values = (new_customers * np.array(rates_to_apply)).astype(float)
        cohort_df.loc[start_year - 1: start_year - 1 + len(rates_to_apply) - 1, start_year] = cohort_values

    # Add initial population to the first column
    cohort_df[1] += init_pop * ar_init_pop

    # Calculate total active customers by summing across cohorts
    total_actives = cohort_df.sum(axis=1).astype(int)

    return total_actives