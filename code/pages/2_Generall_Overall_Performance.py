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



m = folium.Map(location=[filter_df["origin_lat"].mean(), filter_df["origin_lng"].mean()], zoom_start=4)

for index, row in filter_df.iterrows():
    color = colors[index % len(colors)]

    origin = [row["origin_lat"], row["origin_lng"]]
    destination = [row["destination_lat"], row["destination_lng"]]
    route_name = f"{row['origin']} to {row['destination']} Amount of times: {row['total']}"

    folium.PolyLine([origin, destination], color=color, weight=4, opacity=1, popup=route_name).add_to(m)
    folium.CircleMarker(location=origin, radius=5, color=color, fill=True, fill_color=color, popup=f"Origin: {row['origin']}").add_to(m)
    folium.CircleMarker(location=destination, radius=5, color=color, fill=True, fill_color=color, popup=f"Destination: {row['destination']}").add_to(m)

# Streamlit app
st.title(f'Flight Routes Map {years}')

st.dataframe(filter_df)
st_folium(m, height=500, width=900)
