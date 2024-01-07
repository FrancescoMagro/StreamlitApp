import streamlit as st
import pandas as pd

import plotly.express as px
st.set_page_config(page_title="Airline Flight Data Visualization", page_icon='📈')
st.title("Airline Flight Data Visualization📈")

#
data = pd.read_csv('code/pages/csv/FlownFlights.csv')

if data is not None:
    airline = st.selectbox('Select the Airline', data['operatingcarrier'].unique())

    data['year'] = data['year'].fillna(0)
    data['flown_flights'] = data['flown_flights'].fillna(0)

    filtered_data = data[data['operatingcarrier'] == airline]

    fig1 = px.bar(filtered_data, x='year',y='flown_flights',text_auto='.2s',
    title=f'Flown Flights Over Years for {airline}').update_layout(xaxis_title='Year', yaxis_title= 'Flown Flights')

    st.plotly_chart(figure_or_data=fig1)