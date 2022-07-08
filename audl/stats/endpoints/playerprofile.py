#!/usr/bin/env/python

import pandas as pd
import requests 
import sys

from datetime import datetime

from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players
from audl.stats.static.miscellaneous import FIRST_SEASON_YEAR

#  https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=cbrock
#  https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID=cbrock&year=2022


class PlayerProfile(Endpoint):

    def __init__(self, player_id: str):
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=")
        self.player_id = player_id


    def _get_url(self):
        """ 
        Function that return complete url

        Returns
        -------
        url: string
            url of the heroku API request
        
        Examples
        --------
        >>> PlayerProfile('cbrock')._get_url()

        """
        return f"{self.base_url}{self.player_id}"

    def get_regular_seasons_career(self):
        """ 
        Function that return a player's regular season stats as dataframe

        Returns
        -------
        regular_season: pandas.DataFrame
            dataframe with player regular season stats
            

        Examples
        --------
        >>> PlayerProfile('cbrock').get_regular_seasons_career()

        """
        try: 
            # create dataframe
            url = self._get_url()
            results = requests.get(url).json()
            df = pd.DataFrame(results['stats'])

            #  sort by regSeason
            regular_season = df[df['regSeason'] == True]

            # drop regSeason column
            #  regular_season = regular_season.drop(columns=['regSeason'], axis=1)

            return regular_season
        except: 
            print(f'An error has occured when fetching regular season dataframe')
            sys.exit(1)


    def get_playoffs_career(self):
        """ 
        Function that returns a player's playoff stats as dataframe

        Returns
        -------
        playoffs: pandas.DataFrame
            dataframe with player playoffs stats
            

        Examples
        --------
        >>> PlayerProfile('cbrock').get_playoffs_career()

        """
        try: 
            # create dataframe
            url = self._get_url()
            results = requests.get(url).json()
            df = pd.DataFrame(results['stats'])

            #  sort by regSeason
            playoffs = df[df['regSeason'] == False]

            # drop regSeason column
            #  playoffs = playoffs.drop(columns=['regSeason'], axis=1)

            return playoffs 
        except: 
            print(f'An error has occured when fetching playoffs dataframe')
            sys.exit(1)

    def get_season_games_stats(self, year):
        """ 
        Function that returns stats per game in a given season

        Parameters
        ----------
        year: int
            season

        Returns
        -------
        season_games: pandas.DataFrame


        Examples
        --------
        >>> PlayerProfile('cbrock').get_season_games_stats(2022)

        """
        try:
            url = f"https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID={self.player_id}&year={year}"
            results = requests.get(url).json()
            df = pd.DataFrame(results['stats'])
            return df
        except:
            print(f'An error has occured when fetching season stats dataframe')
            sys.exit(1)

    def get_career_games_stats(self):
        """ 
        Function that return dataframe of all games played by a player

        Returns
        -------
        career_games: pandas.DataFrame
            dataframe with all games played

        Examples
        --------
        >>> PlayerProfile('cbrock').get_career_games_stats()

        """
        df = pd.DataFrame()
        current_year = int(datetime.today().strftime('%Y'))
        for year in range(FIRST_SEASON_YEAR, current_year +1):
            df_season = self.get_season_games_stats(year)
            df = df.append(df_season)
        return df

        
        
        

