#!/usr/bin/env/python

import sys
import pandas as pd
import requests
from audl.stats.endpoints._base import Endpoint


#  https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50&year=2019&perGame=true&opponent=true

class TeamStats(Endpoint):

    def __init__(self, season, per, team):
        #  super().__init__("https://theaudl.com/stats/team?year=")
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50")
        self.season = season
        self.per = per
        self.team = team

    def get_table(self):
        """
        Function that return page results table as dataframe
        return [df] dataframe
        """
        try:
            url = self._get_url()
            results = requests.get(url).json()
            teams = results['stats']
            df = pd.DataFrame(teams)
        except:
            print(f'An error has occured when fetching the page results as dataframe')
            sys.exit(1)

        return df


    def _get_url(self):
        is_per_game = 'true' if self.per == 'game' else 'false' 
        is_opponent = 'true' if self.team == 'opponent' else 'false'
        if self.season == 'career':
            return f"https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50&perGame={is_per_game}&opponent={is_opponent}"
        else: 
            return f"https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50&year={self.season}&perGame={is_per_game}&opponent={is_opponent}"

        



