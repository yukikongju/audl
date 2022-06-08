#!/usr/bin/env/python

import pandas as pd
import requests
import json 
import sys

from bs4 import BeautifulSoup

from audl.stats.endpoints._base import Endpoint
from audl.stats.library.parameters import game_schedule_columns_name
from audl.stats.library.parameters import FileName

#  https://audl-stat-server.herokuapp.com/web-api/games?limit=10&years=2022&teamID=alleycats

class SeasonSchedule(Endpoint):

    def __init__(self):
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/games?limit=10")

    def _get_url(self, season, team, opponent):
        if team == None and season == None and opponent == None: # get_all_games_ever_played()
            return self.base_url
        elif opponent == None and team == None: # get_season_schedule()
            return f"{self.base_url}&years={season}"
        elif opponent == None: # get_team_season_schedule()
            return f"{self.base_url}&years={season}&teamID={team}"
        else: # get_team_season_schedule_against_opponent()
            return f"{self.base_url}&years={season}&teamID={team}&opposingTeamID={opponent}"


    def _fetch_data_from_url(self, prefix_url):
        i = 1
        has_games = True
        dfs = pd.DataFrame()
        while(has_games):
            url = f"{prefix_url}&page={i}"
            print(url)
            try:
                page = requests.get(url)
            except:
                print(f'An error occured when fetching the data. Exiting...')
                sys.exit(1)
            results = page.json()
            games = results['games']
            df = pd.json_normalize(games)
            if df.size == 0:
                has_games = False
            i = i + 1 
            dfs = dfs.append(df)
        return dfs
        
    def get_all_games_ever_played(self):
        """ 
        Fetch all games played ever
        return [df]
        """
        url = self._get_url(None, None, None)
        df = self._fetch_data_from_url(url)
        return df


    def get_season_schedule(self, season):
        """ 
        Fetch all games played in a season (all teams)
        param [season]
        return [df]
        """
        url = self._get_url(season, None, None)
        df = self._fetch_data_from_url(url)
        return df

    def get_team_season_schedule(self, team, season):
        """ 
        Fetch all games played by a team in a given season
        param [team] : team_id
        param [season]: year 
        return [df]
        """
        url = self._get_url(season, team, None)
        df = self._fetch_data_from_url(url)
        return df

    def get_team_season_schedule_against_opponent(self, season, team, opponent):
        """ 
        Fetch all games played by a team against opponent in a given season
        param [team] : team_id
        param [season]: year 
        param [opponent]: opponent
        return [df]
        """
        url = self._get_url(season, team, opponent)
        df = self._fetch_data_from_url(url)
        return df


