import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Airport Weather Event Visualization", page_icon='📈')
st.title('Airport Weather Event Visualization📈')

weather_types = ['Rain', 'Snow', 'Fog', 'Hail', 'Cold', 'Storm']


selected_weather = st.selectbox('Select Weather Type', weather_types)
try:
    file_name = 'code/pages/csv/weath.csv'
    df = pd.read_csv(file_name)
except:
    file_name = '/code/pages/csv/weath.csv'
    df = pd.read_csv(file_name)


st.title(f'Event Map Visualization for the Weather: {selected_weather}')

selected_month = st.slider('Select a Month', 1, 12)

selected_year = st.selectbox('Select a Year', df['year'].unique())

airport_options = ['All Airports'] + df['airportcode'].unique().tolist()
selected_airport = st.selectbox('Select an Airport', airport_options)

if selected_airport != 'All Airports':
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year) & (df['airportcode'] == selected_airport)]
else:
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year)]
filtered_df2 = filtered_df[filtered_df['weathertype'] == selected_weather]

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
            data=filtered_df2,
            get_position='[locationlng, locationlat]',
            get_color='[200, 30, 0, 160]',
            get_radius='numberofevents * 1000',
         ),
     ]

 ))