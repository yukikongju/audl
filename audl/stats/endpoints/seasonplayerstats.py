#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.endpoints.teamseasonplayerstats import TeamSeasonPlayerStats
from audl.stats.static.miscellaneous import get_season_id
from audl.stats.library.utils import download_dataframe
from audl.stats.library.parameters import FileName


""" TODO: How to get player's team """

class SeasonPlayerStats(Endpoint):

    def __init__(self, year: int):
        super().__init__("https://theaudl.com/stats/team-season-players")
        self.year = year
        self.season_id = get_season_id(year)

    def _get_season_player_stats_df(self, show_message=True):
        dfs =[]
        page = 1
        hasPlayerLeft = True
        while(hasPlayerLeft):
            endpoint = self._get_endpoint(page)
            url = self._get_url(endpoint)
            try:
                page_df = pd.read_html(url)[0]
                dfs.append(page_df)
                if show_message:
                    print(f"Downloading {page} ...")
                page = page +1
            except ValueError:
                hasPlayerLeft = False
        df_all = pd.concat(dfs)
        return df_all

    def download_season_player_stats(self, show_message=True):
        df = self._get_season_player_stats_df(show_message)
        file_name = f"{FileName.seasonplayerstats}_{self.year}.csv"
        download_dataframe(file_name, df)


    def _get_url(self, endpoint:str):
        return f"{self.base_url}{endpoint}"

    def _get_endpoint(self, page:int)->str:
        return f"?year={self.season_id}&page={page}"



