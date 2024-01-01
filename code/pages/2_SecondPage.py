import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
st.set_page_config(page_title="Domestic Airline Performance", page_icon='📈')
st.write("# Domestic Airline Performance 📈")
df = pd.read_csv('code/pages/csv/new.csv')
tab0,tab1, tab2 = st.tabs(["home","1", "2"])
pivot_df = df.pivot(index='airlinename', columns='date_part', values='count').reset_index()
pivot_df.fillna(0, inplace=True)
fig = px.box(df, x='date_part', y='count', color='airlinename', points='all',
             labels={'date_part': 'Year', 'count': 'Sum', 'airlinename': 'Operating Carrier'},
             title='Yearly Boxplot of amount of deleyed flight by Operating Carrier',
             category_orders={'date_part': sorted(df['date_part'].unique())})

sorted_years = sorted(df['date_part'].unique())
print(type(sorted_years))
# Create a dropdown widget
sorted_airl = sorted(df['airlinename'].unique())
year_dropdown = st.sidebar.multiselect(
    label="Years",options=sorted_years
)
all_options = st.sidebar.checkbox("Select all Years")

if all_options:
    year_dropdown = sorted_years
airline_name = st.sidebar.multiselect(
    label="Airline", options=sorted_airl
)
all_options_air = st.sidebar.checkbox("Select all Airlines")

if all_options_air:
    airline_name = sorted_airl

print(airline_name)

with tab0:
    filtered_df = df[(df['date_part'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
    sum = np.sum(filtered_df['count'])
    st.metric(label="Sum of delayed minutes", value=sum,
              delta_color="inverse")

with tab1:
    filtered_df = df[(df['date_part'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
    fig = px.bar(filtered_df, x='airlinename', y='count', color='airlinename',

                     title=f'Bar Plot for {year_dropdown}')
    st.plotly_chart(figure_or_data=fig)

with tab2:
    filtered_df = df[(df['date_part'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
    st.dataframe(filtered_df)

