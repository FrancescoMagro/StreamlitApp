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
data = {
    "year": [2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
    "origin": ["LAX", "LAS", "LGA", "BOS", "JFK", "DEN", "DEN", "ATL"],
    "destination": ["SFO", "LAX", "ORD", "DCA", "LAX", "LAS", "PHX", "MCO"],
    "total": [17721, 15952, 15231, 15171, 15032, 14058, 13805, 13319],
    "origin_lat": [33.9382, 36.0719, 40.7794, 42.3606, 40.6392, 39.8466, 39.8466, 33.6301],
    "origin_lng": [-118.3865, -115.1634, -73.8803, -71.0097, -73.7639, -104.6562, -104.6562, -84.4418],
    "destination_lat": [37.6196, 33.9382, 41.9875, 38.8472, 33.9382, 36.0719, 33.4277, 28.4183],
    "destination_lng": [-122.3656, -118.3865, -87.9319, -77.0345, -118.3865, -115.1634, -112.0038, -81.3241]
}
df = pd.DataFrame(data)

# Create a Map centered around the average latitude and longitude
m = folium.Map(location=[df["origin_lat"].mean(), df["origin_lng"].mean()], zoom_start=4)

# Adding routes with different colors and markers to the map
for _, row in df.iterrows():
    color = random_color_generator()  # Generate a random color for each route

    # Origin and Destination coordinates
    origin = [row["origin_lat"], row["origin_lng"]]
    destination = [row["destination_lat"], row["destination_lng"]]
    route_name = f"{row['origin']} to {row['destination']}"

    # Draw the flight route with a popup
    folium.PolyLine(
        [origin, destination], color=color, weight=2.5, opacity=1,
        popup=route_name
    ).add_to(m)

    # Add markers for Origin and Destination with a popup
    folium.CircleMarker(
        location=origin, radius=5, color=color, fill=True,
        fill_color=color, popup=f"Origin: {row['origin']}"
    ).add_to(m)
    folium.CircleMarker(
        location=destination, radius=5, color=color, fill=True,
        fill_color=color, popup=f"Destination: {row['destination']}"
    ).add_to(m)

# Display the map

# Streamlit app
st.title('Flight Routes Map')
st_folium(m, width=700, height=500)