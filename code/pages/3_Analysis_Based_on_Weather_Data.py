import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
import pydeck as pdk
st.set_page_config(page_title="Analysis Based on Weather Data", page_icon='📈')
st.title("Analysis Based on Weather Data📈")


weather_types = ['Rain', 'Snow', 'Fog', 'Hail', 'Cold', 'Storm']


selected_weather = st.sidebar.selectbox('Select Weather Type', weather_types)
try:
    file_name = 'code/pages/csv/weath.csv'
    df = pd.read_csv(file_name)
except:
    file_name = '/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/weath.csv'
    df = pd.read_csv(file_name)


st.subheader(f'Event Map Visualization for the Weather: {selected_weather}')

selected_month = st.slider('Select a Month', 1, 12)

selected_year = st.sidebar.selectbox('Select a Year', df['year'].unique())

airport_options = ['All Airports'] + sorted(df['airportcode'].unique())
selected_airport = st.selectbox('Select an Airport', airport_options)

if selected_airport != 'All Airports':
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year) & (df['airportcode'] == selected_airport)]
else:
    filtered_df = df[(df['month'] == selected_month) & (df['year'] == selected_year)]
filtered_df2 = filtered_df[filtered_df['weathertype'] == selected_weather]
sum_of_events=np.sum(filtered_df2['numberofevents'])
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

st.subheader(f'Number of {selected_weather} Events: {sum_of_events}')
try:
    df = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/WeatherData.csv')
    df2 = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/arrivalWeatherDelay.csv')
except:
    df = pd.read_csv('code/pages/csv/WeatherData.csv')
    df2=pd.read_csv('code/pages/csv/arrivalWeatherDelay.csv')
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
df2['flightdate'] = pd.to_datetime(df2['flightdate'])

sorted_airport_code = sorted(df2['destination'].unique())
all_selected_airports = ['All Airports']+ sorted_airport_code
sorted_arrival_severity = sorted(df2['destination_severity'].unique())

#if selected_airport != 'All Airports':
#    print(selected_airport)
#    filtered_df = filtered_df[filtered_df['airportcode'] == selected_airport]



#filtered_df = df[df['starttime'].dt.year==selected_year]


selected_air = st.selectbox('Select an Airport', all_selected_airports)
selected_severity = st.selectbox('Select the Severity', sorted_arrival_severity)
filtered_df2 = df2[(df2['flightdate'].dt.year==selected_year)&(df2['destination_weather']==selected_weather)]
if selected_air == 'All Airports':
    tmp_air = sorted_airport_code
    filtered_df2 = filtered_df2[(filtered_df2['destination'].isin(tmp_air))]
else:
    filtered_df2 = filtered_df2[(filtered_df2['destination']==selected_air)]

filtered_df2 = filtered_df2[filtered_df2['destination_severity'] == selected_severity]

print(filtered_df2.head())
subfig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2 = px.line(filtered_df2, x='flightdate', y='sum')

try:
    df2 = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/DepartureWeatherDelay.csv')
    df3 = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/generalDelayNoWeather.csv')
except:
    df2 = pd.read_csv('code/pages/csv/DepartureWeatherDelay.csv')
    df3 = pd.read_csv('code/pages/csv/generalDelayNoWeather.csv')

df2['flightdate'] = pd.to_datetime(df2['flightdate'])


filtered_df4 = df3[(df3['year']==selected_year)]
filtered_df3 = df2[(df2['flightdate'].dt.year==selected_year)&(df2['origin_weather']==selected_weather)]
if selected_air == 'All Airports':
    tmp_air = sorted_airport_code
    filtered_df3 = filtered_df3[(filtered_df3['origin'].isin(tmp_air))]
    filtered_df4 = filtered_df4[(filtered_df4['origin'].isin(tmp_air))]

else:
    print("test")
    filtered_df3 = filtered_df3[(filtered_df3['origin']==selected_air)]
    filtered_df4 = filtered_df4[(filtered_df4['origin']==selected_air)]

filtered_df3 = filtered_df3[filtered_df3['origin_severity'] == selected_severity]
number_of_events = filtered_df2.groupby('flightdate').size()
number_of_events2 = filtered_df3.groupby('flightdate').size()

number_of_events = number_of_events.reset_index(name='count')
number_of_events2 = number_of_events2.reset_index(name='count')
print(filtered_df4.head())
#number_of_events['Count'] = number_of_events['Count']+number_of_events2['Count']
subfig2.add_scatter(x=filtered_df2['flightdate'], y=filtered_df2['sum'],  name="Sum of Delay at Arrival" ,marker=dict(color="MediumPurple"))
subfig2.add_scatter(x=filtered_df3['flightdate'], y=filtered_df3['sum'],  name="Sum of Delay at Departure")
subfig2.add_scatter(x=number_of_events['flightdate'], y=number_of_events['count'], yaxis="y2", name="Amount of Events at Arrival")
subfig2.add_scatter(x=number_of_events2['flightdate'], y=number_of_events2['count'], yaxis="y2", name="Amount of Events at Departure")

subfig2.layout.xaxis.title="Flight Date"
subfig2.layout.yaxis.title="Delay in Minutes"
subfig2.layout.yaxis2.title="Amount of events"
subfig2.layout.title = f'Delay in Minutes Arrival/Departure in: {selected_year}'

fig4 = px.line(filtered_df4, x='month',y='sum', title="Amount of Events")
st.plotly_chart(figure_or_data=subfig2)
st.plotly_chart(figure_or_data=fig4)

