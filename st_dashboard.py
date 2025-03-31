############################################ CITIBIKES DASHBOARD ####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

##################################### INITIALIZE SETTINGS FOR DASHBOARD #############################################

st.set_page_config(page_title = 'New York Citi Bikes Strategy Dashboard', layout='wide')
st.title("New York Citi Bikes Strategy Dashboard")
st.markdown("The dashboard will help make informed decisions regarding Citi Bike's availability issues and bike distribution across the city.")
st.markdown("Since Citi Bike's launch in 2013, popularity for sustainable and convenient transportation has increased. The Covid-19 pandemic created higher demand leading to distribution problems and, customer complaints, such as fewer bikes at popular stations and the inability to return bikes due to full docking stations. This analysis aims to diagnose the root of the distribution problem and provide actionable insights.")

############################################### IMPORT DATA #########################################################

df = pd.read_csv('Data/Prepared Data/reduced_data.csv', index_col = 0)
top20 = pd.read_csv('Data/Prepared Data/top20.csv', index_col = 0)

############################################## DEFINE CHARTS ########################################################

##### Bar Chart #####

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'viridis_r'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Total trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


##### Line Chart #####

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['daily_rides'], name = 'Daily Bike Rides',
           marker={'color': df['daily_rides'],'color': 'blue'}),
    secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp_F'], name = 'Daily Temperature',
           marker={'color': df['avgTemp_F'],'color': 'red'}),
    secondary_y=True
)

fig_2.update_layout(
    title = 'Daily Bike Trips and Temperature in New York 2022',
    xaxis_title = 'Month',
    yaxis=dict(
        title="Total Rides",
        titlefont=dict(color="blue"),
        tickfont=dict(color="blue")  
    ),
    yaxis2=dict(
        title="Average Temperature (\u00B0F)",
        titlefont=dict(color="red"),
        tickfont=dict(color="red"),
        overlaying="y",
        side="right"
    ),
    width = 1100, height = 400
)

st.plotly_chart(fig_2, use_container_width=True)


##### Add html Map #####

path_to_html = "NY CitiBike Trips Aggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)