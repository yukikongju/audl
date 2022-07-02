#!/usr/bin/env/python

import json
import pandas as pd
import numpy as np
import requests

from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players
from audl.stats.endpoints.playerprofile import PlayerProfile


from audl.stats.library.parameters import quarters_clock_dict
from audl.stats.library.parameters import HerokuPlay
from audl.stats.library.parameters import team_roster_columns_name

#  https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TOR-MTL


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://audl-stat-server.herokuapp.com/stats-pages/game/")
        self.game_id = game_id
        self.json = self._get_json_from_url()
        self.home_team = self._get_home_team()
        self.away_team = self._get_away_team()

    def _get_home_team(self):
        return self.json['game']['team_season_home']['team']['ext_team_id']
        
    def _get_away_team(self):
        return self.json['game']['team_season_away']['team']['ext_team_id']
        pass

    def _get_url(self):
        return f"{self.base_url}{self.game_id}"
    

    def _get_json_from_url(self):
        url = self._get_url()
        return requests.get(url).json()

    def get_game_metadata(self):
        """ 
        Function that retrieve game metadata
        Return [df]:
            - is_regular_season (bool)
            - home_team, away_team
            - home_score, away_score
            - stadium_name (from location_id)
        """
        game = self.json['game']
        df = pd.json_normalize(game)
        return df

    def get_boxscores(self):
        """ 
        Function that return team scores by quarter
        Ex:
                            Q1	Q2	Q3	Q4	T
            Toronto Rush	4	6	4	7	21
            Montreal Royal	4	7	4	5	20
        """
        pass

    def _get_scoring_time(self):
        """ 
        Function that return scoring time for each team
        Ex: 
                    scoring_time    quarter
            TOR
            MTL
        """
        pass
        
    def get_scores(self): # todo in sql?
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

    def get_roster_stats(self):
        """ 
        Function that retrieves stats for all players that played this games
        return [df]
        """
        # get external ids for all players that played
        roster_ext_ids = self._get_roster_ext_ids()

        roster_stats = pd.DataFrame()
        for player_id in roster_ext_ids:
            # get all games played in game's season
            player = PlayerProfile(player_id)
            year = self._get_season_from_game_id()
            games = player.get_season_games_stats(year)

            # filter by gameID and add player_id, city_id
            player_stat = games[games['gameID'] == self.game_id]
            player_stat['ext_player_id'] = player_id
            # FIXME: use .iloc instead #  is_home = player_stat.at[0,'isHome']
            is_home = player_stat['isHome'].values[0]
            player_stat['team_abbrev'] = self._get_city_abbrev_from_game_id(is_home)

            roster_stats = pd.concat([roster_stats, player_stat])

        # change columns order
        roster_stats.insert(0, 'ext_player_id', roster_stats.pop('ext_player_id'))
        roster_stats.insert(1, 'team_abbrev', roster_stats.pop('team_abbrev'))

        return roster_stats

    def _get_city_abbrev_from_game_id(self, is_home):
        """ 
        Function that return season from game_id
            ex: "2022-05-28-IND-DET" return IND if is_home = True, DET if is_home=False
        param: 
            - is_home (bool): True if home, False if away
        return:
            - season (int): year  ex: 2022
        """
        if is_home:
            return self.game_id.split('-')[4]
        else:
            return self.game_id.split('-')[3]
        


    def _get_season_from_game_id(self):
        """ 
        Function that return season from game_id
            ex: "2022-05-28-IND-DET" return 2022
        return:
            - season (int): year  ex: 2022
        """
        return self.game_id.split('-')[0]


        
    def _get_roster_ext_ids(self):
        """ 
        Function that return all players that played this game (rosterIds)
        Return [list] ext_player_id
            ex: ['pbisson', 'thodge']
        """
        # get all player_id who have played as list
        rosterHome = self.json['tsgHome']['rosterIds']
        rosterAway= self.json['tsgAway']['rosterIds']
        roster_ids = rosterHome + rosterAway

        # get player_ext_ids
        players = self.get_players_metadata()
        roster_df = players[players['id'].isin(roster_ids)]
        ext_player_ids = roster_df['player.ext_player_id'].tolist()

        return ext_player_ids


    def get_team_stats(self):
        """ 
        Function that retrieves teams stats
        Return [df]:
           'id', 'teamSeasonId', 'gameId', 'source', 'startOnOffense',
           'updateMoment', 'statusId', 'completionsNumer', 'completionsDenom',
           'hucksNumer', 'hucksDenom', 'blocks', 'turnovers', 'oLineScores',
           'oLinePoints', 'oLinePossessions', 'dLineScores', 'dLinePoints',
           'dLinePossessions', 'redZoneScores', 'redZonePossessions', 'road',
           'completionsPerc', 'hucksPerc', 'holdPerc', 'oLineConversionPerc',
           'dLineConversionPerc', 'breakPerc', 'redZoneConversionPerc'
        """
        tsg_home = self._read_teams_tsg_json(self.json['tsgHome'])
        tsg_home['road'] = 'home'
        tsg_home['team'] = self.home_team
        tsg_away = self._read_teams_tsg_json(self.json['tsgAway'])
        tsg_away['road'] = 'away'
        # concatenate home and away dataframes
        tsg = pd.concat([tsg_home, tsg_away])

        # calculate percentage columns
        tsg['completionsPerc'] = tsg['completionsNumer'] / tsg['completionsDenom'] 
        tsg['hucksPerc'] = tsg['hucksNumer'] / tsg['hucksDenom'] 
        tsg['holdPerc'] = tsg['oLineScores'] / tsg['oLinePoints'] 
        tsg['oLineConversionPerc'] = tsg['oLineScores'] / tsg['oLinePossessions'] 
        tsg['dLineConversionPerc'] = tsg['dLineScores'] / tsg['dLinePossessions'] 
        tsg['breakPerc'] = tsg['dLineScores'] / tsg['dLinePoints'] 
        tsg['redZoneConversionPerc'] = tsg['redZoneScores'] / tsg['redZonePossessions'] 

        return tsg



    def _read_teams_tsg_json(self, team_tsg):
        """ 
        Function that retrieves scoring information in json.tsgHome and 
            json.tsgAway
        param:
            - team_tsg: json dictionary ie json.tsgHome 
        Return [df]:
            
        """
        # read json
        tsg = pd.json_normalize(team_tsg, max_level=1)

        # drop columns
        cols_to_drop = [
                'events', 
                'scoreTimesOur',
                'scoreTimesTheir',
                'rosterIds'
            ]
        tsg = tsg.drop(cols_to_drop, axis=1)

        return tsg


    def get_players_metadata(self):
        """ 
        Function that retrieves all players from both team (even those who 
        are not playing)
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
        home_players['team'] = self.home_team
        awayJSON = self.json['rostersAway']
        away_players = pd.json_normalize(awayJSON)
        away_players['road'] = 'away'
        away_players['team'] = self.away_team

        # concatenate dataset
        players = pd.concat([home_players, away_players])
        return players 

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
        
    def get_teams_events(self):
        """ 
        Function that retrieves events for home and away teams
        return [df]
        """
        pass
        #  home_events = json.loads(self.json['tsgHome']['events'])
        #  df = pd.json_normalize(home_events, max_level=1)

        #  # FIXME: convert columns double values to int
        #  cols_to_int = ['t', 'ms', 's', 'c', 'q']
        #  for col in cols_to_int:
        #      df[col] = df[col].astype('int', errors='ignore')

        #  # rename columns
        #  col_names_dict = {
        #          "t": "type",
        #          "l": "lineup",
        #          "r": "receiver",
        #          "x": "x",
        #          "y": "y",
        #          "ms": "ms",
        #          "s": "s",
        #          "c": "c",
        #          "q": "q",
        #          }
        #  new_col_names = [col_names_dict.get(col) for col in df.columns.tolist()]
        #  df.columns = new_col_names

        #  # get players_metadata
        #  players = self.get_players_metadata()
        #  players = players[['id', 'player.first_name', 'player.last_name']]
        #  print(players)


        #  # get type = 3
        #  tmp = df[df['type'] == 3].copy()

        #  #  tmp['receiver'] = tmp['receiver'].apply(lambda x: int(x) if not pd.isna(x) else 'NaN')
        #  tmp['receiver'] = tmp['receiver'].apply(lambda x: players[players['id'] == int(x)] if not pd.isna(x) else 'NaN')
        #  print(tmp)

        

