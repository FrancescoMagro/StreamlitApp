import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display

st.set_page_config(page_title="Domestic Airline Performance", page_icon='📈')
st.title("Domestic Airline Performance 📈")
try:
    df = pd.read_csv('code/pages/csv/yearly_on_time_performance.csv')
except:
    df = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/yearly_on_time_performance.csv')
try:
    overalldf = pd.read_csv('code/pages/csv/yearlyoverall.csv')
except:
    overalldf = pd.read_csv('/Users/francescomagro/Desktop/Streamlit/StreamlitApp/code/pages/csv/yearlyoverall.csv')
tab0,tab1, tab2 = st.tabs(["Home", "Top 5 US Airlines", "Worst 5 US Airlines"])

sorted_years = sorted(df['year'].unique())
print(type(sorted_years))
# Create a dropdown widget
sorted_airl = sorted(df['airlinename'].unique())
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
year_dropdown = st.sidebar.multiselect(
    label="Years", options=sorted_years
)
airline_name = st.sidebar.multiselect(
    label="Airline", options=sorted_airl
)
all_options = st.sidebar.checkbox("Select all Years")

if all_options:
    year_dropdown = sorted_years

all_options_air = st.sidebar.checkbox("Select all Airlines")

if all_options_air:
    airline_name = sorted_airl


