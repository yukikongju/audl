#!/usr/bin/env/python

import pandas as pd
import requests 
import sys

from datetime import datetime

from audl.stats.endpoints._base import Endpoint
from audl.stats.static.constants import FIRST_SEASON_YEAR

#  old: https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=cbrock
#  old: https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID=cbrock&year=2022

#  new: https://www.backend.audlstats.com/web-api/roster-stats-for-player?playerID=abartlett
#  new: https://www.backend.audlstats.com/web-api/roster-game-stats-for-player?playerID=wbrandt&year=2022



class PlayerProfile(Endpoint):

    def __init__(self, player_id: str):
        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=")
        super().__init__("https://www.backend.audlstats.com/web-api/roster-stats-for-player?playerID=")
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

    def get_career_stats(self):
        """ 
        Function that return player regular and playoffs stats as a dataframe

        Returns
        -------
        career_stats: pandas.DataFrame
            dataframe with player regular and playoffs season stats

        Examples
        --------
        >>> PlayerProfile('cbrock').get_career_stats()
        """
        try: 
            # create dataframe
            url = self._get_url()
            results = requests.get(url).json()
            df = pd.DataFrame(results['stats'])
            return df
        except:
            print(f'An error has occured when fetching regular season dataframe')
            sys.exit(1)


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
        df = self.get_career_stats()
        df['player_ext_id'] = self.player_id
        regular_season = df[df['regSeason'] == True]
        return regular_season


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
        df = self.get_career_stats()
        playoffs = df[df['regSeason'] == True]
        return playoffs 

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
            #  url = f"https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID={self.player_id}&year={year}"
            url = f"https://www.backend.audlstats.com/web-api/roster-game-stats-for-player?playerID={self.player_id}&year={year}"
            results = requests.get(url).json()
            df = pd.DataFrame(results['stats'])
            df['player_ext_id'] = self.player_id
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
        df['player_ext_id'] = self.player_id
        return df

#  ------------------------------------------------------------------------


def main():
    #  player = PlayerProfile('bbergmeie')
    player = PlayerProfile('wbrandt')

    #  print(player.get_career_games_stats())
    print(player.get_career_stats())
    #  print(player.get_playoffs_career())
    #  print(player.get_regular_seasons_career())
    #  print(player.get_season_games_stats(2022))
    

if __name__ == "__main__":
    main()
