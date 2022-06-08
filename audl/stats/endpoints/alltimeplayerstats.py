#!/usr/bin/env/python

import pandas as pd
import json 
import requests
import sys

from audl.stats.endpoints._base import Endpoint
from audl.stats.library.parameters import FileName
from audl.stats.library.utils import download_dataframe


class AllTimePlayerStats(Endpoint):

    def __init__(self):
        #  super().__init__("https://theaudl.com/stats/players-all-time?page=")
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20&page=")

    def _get_all_time_player_stats_df(self, show_message=True):
        """
        Function that fetch all time stats for all players as dataframe
        return [df] dataframe of all players stats
        """
        hasPlayerLeft = True
        all_players = []
        #  page = 1
        page = 146
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
        [deprecated] Function that return the url by concatening the base url with its page number
        """
        return f"{self.base_url}{page_num}"

    def _fetch_page_players_as_json(self, page_num):
        """
        [deprecated] 
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


    def download_all_time_player_stats(self, show_message=True):
        """ 
        [deprecated] 
        Function that download all time players stats as csv file
        return [flag] True if successfully downloaded, else False
        """
        df = self._get_all_time_player_stats_df(show_message)
        file_name = f"{FileName.alltimeplayer}.csv"
        flag = False
        try:
            df.to_csv(file_name, sep=',', index=False)
            print(f'Downloaded csv file at {file_name}')
            flag = True
        except: 
            print('An error has occured when saving the file as csv')
        return flag 


