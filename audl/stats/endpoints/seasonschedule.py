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



class ScheduleEndpoint(Endpoint):

    def __init__(self):
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/games?limit=10")

    def _get_prefix_url(self):
        pass

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


    def get_schedule(self):
        """ 
        Fetch schedule
        """
        prefix_url = self._get_prefix_url()
        df = self._fetch_data_from_url(prefix_url)
        return df



class AllSchedule(ScheduleEndpoint):

    def __init__(self):
        super().__init__()

    def _get_prefix_url(self):
        return self.base_url


class SeasonSchedule(ScheduleEndpoint):

    def __init__(self, season):
        super().__init__()
        self.season = season

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}"


class TeamSeasonSchedule(ScheduleEndpoint):

    def __init__(self, season, team):
        super().__init__()
        self.season = season
        self.team = team

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}&teamID={self.team}"

class TeamSeasonAgainstOpponentSchedule(ScheduleEndpoint):

    def __init__(self, season, team, opponent):
        super().__init__()
        self.season = season
        self.team = team
        self.opponent = opponent

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}&teamID={self.team}&opposingTeamID={self.opponent}"

