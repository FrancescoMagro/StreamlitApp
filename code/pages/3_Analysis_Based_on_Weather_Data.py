import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
st.set_page_config(page_title="Domestic Airline Performance", page_icon='📈')
st.write("# Wheater Analysis📈")
try:
    df = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/WeatherData.csv')
except:
    df = pd.read_csv('code/pages/csv/WeatherData.csv')
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

df['starttime'] = pd.to_datetime(df['starttime'])

sorted_years = sorted(df['starttime'].dt.year.unique())
print(sorted_years)
sorted_airport_code = sorted(df['airportcode'].unique())
year_dropdown2 = st.sidebar.multiselect(
    label="Years", options=sorted_years
)

select_all_years = st.sidebar.checkbox("Select all Years")

if select_all_years:

    year_dropdown2 = sorted_years
print(year_dropdown2)


airport_code = st.sidebar.selectbox(
    label="Airport", options=sorted_airport_code
)
filtered_df = df[df['starttime'].dt.year.isin(year_dropdown2)]
print(filtered_df.head())
filtered_df = filtered_df[filtered_df['airportcode']==airport_code]

fig1 = px.line(filtered_df, x='starttime', y='amount_of_events', title=f'Events per Year for {airport_code} ').update_layout(
    yaxis_title='Events Per Year')
st.plotly_chart(figure_or_data=fig1)
