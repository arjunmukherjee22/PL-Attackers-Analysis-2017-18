import json
import numpy as np
import pandas as pd
import unicodedata
import streamlit as st
import Pl_Attackers_App
import bokeh
from bokeh.io import output_notebook
from bokeh.plotting import figure, show

with open('./data/players.json') as json_file:
    player_id_data = json.load(json_file)
    

salah_info = [player for player in player_id_data if 'Salah' in player['shortName']]
salah_player_id = salah_info[0]['wyId']
print(f'The player id of Salah is : {salah_player_id}')

kane_info = [player for player in player_id_data if 'Kane' in player['shortName']]
kane_player_id = kane_info[0]['wyId']
print(f'The player id of Kane is : {kane_player_id}')

debruyne_info = [player for player in player_id_data if 'De Bruyne' in player['shortName']]
debruyne_player_id = debruyne_info[0]['wyId']
print(f'The player id of De Bruyne is : {debruyne_player_id}')

aubameyang_info = [player for player in player_id_data if 'Aubameyang' in player['shortName']]
aubameyang_player_id = aubameyang_info[0]['wyId']
print(f'The player id of Aubameyang is : {aubameyang_player_id}')

with open('./data/teams.json') as json_file:
    team_id_data = json.load(json_file)
    
eng_teams_data = [teams for teams in team_id_data if 'England' in teams['area']['name']]

liv_team = [team for team in eng_teams_data if 'Liverpool' in team['officialName']]
liv_team_id = liv_team[0]['wyId']
print(f'Liverpool team id is {liv_team_id}')

tot_team = [team for team in eng_teams_data if 'Tottenham' in team['officialName']]
tot_team_id = tot_team[0]['wyId']
print(f'Tottenham team id is {tot_team_id}')

city_team = [team for team in eng_teams_data if 'Manchester City' in team['officialName']]
city_team_id = city_team[0]['wyId']
print(f'Manchester City team id is {city_team_id}')

arsenal_team = [team for team in eng_teams_data if 'Arsenal' in team['officialName']]
arsenal_team_id = arsenal_team[0]['wyId']
print(f'Arsenal team id is {arsenal_team_id}')

with open('./data/matches/matches_England.json') as json_file:
    matches_england_data = json.load(json_file)
    
with open('./data/events/events_England.json') as json_file:
    events_england_data = json.load(json_file)

liverpool_matches = [match for match in matches_england_data if '1612' in match['teamsData'].keys()]
tottenham_matches = [match for match in matches_england_data if '1624' in match['teamsData'].keys()]
city_matches = [match for match in matches_england_data if '1625' in match['teamsData'].keys()]
arsenal_matches = [match for match in matches_england_data if '1609' in match['teamsData'].keys()]

liverpool_matches_df = pd.DataFrame(liverpool_matches)
tottenham_matches_df = pd.DataFrame(tottenham_matches)
city_matches_df = pd.DataFrame(city_matches)
arsenal_matches_df = pd.DataFrame(arsenal_matches)

arsenal_matches_df.head(3)

salah_events_data = []
for event in events_england_data:
    if event['playerId'] == 120353:
        salah_events_data.append(event)
        
kane_events_data = []
for event in events_england_data:
    if event['playerId'] == 8717:
        kane_events_data.append(event)
        
debruyne_events_data = []
for event in events_england_data:
    if event['playerId'] == 38021:
        debruyne_events_data.append(event)
        
aubameyang_events_data = []
for event in events_england_data:
    if event['playerId'] == 25867:
        aubameyang_events_data.append(event)
        
salah_events_data_df = pd.DataFrame(salah_events_data)
kane_events_data_df = pd.DataFrame(kane_events_data)
debruyne_events_data_df = pd.DataFrame(debruyne_events_data)
aubameyang_events_data_df = pd.DataFrame(aubameyang_events_data)

aubameyang_events_data_df.head(3)

def add_event_tag(tags, tag_id):
    return tag_id in [tag['id'] for tag in tags]

salah_events_data_df['goal'] = salah_events_data_df['tags'].apply(lambda x: add_event_tag(x,101))
salah_events_data_df['assist'] = salah_events_data_df['tags'].apply(lambda x: add_event_tag(x,301))
salah_events_data_df['key_pass'] = salah_events_data_df['tags'].apply(lambda x: add_event_tag(x,302))
salah_events_data_df['left_foot'] = salah_events_data_df['tags'].apply(lambda x: add_event_tag(x,401))
salah_events_data_df['right_foot'] = salah_events_data_df['tags'].apply(lambda x: add_event_tag(x,402))

