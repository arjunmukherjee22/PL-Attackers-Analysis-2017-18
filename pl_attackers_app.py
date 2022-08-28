import datetime
import unicodedata

import markdown
import json
import numpy as np
import pandas as pd

import bokeh

import streamlit as st

from plots import *


@st.cache(allow_output_mutation=True)
def get_data(foot):

    #Reading Data
    salah_events_data_df = pd.read_pickle("./data/salah_events_data_df.pkl")
    kane_events_data_df = pd.read_pickle("./data/kane_events_data_df.pkl")
    debruyne_events_data_df = pd.read_pickle("./data/debruyne_events_data_df.pkl")
    aubameyang_events_data_df = pd.read_pickle("./data/aubameyang_events_data_df.pkl")

    #Dealing with double backslashes
    salah_events_data_df['label'] = salah_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    kane_events_data_df['label'] = kane_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    debruyne_events_data_df['label'] = debruyne_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    aubameyang_events_data_df['label'] = aubameyang_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))

    if foot == 'Left':
       salah_events_data_df = salah_events_data_df[salah_events_data_df['left_foot']]
       kane_events_data_df = kane_events_data_df[kane_events_data_df['left_foot']]
       debruyne_events_data_df = debruyne_events_data_df[debruyne_events_data_df['left_foot']]
       aubameyang_events_data_df = aubameyang_events_data_df[aubameyang_events_data_df['left_foot']]

    if foot == 'Right':
       salah_events_data_df = salah_events_data_df[salah_events_data_df['right_foot']]
       kane_events_data_df = kane_events_data_df[kane_events_data_df['right_foot']]
       debruyne_events_data_df = debruyne_events_data_df[debruyne_events_data_df['right_foot']]
       aubameyang_events_data_df = aubameyang_events_data_df[aubameyang_events_data_df['right_foot']]

    liverpool_matches_dates_df = pd.read_pickle("./data/liverpool_matches_played_df.pkl")
    tottenham_matches_dates_df = pd.read_pickle("./data/tottenham_matches_played_df.pkl")
    city_matches_dates_df = pd.read_pickle("./data/city_matches_played_df.pkl")
    arsenal_matches_dates_df = pd.read_pickle("./data/arsenal_matches_played_df.pkl")

    liverpool_matches_dates_df['match'] = liverpool_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    tottenham_matches_dates_df['match'] = tottenham_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    city_matches_dates_df['match'] = city_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    arsenal_matches_dates_df['match'] = arsenal_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))

    return salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df


