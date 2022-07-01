#!/usr/bin/env/python

import json
import pandas as pd
import numpy as np
import requests

from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players
from audl.stats.library.parameters import quarters_clock_dict
from audl.stats.library.parameters import HerokuPlay
from audl.stats.library.parameters import team_roster_columns_name

#  https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TOR-MTL


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://audl-stat-server.herokuapp.com/stats-pages/game/")
        self.game_id = game_id
        self.json = self._get_json_from_url()

    def _get_url(self):
        return f"{self.base_url}{self.game_id}"
    

    def _get_json_from_url(self):
        url = self._get_url()
        return requests.get(url).json()

    def get_metadata(self):
        """ 
        Function that retrieve game metadata
        Return [df]:
            - is_regular_season (bool)
            - home_team, away_team
            - home_score, away_score
            - stadium_name (from location_id)
        """
        pass

    def get_boxscores(self):
        """ 
        Function that return team scores by quarter
        Ex:
                            Q1	Q2	Q3	Q4	T
            Toronto Rush	4	6	4	7	21
            Montreal Royal	4	7	4	5	20
        """

        pass
        
    def get_team_stats(self):
        pass


    def get_scores(self):
        """ 
        Function that retrieves scores by times
        Return [df]:
            - team: "home" or "away"
            - time: time when the team scored
            - goal: who scored the goal
            - assist: who assisted the goal
            - hockey: who made the hockey pass
        """
        pass

    def get_players_metadata(self):
        """ 
        Function that retrieves players data
        Return [df] from json.rostersHome and json.rostersAway
            - player_game_id: id used in events
            - jersey_number
            - player_id
            - first_name:
            - last_name
            - ext_player_id: 'pbisson'
            - ext_team_id: 'royal'
            - city
        """
        # get home and away roster
        homeJSON = self.json['rostersHome']
        home_players = pd.json_normalize(homeJSON)
        home_players['road'] = 'home'
        awayJSON = self.json['rostersAway']
        away_players = pd.json_normalize(awayJSON)
        away_players['road'] = 'away'

        # concatenate dataset
        teams = pd.concat([home_players, away_players])
        return teams



    def get_teams_metadata(self):
        """ 
        Function that retrieve team and city name for home and away team
        Return [df] from games.team_season_home games.team_season_away
            - team_season_id
            - team_id
            - city: 'Monteal'
            - city_abbrev: 'MTL'
            - name: 'Royal'
            - ext_team_id: 'royal'
            - stadium? TODO
        """
        # retrieve df from home and away team
        game = self.json['game']
        home = pd.json_normalize(game['team_season_home'])
        away = pd.json_normalize(game['team_season_away'])
        home['road'] = 'home'
        away['road'] = 'away'

        # concatenate home and away dataframes
        teams = pd.concat([home, away])
        return teams
        

