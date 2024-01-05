import streamlit as st
import pandas as pd
import pydeck as pdk


st.title('Airport Weather Event Visualization')

weather_types = ['Rain', 'Snow', 'Fog', 'Hail', 'Cold', 'Storm']


selected_weather = st.selectbox('Select weather type', weather_types)
file_name = 'code/pages/csv/weath.csv'
df = pd.read_csv(file_name)

st.title('Airport Rain Event Visualization')

selected_month = st.slider('Select a month', 1, 12)

selected_year = st.selectbox('Select a year', df['year'].unique())

airport_options = ['All Airports'] + df['airportcode'].unique().tolist()
selected_airport = st.selectbox('Select an airport', airport_options)

if selected_airport != 'All Airports':
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year) & (df['airportcode'] == selected_airport)]
else:
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year)]
filtered_df = filtered_df[filtered_df['weathertype'] == selected_weather]
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=filtered_df['locationlat'].mean(),
         longitude=filtered_df['locationlng'].mean(),
         zoom=3,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[locationlng, locationlat]',
            get_color='[200, 30, 0, 160]',
            get_radius='numberofevents * 1000',
         ),
     ],

 ),tooltip=filtered_df['numberofevents'])