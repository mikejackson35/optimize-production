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
    model += machine_time_shirt * num_shirts + machine_time_pant * num_pants + machine_time_short * num_shorts <= num_machines * 240
    model += worker_time_shirt * num_shirts + worker_time_pant * num_pants + worker_time_short * num_shorts <= num_workers * 240

    # Solve the model
    model.solve()

    return num_shirts.varValue, num_pants.varValue, num_shorts.varValue

col1,col2,blank = st.columns([1.25,3.5,.25])
with col1:
    # Set the title of the app
    st.markdown("## Production<br>Optimization",unsafe_allow_html=True)
    st.markdown("#### Using Python &<br>Linear Programming",unsafe_allow_html=True)
with col2:
    st.write(" ")
    # st.markdown("Scenario:<br>You own a garment factory that makes shirts, pants, and shorts.<br>The factory mans anywhere from 1-10 workers at a time and deploys up<br>to 10 sewing machines. Adjust the constraints below to display optimal<br>production output of each style garment in order to maximize profit.",unsafe_allow_html=True)
    st.write("")

    placeholder = st.empty()

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

# Create columns for the sliders
col1, blank, col2, blank, col3, blank, col4, blank = st.columns(8)

# Group sliders for workers and machines
with col1:
    st.markdown("##### Resources")
    st.write(" ")
    num_machines = st.selectbox("Number of Sewing Machines", (4,5,6))
    num_workers = st.selectbox("Number of Workers", (6,7,8,9,10))

container = st.container(border=True)
with container:
    # Group sliders for shirts
    with col2:
        st.markdown("##### Shirts")
        st.write(" ")
        profit_shirt = st.slider("Profit per Shirt ($)", min_value=2.0, max_value=4.0, value=3.3, step=.1)
        st.write("")
        machine_time_shirt = st.slider("Machine Time Shirt (mins)", min_value=.5, max_value=3.0, value=1.3, step=.1)
        st.write("")
        worker_time_shirt = st.slider("Labor Shirt (mins)", min_value=2.0, max_value=5.0, value=2.5, step=.1)

# Group sliders for pants
with col3:
    st.markdown("##### Pants")
    st.write(" ")
    profit_pant = st.slider("Profit per Pant ($)", min_value=4.0, max_value=6.0, value=4.9, step=.1)
    st.write("")
    machine_time_pant = st.slider("Machine Time Pants (mins)", min_value=1.0, max_value=4.0, value=2.3, step=.1)
    st.write("")
    worker_time_pant = st.slider("Labor Pants (mins)", min_value=2.0, max_value=5.0, value=3.1, step=.1)

# Group sliders for shorts
with col4:
    st.markdown("##### Shorts")
    st.write(" ")
    profit_short = st.slider("Profit per Short ($)", min_value=3.0, max_value=5.0, value=4.0, step=.1)
    st.write("")
    machine_time_short = st.slider("Machine Time Shorts (mins)", min_value=1.0, max_value=4.0, value=1.8, step=.1)
    st.write("")
    worker_time_short = st.slider("Labor Shorts (mins)", min_value=2.0, max_value=5.0, value=2.7, step=.1)

# Calculate optimal production in real-time
num_shirts, num_pants, num_shorts = get_production_optimals(
    num_workers, num_machines,
    profit_shirt, profit_pant, profit_short,
    machine_time_shirt, machine_time_pant, machine_time_short,
    worker_time_shirt, worker_time_pant, worker_time_short
)

# Display the results prominently as st.metric objects
with placeholder:
    st.write(" ")
    st.write(" ")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Shirts", value=int(num_shirts))
    col2.metric(label="Pants", value=int(num_pants))
    col3.metric(label="Shorts", value=int(num_shorts))
    col4.metric(label="Profit ($)", value=f"${int(profit_shirt * num_shirts + profit_pant * num_pants + profit_short * num_shorts)}")