with tab0:


    if all_options and all_options_air:
        st.write(f'Welcome to the Hompage you selected all years')
    elif year_dropdown == [] and airline_name == []:
        st.write(f'Welcome to the hompage please select the years and airlines in the sidebar')
    else:
        st.write(f'Welcome to the hompage this are your selected years {year_dropdown}')

    print(airline_name)
    with st.container():
        col1, col2, col3 = st.columns(3)
        filtered_df = df[(df['year'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
        sum = np.sum(filtered_df['totalflights'])
        minutessum = np.sum(filtered_df['sumofyearlydelayedsarrivalminutes'])
        depminutesum = np.sum(filtered_df['sumofyearlydelayeddeapartureminutes'])
        with col1:
            st.metric(f"Ammount of Flights",value=large_number_to_readable_format(sum))
        with col2:
            st.metric(f"Sum of arrival delay in minutes", value=large_number_to_readable_format(minutessum))
        with col3:
            st.metric(f"Sum of departure delay in minutes", value=large_number_to_readable_format(depminutesum))
    with st.container():
        filtered_df = df[(df['year'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
        filtered_df.sort_values(by='sumofyearlydelayeddeapartureminutes', axis=0,
                     ascending=False,
                     inplace = True)
        fig1 = px.bar(filtered_df, x='year', y='sumofyearlydelayeddeapartureminutes', color='airlinename',barmode='group',text_auto='.2s',
                     title=f'Yearly Departure Delay').update_layout(xaxis_title='Year', yaxis_title= 'Departure delay in Min')
        st.plotly_chart(figure_or_data=fig1)
        filtered_df = df[(df['year'].isin(year_dropdown)) & (df['airlinename'].isin(airline_name))]
        filtered_df.sort_values(by='sumofyearlydelayedsarrivalminutes', axis=0,  # for column sorting
                                ascending=False,
                                inplace=True)
        fig = px.bar(filtered_df, x='year', y='sumofyearlydelayedsarrivalminutes', color='airlinename',barmode='group',text_auto='.2s',
                     title=f'Yearly Arrival Delay').update_layout(xaxis_title='Year', yaxis_title= 'Arrival delay in Min')
        st.plotly_chart(figure_or_data=fig)
    with st.container():
        fig = px.scatter(filtered_df, x='ontimeperformancedeparture', y="ontimeperformancearrival", color='airlinename').update_layout(xaxis_title='Percentage of on time arrival', yaxis_title= 'Percentage of on time departure')
        st.plotly_chart(figure_or_data=fig)


with tab1:
    fil_df = overalldf[(overalldf['year'].isin(year_dropdown))]
    average_on_time_performance = fil_df.groupby('airlinename').agg(
        average_departure_performance=pd.NamedAgg(column='sumofyearlydelayeddeapartureminutes', aggfunc='mean'),
        average_arrival_performance=pd.NamedAgg(column='sumofyearlydelayedsarrivalminutes', aggfunc='mean'),


    ).reset_index()

    average_on_time_performance['average_overall_performance'] = average_on_time_performance[
        ['average_departure_performance', 'average_arrival_performance']].mean(axis=1)
    fil_df2 = df[(df['year'].isin(year_dropdown))]
    average_on_time_performance_perc = fil_df2.groupby('airlinename').agg(
        average_departure_performance_perc=pd.NamedAgg(column='ontimeperformancedeparture', aggfunc='mean'),
        average_arrival_performance_perc=pd.NamedAgg(column='ontimeperformancearrival', aggfunc='mean'),

    ).reset_index()
    average_on_time_performance_perc['average_overall_performance_perc'] = average_on_time_performance_perc[
        ['average_departure_performance_perc', 'average_arrival_performance_perc']].mean(axis=1)
    best_performing_airline = average_on_time_performance_perc.sort_values(by='average_overall_performance_perc',
                                                                     ascending=False).iloc[:5]

    fig1= px.bar(best_performing_airline, x='airlinename', y='average_overall_performance_perc',
                    text_auto='.4s', title='Top 5 Airlines based on Percentage',color='airlinename').update_layout( yaxis_title= 'Mean Performance in percentage')
    st.plotly_chart(figure_or_data=fig1)
    with st.expander("See The List"):
        best_performing_airline

    best_performing_airline_min = average_on_time_performance.sort_values(by='average_overall_performance',
                                                                      ascending=True).iloc[:5]

    fig = px.bar(best_performing_airline_min, x='airlinename', y='average_overall_performance',
                 text_auto='.4s', title='Top 5 Airlines based on Minutes',color='airlinename').update_layout(yaxis_title= 'Mean Performance in Min')

    st.plotly_chart(figure_or_data=fig)
    with st.expander("See The List"):
        best_performing_airline_min
with tab2:
    fil_df = overalldf[(overalldf['year'].isin(year_dropdown))]
    average_on_time_performance = fil_df.groupby('airlinename').agg(
        average_departure_performance=pd.NamedAgg(column='sumofyearlydelayeddeapartureminutes', aggfunc='mean'),
        average_arrival_performance=pd.NamedAgg(column='sumofyearlydelayedsarrivalminutes', aggfunc='mean')

    ).reset_index()
    average_on_time_performance['average_overall_performance'] = average_on_time_performance[
        ['average_departure_performance', 'average_arrival_performance']].mean(axis=1)

    fil_df2 = df[(df['year'].isin(year_dropdown))]
    average_on_time_performance_perc = fil_df2.groupby('airlinename').agg(
        average_departure_performance_perc=pd.NamedAgg(column='ontimeperformancedeparture', aggfunc='mean'),
        average_arrival_performance_perc=pd.NamedAgg(column='ontimeperformancearrival', aggfunc='mean'),

    ).reset_index()
    average_on_time_performance_perc['average_overall_performance_perc'] = average_on_time_performance_perc[
        ['average_departure_performance_perc', 'average_arrival_performance_perc']].mean(axis=1)
    best_performing_airline = average_on_time_performance_perc.sort_values(by='average_overall_performance_perc',
                                                                           ascending=True).iloc[:5]

    fig1 = px.bar(best_performing_airline, x='airlinename', y='average_overall_performance_perc',
                  text_auto='.4s', title='Top 5 Airlines based on Percentage', color='airlinename').update_layout(
        yaxis_title='Mean Performance in percentage')
    st.plotly_chart(figure_or_data=fig1)
    with st.expander("See The List"):
        best_performing_airline

    best_performing_airline_min = average_on_time_performance.sort_values(by='average_overall_performance',
                                                                      ascending=False).iloc[:5]

    fig = px.bar(best_performing_airline_min, x='airlinename', y='average_overall_performance',
                 text_auto='.4s',color='airlinename', title='Worst 5 Airlines based on Minutes').update_layout(yaxis_title= 'Mean Performance in Min')

    st.plotly_chart(figure_or_data=fig)
    with st.expander("See The List"):
        best_performing_airline_min

