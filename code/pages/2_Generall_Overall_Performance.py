import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
import folium
from streamlit_folium import st_folium
import random
import pydeck as pdk

def large_number_to_readable_format(number):

    if number < 1000:
        return str(number)
    elif number >= 1000 and number < 1000000:
        return f"{number / 1000:.1f}K"
    elif number >= 1000000 and number < 1000000000:
        return f"{number / 1000000:.1f}M"
    elif number >= 1000000000 and number < 1000000000000:
        return f"{number / 1000000000:.1f}B"
    else:
        return f"{number / 1000000000000:.1f}T"

def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
try:
    df = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/most_frequent_airports.csv')
except:
    df = pd.read_csv('code/pages/csv/most_frequent_airports.csv')
sorted_years = sorted(df['year'].unique())
print(sorted_years)

years=st.selectbox(label="Select a year", options=sorted_years)
print(years)
filter_df = df[df['year'] == years]
print(filter_df)

colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000']
layer_data = []
for index, row in filter_df.iterrows():
    color = colors[index % len(colors)]
    color = color.lstrip('#')
    layer_data.append({
        "origin": [row["origin_lng"], row["origin_lat"]],
        "destination": [row["destination_lng"], row["destination_lat"]],
        "tooltip": f"{row['origin']} to {row['destination']}",
        "color":  tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    })

layer = pdk.Layer(
    type="LineLayer",
    data=layer_data,
    get_source_position="origin",
    get_target_position="destination",
    get_color="color",
    get_width=5,
    pickable=True
)
layer1=pdk.Layer(
'ScatterplotLayer',
data = layer_data,
get_position = 'origin',
get_color = '[0, 0, 0]',
get_radius = 60000,
)

layer2=pdk.Layer(
'ScatterplotLayer',
data = layer_data,
get_position = 'destination',
get_color = '[0, 0, 0]',
get_radius = 60000,
)
view_state = pdk.ViewState(
    latitude=filter_df["origin_lat"].mean(),
    longitude=filter_df["destination_lng"].mean(),
    zoom=3,
    pitch=50,
)




st.write(f'Flight Routes Map {years}')
with st.expander("List of the Top 10 Trips"):
    col1,col4,col2,col3, col5 = st.columns(5)
    for index, row in filter_df.iterrows():
        color = colors[index % len(colors)]
        with col1:
            st.metric(label="Origin", value=row['origin'])
        with col4:
            st.metric(label="",value='➡️')
        with col2:
            st.metric(label="Destination", value=row['destination'])
        with col3:
            st.metric(label="Amount of flights", value=large_number_to_readable_format(row['total']))
        with col5:
            st.write("")
            st.color_picker('', color, disabled=True)


st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',layers=[layer,layer1,layer2], initial_view_state=view_state, tooltip={"text": "{tooltip}"}))