kane_events_data_df['goal'] = kane_events_data_df['tags'].apply(lambda x: add_event_tag(x,101))
kane_events_data_df['assist'] = kane_events_data_df['tags'].apply(lambda x: add_event_tag(x,301))
kane_events_data_df['key_pass'] = kane_events_data_df['tags'].apply(lambda x: add_event_tag(x,302))
kane_events_data_df['left_foot'] = kane_events_data_df['tags'].apply(lambda x: add_event_tag(x,401))
kane_events_data_df['right_foot'] = kane_events_data_df['tags'].apply(lambda x: add_event_tag(x,402))

debruyne_events_data_df['goal'] = debruyne_events_data_df['tags'].apply(lambda x: add_event_tag(x,101))
debruyne_events_data_df['assist'] = debruyne_events_data_df['tags'].apply(lambda x: add_event_tag(x,301))
debruyne_events_data_df['key_pass'] = debruyne_events_data_df['tags'].apply(lambda x: add_event_tag(x,302))
debruyne_events_data_df['left_foot'] = debruyne_events_data_df['tags'].apply(lambda x: add_event_tag(x,401))
debruyne_events_data_df['right_foot'] = debruyne_events_data_df['tags'].apply(lambda x: add_event_tag(x,402))

aubameyang_events_data_df['goal'] = aubameyang_events_data_df['tags'].apply(lambda x: add_event_tag(x,101))
aubameyang_events_data_df['assist'] = aubameyang_events_data_df['tags'].apply(lambda x: add_event_tag(x,301))
aubameyang_events_data_df['key_pass'] = aubameyang_events_data_df['tags'].apply(lambda x: add_event_tag(x,302))
aubameyang_events_data_df['left_foot'] = aubameyang_events_data_df['tags'].apply(lambda x: add_event_tag(x,401))
aubameyang_events_data_df['right_foot'] = aubameyang_events_data_df['tags'].apply(lambda x: add_event_tag(x,402))

aubameyang_events_data_df.head(3)
                                                                  
salah_events_data_df = pd.merge(salah_events_data_df, liverpool_matches_df, left_on='matchId', right_on='wyId', copy=False, how='left')

kane_events_data_df = pd.merge(kane_events_data_df, tottenham_matches_df, left_on='matchId', right_on='wyId', copy=False, how='left')

debruyne_events_data_df = pd.merge(debruyne_events_data_df, city_matches_df, left_on='matchId', right_on='wyId', copy=False, how='left')

aubameyang_events_data_df = pd.merge(aubameyang_events_data_df, arsenal_matches_df, left_on='matchId', right_on='wyId', copy=False, how='left')

liverpool_matches_played_df = liverpool_matches_df[['date', 'label']].copy()
tottenham_matches_played_df = tottenham_matches_df[['date', 'label']].copy()
city_matches_played_df = city_matches_df[['date', 'label']].copy()
arsenal_matches_played_df = arsenal_matches_df[['date', 'label']].copy()

# convert date to utc 
liverpool_matches_played_df['date'] = (pd.to_datetime(liverpool_matches_df['date'], utc = True).dt.date)
liverpool_matches_played_df['date'] = liverpool_matches_played_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
tottenham_matches_played_df['date'] = (pd.to_datetime(tottenham_matches_df['date'], utc = True).dt.date)
tottenham_matches_played_df['date'] = tottenham_matches_played_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
city_matches_played_df['date'] = (pd.to_datetime(city_matches_df['date'], utc = True).dt.date)
city_matches_played_df['date'] = city_matches_played_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
arsenal_matches_played_df['date'] = (pd.to_datetime(arsenal_matches_df['date'], utc = True).dt.date)
arsenal_matches_played_df['date'] = arsenal_matches_played_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

liverpool_matches_played_df = liverpool_matches_played_df.rename(columns={"label": "match"})
tottenham_matches_played_df = tottenham_matches_played_df.rename(columns={"label": "match"})
city_matches_played_df = city_matches_played_df.rename(columns={"label": "match"})
arsenal_matches_played_df = arsenal_matches_played_df.rename(columns={"label": "match"})

salah_lf_goals = salah_events_data_df[salah_events_data_df['left_foot'] == True]['goal'].sum()
salah_rf_goals = salah_events_data_df[salah_events_data_df['right_foot'] == True]['goal'].sum()
salah_assist = salah_events_data_df[salah_events_data_df['assist'] == True]['assist'].sum()
print(f"Goal scored by Salah with the left foot: {salah_lf_goals}")
print(f"Goal scored by Salah with the right foot: {salah_rf_goals}")
print(f"Assists by Salah: {salah_assist}")
print('--------------------------------------------')

