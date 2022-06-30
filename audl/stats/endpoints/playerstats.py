#!/usr/bin/env/python

import pandas as pd
import json 
import requests
import sys

from audl.stats.endpoints._base import Endpoint
from audl.stats.library.parameters import FileName


class PlayerStats(Endpoint):
    """ class that download data from https://theaudl.com/stats/player-stats
        based on [Season], [Per], [Team]
    """

#  https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20&year=2019&per=possessions&team=aviators
#  https://theaudl.com/stats/player-stats?page=2&per=possessions&team=aviators&year=2019

    def __init__(self, season, per, team):
        self.season = season
        self.per = per
        self.team = team
        super().__init__('https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20')

    def fetch_table(self, show_message=True):
        """
        Function that fetch query for all players as dataframe
        return [df] dataframe of all players stats
        """
        hasPlayerLeft = True
        all_players = []
        page = 1
        # add all players 
        while(hasPlayerLeft):
            players = self._fetch_page_players_as_json(page)
            print(page)
            if not players:
                break
            all_players = all_players + players     # concatenating
            page = page + 1

        # turn json as dataframe
        df = pd.DataFrame(all_players)

        return df.drop_duplicates()


    def _get_url(self, page_num: int) -> str:
        """ 
        Function that return the url by concatening the base url with its page number
        """
        if self.season == 'career' and self.team == 'all':
            return f"{self.base_url}&page={page_num}&per={self.per}"
        elif self.season == 'career':
            return f"{self.base_url}&page={page_num}&per={self.per}&team={self.team}"
        elif self.team == 'all':
            return f"{self.base_url}&page={page_num}&year={self.season}&per={self.per}"
        return f"{self.base_url}&page={page_num}&year={self.season}&per={self.per}&team={self.team}"

    def _fetch_page_players_as_json(self, page_num):
        """
        Function that fetch players in page as json 
        param: [page_num] url page number
        return:  result_json] players as json
        """
        try:
            url = self._get_url(page_num)
            page = requests.get(url)
            results = page.json()
            players = results['stats']
        except: 
            print(f'An error has occured when fetching the data from {url}')
            sys.exit(1)
            
        return players


    # TODO: create Download class
    def download_stats_as_dataframe(self, file_path_name, show_message=True):
        """ 
        Function that download players stats as csv file
        param [file_path_name] output file name     *.csv
        return [flag] True if successfully downloaded, else False
        """
        flag = False
        try:
            df = self.fetch_table()
            df.to_csv(file_path_name, sep=',', index=False)
            print(f'Downloaded csv file at {file_path_name}')
            flag = True
        except: 
            print('An error has occured when saving the file as csv')
        return flag 


