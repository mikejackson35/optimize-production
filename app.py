from pulp import LpProblem, LpMaximize, LpVariable

import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
import altair as alt

## DISPLAY CONFIGS
# Streamlit
st.set_page_config(
    page_title='Optimal Production',
    page_icon=':eggplant:',
    layout='wide'
    )
# css
with open(r"styles/main.css") as f:                                          
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True) 
#plotly
config = {'displayModeBar': False}

# Define the function
def get_production_optimals(num_workers, num_machines, profit_shirt, profit_pant, profit_short, machine_time_shirt, machine_time_pant, machine_time_short, worker_time_shirt, worker_time_pant, worker_time_short):
    # instantiate a Problem
    model = LpProblem("maximize_profit", LpMaximize)

    # define variables
    num_shirts = LpVariable('num_shirts', lowBound=0, cat='Integer')
    num_pants = LpVariable('num_pants', lowBound=0, cat='Integer')
    num_shorts = LpVariable('num_shorts', lowBound=0, cat='Integer')

    # define Objective
    model += profit_shirt * num_shirts + profit_pant * num_pants + profit_short * num_shorts

    # define Constraints
    model += machine_time_shirt * num_shirts + machine_time_pant * num_pants + machine_time_short * num_shorts <= num_machines * 30
    model += worker_time_shirt * num_shirts + worker_time_pant * num_pants + worker_time_short * num_shorts <= num_workers * 30

    # Solve the model
    model.solve()

    return num_shirts.varValue, num_pants.varValue, num_shorts.varValue

# Set the title of the app
st.title("Production Optimization")
st.write(" ")
st.caption("Adjust constraints",unsafe_allow_html=True)
st.markdown("Scenario:  You own a garment factory that makes shirts, pants, and shorts.<br>The factory mans anywhere from 1-10 workers at a time and deploys up to 10 sewing machines. <br>Adjust the constraints below to display optimal production output of each style garment in order to maximize profit.",unsafe_allow_html=True)

# Create columns for the sliders
col1, blank, col2, blank, col3, blank, col4, blank = st.columns(8)

# Group sliders for workers and machines
with col1:
    st.markdown("##### Resources")
    st.write(" ")
    num_workers = st.slider("Number of Workers", min_value=1, max_value=10, value=3, step=1)
    num_machines = st.slider("Number of Machines", min_value=1, max_value=10, value=2, step=1)

# Group sliders for shirts
with col2:
    st.markdown("##### Shirts")
    st.write(" ")
    profit_shirt = st.slider("Profit per Shirt ($)", min_value=1.0, max_value=3.00, value=1.85, step=.05)
    machine_time_shirt = st.slider("Machine Time per Shirt (days)", min_value=0.01, max_value=.2, value=0.03, step=.01)
    worker_time_shirt = st.slider("Worker Time per Shirt (days)", min_value=0.01, max_value=.2, value=0.07, step=.01)

# Group sliders for pants
with col3:
    st.markdown("##### Pants")
    st.write(" ")
    profit_pant = st.slider("Profit per Pant ($)", min_value=1.0, max_value=3.00, value=2.20, step=.05)
    machine_time_pant = st.slider("Machine Time per Pant (days)", min_value=0.01, max_value=.2, value=0.07, step=.01)
    worker_time_pant = st.slider("Worker Time per Pant (days)", min_value=0.01, max_value=.2, value=0.06, step=.01)

# Group sliders for shorts
with col4:
    st.markdown("##### Shorts")
    st.write(" ")
    profit_short = st.slider("Profit per Short ($)", min_value=1.0, max_value=3.00, value=2.25, step=.05)
    machine_time_short = st.slider("Machine Time per Short (days)", min_value=0.01, max_value=.2, value=0.06, step=.01)
    worker_time_short = st.slider("Worker Time per Short (days)", min_value=0.01, max_value=.2, value=0.07, step=.01)

# Calculate optimal production in real-time
num_shirts, num_pants, num_shorts = get_production_optimals(
    num_workers, num_machines,
    profit_shirt, profit_pant, profit_short,
    machine_time_shirt, machine_time_pant, machine_time_short,
    worker_time_shirt, worker_time_pant, worker_time_short
)

# Display the results prominently as st.metric objects
st.write(" ")
st.write(" ")
container = st.container(border=True)
with container:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Shirts", value=int(num_shirts))
    col2.metric(label="Pants", value=int(num_pants))
    col3.metric(label="Shorts", value=int(num_shorts))

