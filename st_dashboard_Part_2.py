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
from numerize.numerize import numerize
from PIL import Image

####################################### INITIAL SETTINGS FOR DASHBOARD ##############################################

st.set_page_config(page_title = 'New York Citi Bikes Strategy Dashboard', layout='wide')
st.title("New York Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Introduction","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

############################################### IMPORT DATA #########################################################

df = pd.read_csv('small_data_for_dash.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

############################################### DEFINE PAGES ########################################################

##### Introduction (pg.1) #####

if page == "Introduction":
    st.markdown("#### This dashboard aims to help make informed decisions regarding Citi Bike's availability issues and bike distribution across the city.")
    st.markdown("Since Citi Bike's launch in 2013, popularity for sustainable and convenient transportation has increased. The Covid-19 pandemic created higher demand leading to distribution problems and, customer complaints, such as fewer bikes at popular stations and the inability to return bikes due to full docking stations. This analysis looks to diagnose the root of the distribution and demand problem and provide actionable insights. The dashboard is separated into 4 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("#### The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis.")

    myImage = Image.open("Citi-Bike-image.jpg") # image source: https://citibikenyc.com/blog/program-expansion2023
    st.image(myImage)


##### Line Chart (pg.2) #####

elif page == 'Weather component and bike usage':

    ## Create a month filter ##
    with st.sidebar:
        month_filter = st.multiselect(label= 'Select the month(s)', options=df['month_name'].unique(),
    default=df['month_name'].unique())

    df1 = df.query('month_name == @month_filter')
    
    ## Define the metrics ##
    col1, col2 = st.columns(2)
    with col1:
        monthly_rides = float(df1['daily_rides'].count())    
        st.metric(label = 'Total Bike Rides', value= numerize(monthly_rides))
    with col2:
        monthly_avgTemp = float(df1['avgTemp_F'].mean())
        st.metric(label = 'Average Temperature (\u00B0F)', value= numerize(monthly_avgTemp))
    
    st.markdown("##### Use the filter on the left to select one or more months to view. The metrics will also change to reflect the months selected.")
    
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df1['date'], y = df1['daily_rides'], name = 'Daily Bike Rides',
               marker={'color': df1['daily_rides'],'color': 'blue'}),
        secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df1['date'], y = df1['avgTemp_F'], name = 'Daily Temperature',
               marker={'color': df1['avgTemp_F'],'color': 'red'}),
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
    st.markdown("There is a clear correlation in the relationship between the temperature and the frequency of bike trips taken daily. As temperatures decrease, so does bike usage. And as temperatures rise we se an increase in daily rides. This insight indicates that the bike shortage problem may predominantly occur during the warmer periods of the year, approximately from mid-April to the end of October.")


##### Bar Chart (pg.3) #####

elif page == 'Most popular stations':

    ## Create season filter on the side bar ##   
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season(s)', options=df['season'].unique(),
    default=df['season'].unique())

    df2 = df.query('season == @season_filter')
    
    ## Define the total rides ##
    total_rides = float(df2['daily_rides'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

    st.markdown("##### Use the filter on the left to select one or more seasons to view.")
    
    ## Create bar chart ##
    df2['value'] = 1 
    df_groupby_bar = df2.groupby('start_station_name').agg({'value': 'sum'}).reset_index()
    top20_1 = df_groupby_bar.nlargest(20, 'value')
   
    fig = go.Figure(go.Bar(x = top20_1['start_station_name'], y = top20_1['value'], marker={'color': top20_1['value'],'colorscale': 'viridis_r'}))
    fig.update_layout(
        title = 'Top 20 Most Popular Bike Stations in New York',
        xaxis_title = 'Start stations',
        yaxis_title ='Total trips',
        width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Looking at the bar chart, it is obvious that the Grove Street PATH is the most popular starting station by far. The next top three include South Waterfront Walkway - Sinatra Drive & 1st Street, and two Hoboken Terminal locations one at River Street & Hudson Place and the other at Hudson Street & Hudson Place. Then, there is a significant jump down to the next station on the list (the City Hall location) and it is around half that of the most popular station (Grove Street). This indicates that there is a clear preference for the first four starting stations listed. We can cross reference these findings with the interactive map that you can access through the side bar menu.")
    st.markdown("Seasonal filtering reveals that the most popular station varies by season, yet consistently belongs to the overall top-ranked stations.")
    

##### Add HTML Map (pg.4) #####

elif page == 'Interactive map with aggregated bike trips':

    st.write("Interactive Map Showing Aggregated Bike Trips Around New York")

    path_to_html = "NY CitiBike Trips Aggregated.html" 

    ## Read file and keep in variable ##
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage ##
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most frequent trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("Grove Street PATH, South Waterfront Walkway - Sinatra Drive & 1st Street, Hoboken Terminal - River Street & Hudson Place, and Hoboken Terminal - Hudson Street & Hudson Place. While filtering out routes of less than 3000 trips, we can see that most of our top starting stations also have the most trips. The exception is the Hoboken Terminal - River Street & Hudson Place. While it was third on the list of most popular start stations it isn't among those with the most trips.")
    st.markdown("An important note is there are some trips that aren't shown with an arc because the bikes were rented from one station and returned to the same station. One example is the South Waterfront Walkway station. If you hover your cursor over the dot itself you can see that the start and end station are the same and it has a total of 5,439 trips.")
    st.markdown("Some other most common routes (>3,000) are between Hoboken Terminal - Hudson Street & Hudson Place to Hoboken Avenue at Monmouth Street, Grove Street PATH to Marin Light Rail and vice versa, and round trips at Liberty Light Rail.")
    st.markdown("The biggest insight here is all of these stations and trips are located near major public transportation, such as light rails, train stations, bus stops, ferries, and subways. These stations are also located on the Jersey side of the Hudson River close to the waterfront.")

##### Recommendations Page (pg.5) #####

else:
    
    st.header("Conclusions and Recommendations")
    bikes = Image.open("parked-city-bike.jpg")  #source: https://www.freepik.com/free-photo
    st.image(bikes)
    st.markdown("### My analysis has shown that Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations along the Jersey side of the Hudson River, particularly around Hoboken Terminal, Newport Center near the Holland Tunnel, Downtown Jersey City along the water line, and north up Sinatra Drive to 14th Street.")
    st.markdown("- Stations should also be added around major public transportation depots. Along with those already mentioned like Hoboken Terminal and Newport Center, others further inland should also be included, specifically around Journal Square Transportation and especially at the intersection of Grove Street and Christopher Columbus Drive. The Grove Street location is a very popular spot since it's at the heart of Jersey City with an entrance to the subway station and number of shops and restaurants around.")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but reduce supply in late autumn, through winter, and into early spring to reduce logistics costs. The slower winter months can also be used to conduct maintainance on the bikes and determine if upgrades or replacements are needed.")