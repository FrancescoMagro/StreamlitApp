import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
st.set_page_config(page_title="Domestic Airline Performance", page_icon='📈')
st.write("# General Overall Performance📈")
try:
    df = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/generall_overall_perf.csv')
except:
    df = pd.read_csv('code/pages/csv/generall_overall_perf.csv')
sorted_years = sorted(df['flightdate'].dt.year.unique())
year_dropdown = st.sidebar.multiselect(
    label="Years", options=sorted_years
)
select_all_years = st.sidebar.checkbox("Select all")

if select_all_years:
    year_dropdown = sorted_years

filtered_df = df[df['flightdate'].dt.year.isin(year_dropdown)]

average_on_time_performance_perc = filtered_df.groupby('flightdate').agg(
    average_departure_performance_perc=pd.NamedAgg(column='ontimeperformancedeparture', aggfunc='mean'),
    average_arrival_performance_perc=pd.NamedAgg(column='ontimeperformancearrival', aggfunc='mean'),

).reset_index()
average_on_time_performance_perc['average_overall_performance_perc'] = average_on_time_performance_perc[
    ['average_departure_performance_perc', 'average_arrival_performance_perc']].mean(axis=1)
print(average_on_time_performance_perc.head())
fig1 = px.line(average_on_time_performance_perc, x='flightdate', y='average_departure_performance_perc').update_layout(
    yaxis_title='Mean Performance in percentage')
fig2 = px.line(average_on_time_performance_perc, x='flightdate', y='average_arrival_performance_percyxy').update_layout(
    yaxis_title='Mean Performance in percentage')
st.plotly_chart(figure_or_data=fig1)