kane_lf_goals = kane_events_data_df[kane_events_data_df['left_foot'] == True]['goal'].sum()
kane_rf_goals = kane_events_data_df[kane_events_data_df['right_foot'] == True]['goal'].sum()
kane_assist = kane_events_data_df[kane_events_data_df['assist'] == True]['assist'].sum()
print(f"Goal scored by Kane with the left foot: {kane_lf_goals}")
print(f"Goal scored by Kane with the right foot: {kane_rf_goals}")
print(f"Assists by Kane: {kane_assist}")
print('--------------------------------------------')

debruyne_lf_goals = debruyne_events_data_df[debruyne_events_data_df['left_foot'] == True]['goal'].sum()
debruyne_rf_goals = debruyne_events_data_df[debruyne_events_data_df['right_foot'] == True]['goal'].sum()
debruyne_assist = debruyne_events_data_df[debruyne_events_data_df['assist'] == True]['assist'].sum()
print(f"Goal scored by De Bruyne with the left foot: {debruyne_lf_goals}")
print(f"Goal scored by De Bruyne with the right foot: {debruyne_rf_goals}")
print(f"Assists by De Bruyne: {debruyne_assist}")
print('--------------------------------------------')

aubameyang_lf_goals = aubameyang_events_data_df[aubameyang_events_data_df['left_foot'] == True]['goal'].sum()
aubameyang_rf_goals = aubameyang_events_data_df[aubameyang_events_data_df['right_foot'] == True]['goal'].sum()
aubameyang_assist = aubameyang_events_data_df[aubameyang_events_data_df['assist'] == True]['assist'].sum()
print(f"Goal scored by Aubameyang with the left foot: {aubameyang_lf_goals}")
print(f"Goal scored by Aubameyang with the right foot: {aubameyang_rf_goals}")
print(f"Assists by Aubameyang: {aubameyang_assist}")

goals = [salah_events_data_df['goal'].sum(), kane_events_data_df['goal'].sum(), debruyne_events_data_df['goal'].sum(), aubameyang_events_data_df['goal'].sum()]
assists = [salah_events_data_df['assist'].sum(), kane_events_data_df['assist'].sum(), debruyne_events_data_df['assist'].sum(), aubameyang_events_data_df['assist'].sum()]
passes = [salah_events_data_df[salah_events_data_df['eventName'] == 'Pass'].count()['eventName'],
          kane_events_data_df[kane_events_data_df['eventName'] == 'Pass'].count()['eventName'],
          debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Pass'].count()['eventName'], 
          aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Pass'].count()['eventName']]
shots = [salah_events_data_df[salah_events_data_df['eventName'] == 'Shot'].count()['eventName'],
          kane_events_data_df[kane_events_data_df['eventName'] == 'Shot'].count()['eventName'],
          debruyne_events_data_df[debruyne_events_data_df['eventName'] == 'Shot'].count()['eventName'], 
          aubameyang_events_data_df[aubameyang_events_data_df['eventName'] == 'Shot'].count()['eventName']]
free_kicks = [salah_events_data_df[salah_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'],
          kane_events_data_df[kane_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'],
          debruyne_events_data_df[debruyne_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'], 
          aubameyang_events_data_df[aubameyang_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName']]

stats_df = pd.DataFrame([goals, assists, passes, shots, free_kicks], columns = ['Salah', 'Kane', 'De Bruyne', 'Aubameyang'], index = ['Goals', 'Assists', 'Passes', 'Shots', 'Free Kicks'])

salah_events_data_df.to_pickle('./data/salah_events_data_df.pkl')
kane_events_data_df.to_pickle('./data/kane_events_data_df.pkl')
debruyne_events_data_df.to_pickle('./data/debruyne_events_data_df.pkl')
aubameyang_events_data_df.to_pickle('./data/aubameyang_events_data_df.pkl')

liverpool_matches_played_df.to_pickle('./data/liverpool_matches_played_df.pkl')
tottenham_matches_played_df.to_pickle('./data/tottenham_matches_played_df.pkl')
city_matches_played_df.to_pickle('./data/city_matches_played_df.pkl')
arsenal_matches_played_df.to_pickle('./data/arsenal_matches_played_df.pkl')