def plot_goals(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df):

    #Getting events data positions
    salah_goals = salah_events_data_df[salah_events_data_df['goal'] == True]['positions']
    kane_goals = kane_events_data_df[kane_events_data_df['goal'] == True]['positions']
    debruyne_goals = debruyne_events_data_df[debruyne_events_data_df['goal'] == True]['positions']
    aubameyang_goals = aubameyang_events_data_df[aubameyang_events_data_df['goal'] == True]['positions']

    #Pitch with events
    p_salah = plot_events(salah_goals, 'Goals', 'red')
    p_kane = plot_events(kane_goals, 'Goals', 'pink')
    p_debruyne = plot_events(debruyne_goals, 'Goals', 'blue')
    p_aubameyang = plot_events(aubameyang_goals, 'Goals', 'yellow')

    #Table
    salah_stats = salah_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    salah_stats_df = pd.DataFrame(data=zip(salah_stats.index, salah_stats), columns=['match', '#goals'])
    kane_stats = kane_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    kane_stats_df = pd.DataFrame(data=zip(kane_stats.index, kane_stats), columns=['match', '#goals'])
    debruyne_stats = debruyne_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    debruyne_stats_df = pd.DataFrame(data=zip(debruyne_stats.index, debruyne_stats), columns=['match', '#goals'])
    aubameyang_stats = aubameyang_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    aubameyang_stats_df = pd.DataFrame(data=zip(aubameyang_stats.index, aubameyang_stats), columns=['match', '#goals'])
     
    #Adding Dates
    salah_stats_df = pd.merge(salah_stats_df, liverpool_matches_dates_df, on='match', copy=False, how="left")
    kane_stats_df = pd.merge(kane_stats_df, tottenham_matches_dates_df, on='match', copy=False, how="left")
    debruyne_stats_df = pd.merge(debruyne_stats_df, city_matches_dates_df, on='match', copy=False, how="left")
    aubameyang_stats_df = pd.merge(aubameyang_stats_df, arsenal_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    salah_stats_df = salah_stats_df[['date', 'match', '#goals']]
    kane_stats_df = kane_stats_df[['date', 'match', '#goals']]
    debruyne_stats_df = debruyne_stats_df[['date', 'match', '#goals']]
    aubameyang_stats_df = aubameyang_stats_df[['date', 'match', '#goals']]


    grid = bokeh.layouts.grid(
        children=[
            [p_salah, p_kane, p_debruyne, p_aubameyang],
            [print_table(salah_stats_df), print_table(kane_stats_df), print_table(debruyne_stats_df), print_table(aubameyang_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Goals")


def plot_assists(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df):

    #Getting events data positions
    salah_assists = salah_events_data_df[salah_events_data_df['assist'] == True]['positions']
    kane_assists = kane_events_data_df[kane_events_data_df['assist'] == True]['positions']
    debruyne_assists = debruyne_events_data_df[debruyne_events_data_df['assist'] == True]['positions']
    aubameyang_assists = aubameyang_events_data_df[aubameyang_events_data_df['assist'] == True]['positions']

    #Pitch with events
    p_salah = plot_events(salah_assists, 'Assists', 'red')
    p_kane = plot_events(kane_assists, 'Assists', 'pink')
    p_debruyne = plot_events(debruyne_assists, 'Assists', 'blue')
    p_aubameyang = plot_events(aubameyang_assists, 'Assists', 'yellow')

    #Table
    salah_stats = salah_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    salah_stats_df = pd.DataFrame(data=zip(salah_stats.index, salah_stats), columns=['match', '#assists'])
    kane_stats = kane_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    kane_stats_df = pd.DataFrame(data=zip(kane_stats.index, kane_stats), columns=['match', '#assists'])
    debruyne_stats = debruyne_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    debruyne_stats_df = pd.DataFrame(data=zip(debruyne_stats.index, debruyne_stats), columns=['match', '#assists'])
    aubameyang_stats = aubameyang_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    aubameyang_stats_df = pd.DataFrame(data=zip(aubameyang_stats.index, aubameyang_stats), columns=['match', '#assists'])
   
    #Adding Dates
    salah_stats_df = pd.merge(salah_stats_df, liverpool_matches_dates_df, on='match', copy=False, how="left")
    kane_stats_df = pd.merge(kane_stats_df, tottenham_matches_dates_df, on='match', copy=False, how="left")
    debruyne_stats_df = pd.merge(debruyne_stats_df, city_matches_dates_df, on='match', copy=False, how="left")
    aubameyang_stats_df = pd.merge(aubameyang_stats_df, arsenal_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    salah_stats_df = salah_stats_df[['date', 'match', '#assists']]
    kane_stats_df = kane_stats_df[['date', 'match', '#assists']]
    debruyne_stats_df = debruyne_stats_df[['date', 'match', '#assists']]
    aubameyang_stats_df = aubameyang_stats_df[['date', 'match', '#assists']]

    grid = bokeh.layouts.grid(
        children=[
            [p_salah, p_kane, p_debruyne, p_aubameyang],
            [print_table(salah_stats_df), print_table(kane_stats_df), print_table(debruyne_stats_df), print_table(aubameyang_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Assists")


def plot_shots(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df):

    #Getting events data positions
    salah_shots = salah_events_data_df[salah_events_data_df['eventName'] == 'Shot']['positions']
    kane_shots = kane_events_data_df[kane_events_data_df['eventName'] == 'Shot']['positions']
    debruyne_shots = debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Shot']['positions']
    aubameyang_shots = aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Shot']['positions']

    #Pitch with events
    p_salah = plot_events(salah_shots, 'Shots', 'red')
    p_kane = plot_events(kane_shots, 'Shots', 'pink')
    p_debruyne = plot_events(debruyne_shots, 'Shots', 'blue')
    p_aubameyang = plot_events(aubameyang_shots, 'Shots', 'yellow')

    # Table
    salah_stats = salah_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    salah_stats_df = pd.DataFrame(data=zip(salah_stats[:, 'Shot'].index, salah_stats[:, 'Shot']), columns=['match', '#shots'])
    kane_stats = kane_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    kane_stats_df = pd.DataFrame(data=zip(kane_stats[:, 'Shot'].index, kane_stats[:, 'Shot']), columns=['match', '#shots'])
    debruyne_stats = debruyne_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    debruyne_stats_df = pd.DataFrame(data=zip(debruyne_stats[:, 'Shot'].index, debruyne_stats[:, 'Shot']), columns=['match', '#shots'])
    aubameyang_stats = kane_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    aubameyang_stats_df = pd.DataFrame(data=zip(aubameyang_stats[:, 'Shot'].index, aubameyang_stats[:, 'Shot']), columns=['match', '#shots'])

    #Adding Dates
    salah_stats_df = pd.merge(salah_stats_df, liverpool_matches_dates_df, on='match', copy=False, how="left")
    kane_stats_df = pd.merge(kane_stats_df, tottenham_matches_dates_df, on='match', copy=False, how="left")
    debruyne_stats_df = pd.merge(debruyne_stats_df, city_matches_dates_df, on='match', copy=False, how="left")
    aubameyang_stats_df = pd.merge(aubameyang_stats_df, arsenal_matches_dates_df, on='match', copy=False, how="left")
    
    #Change order of columns
    salah_stats_df = salah_stats_df[['date', 'match', '#shots']]
    kane_stats_df = kane_stats_df[['date', 'match', '#shots']]
    debruyne_stats_df = debruyne_stats_df[['date', 'match', '#shots']]
    aubameyang_stats_df = aubameyang_stats_df[['date', 'match', '#shots']]

    grid = bokeh.layouts.grid(
        children=[
            [p_salah, p_kane, p_debruyne, p_aubameyang],
            [print_table(salah_stats_df), print_table(kane_stats_df), print_table(debruyne_stats_df), print_table(aubameyang_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Shots")

def plot_passes(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df):

    #Getting events data positions
    salah_passes = salah_events_data_df[salah_events_data_df['eventName'] == 'Pass']['positions']
    kane_passes = kane_events_data_df[kane_events_data_df['eventName'] == 'Pass']['positions']
    debruyne_passes = debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Pass']['positions']
    aubameyang_passes = aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Pass']['positions']

    #Pitch with events
    p_salah = plot_events(salah_passes, 'Passes', 'red')
    p_kane = plot_events(kane_passes, 'Passes', 'pink')
    p_debruyne = plot_events(debruyne_passes, 'Passes', 'blue')
    p_aubameyang = plot_events(aubameyang_passes, 'Passes', 'yellow')

    # Table
    salah_stats = salah_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    salah_stats_df = pd.DataFrame(data=zip(salah_stats[:, 'Pass'].index, salah_stats[:, 'Pass']), columns=['match', '#passes'])
    kane_stats = kane_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    kane_stats_df = pd.DataFrame(data=zip(kane_stats[:, 'Pass'].index, kane_stats[:, 'Pass']), columns=['match', '#passes'])
    debruyne_stats = debruyne_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    debruyne_stats_df = pd.DataFrame(data=zip(debruyne_stats[:, 'Pass'].index, debruyne_stats[:, 'Pass']), columns=['match', '#passes'])
    aubameyang_stats = kane_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    aubameyang_stats_df = pd.DataFrame(data=zip(aubameyang_stats[:, 'Pass'].index, aubameyang_stats[:, 'Pass']), columns=['match', '#passes'])

    #Adding Dates
    salah_stats_df = pd.merge(salah_stats_df, liverpool_matches_dates_df, on='match', copy=False, how="left")
    kane_stats_df = pd.merge(kane_stats_df, tottenham_matches_dates_df, on='match', copy=False, how="left")
    debruyne_stats_df = pd.merge(debruyne_stats_df, city_matches_dates_df, on='match', copy=False, how="left")
    aubameyang_stats_df = pd.merge(aubameyang_stats_df, arsenal_matches_dates_df, on='match', copy=False, how="left")
     #Change order of columns
    salah_stats_df = salah_stats_df[['date', 'match', '#passes']]
    kane_stats_df = kane_stats_df[['date', 'match', '#passes']]
    debruyne_stats_df = debruyne_stats_df[['date', 'match', '#passes']]
    aubameyang_stats_df = aubameyang_stats_df[['date', 'match', '#passes']]

    grid = bokeh.layouts.grid(
        children=[
            [p_salah, p_kane, p_debruyne, p_aubameyang],
            [print_table(salah_stats_df), print_table(kane_stats_df), print_table(debruyne_stats_df), print_table(aubameyang_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Passes")


if __name__ == '__main__':

    #CSS to display content correctly
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: 95%;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.write(''' ### Foot''')
    foot = st.sidebar.radio("", ('Either Left or Right', 'Left', 'Right'))
    salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df = get_data(foot)

    #Calculate Stats of both playters and structure them in a Pandas DataFrame
    goals = [salah_events_data_df['goal'].sum(), kane_events_data_df['goal'].sum(), debruyne_events_data_df['goal'].sum(), aubameyang_events_data_df['goal'].sum()]
    assists = [salah_events_data_df['assist'].sum(), kane_events_data_df['assist'].sum(), debruyne_events_data_df['assist'].sum(), aubameyang_events_data_df['assist'].sum()]
    shots = [salah_events_data_df[salah_events_data_df['eventName'] == 'Shot'].count()['eventName'],
             kane_events_data_df[kane_events_data_df['eventName'] == 'Shot'].count()['eventName'],
             debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Shot'].count()['eventName'],
             aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Shot'].count()['eventName'],
             ]
    free_kicks = [salah_events_data_df[salah_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'], 
                kane_events_data_df[kane_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'],
                debruyne_events_data_df[debruyne_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'], 
                aubameyang_events_data_df[aubameyang_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName']]
    passes = [salah_events_data_df[salah_events_data_df['eventName'] == 'Pass'].count()['eventName'],
            kane_events_data_df[kane_events_data_df['eventName'] == 'Pass'].count()['eventName'],
            debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Pass'].count()['eventName'],
            aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Pass'].count()['eventName']]

    stats_df = pd.DataFrame([goals, assists, shots, free_kicks, passes],
                            columns=['Salah', 'Kane', 'De Bruyne', 'Aubameyang'], 
                            index=['Goals', 'Assists', 'Shots', 'Free Kicks', 'Passes'])

    st.sidebar.markdown(""" ### Stats """)
    st.sidebar.dataframe(stats_df)


    tabs = bokeh.models.Tabs(
        tabs=[
            plot_goals(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df),
            plot_assists(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df),
            plot_shots(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df),
            plot_passes(salah_events_data_df, kane_events_data_df, debruyne_events_data_df, aubameyang_events_data_df, liverpool_matches_dates_df, tottenham_matches_dates_df, city_matches_dates_df, arsenal_matches_dates_df),
        ]
    )
    st.bokeh_chart(tabs)

    st.header('Salah vs Kane vs De Bruyne vs Aubameyang')