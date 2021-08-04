#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.library.parameters import FileName
from audl.stats.library.utils import download_dataframe


class AllTimePlayerStats(Endpoint):

    def __init__(self):
        super().__init__("https://theaudl.com/stats/players-all-time?page=")

    def _get_all_time_player_stats_df(self, show_message=True):
        hasPlayerLeft = True
        dfs = []
        page = 1
        while(hasPlayerLeft):
            try:
                url = self._get_url(page)
                page_df = pd.read_html(url)[0]
                dfs.append(page_df)
                if show_message:
                    print(f"Downloading page {page} ...")
                page = page + 1
            except ValueError:
                hasPlayerLeft = False
                if show_message:
                    print("No more players to add to dataframe")
        df = pd.concat(dfs)
        return df.drop_duplicates()

    def _get_url(self, page_num: int) -> str:
        return f"{self.base_url}{page_num}"

    def download_all_time_player_stats(self, show_message=True):
        df = self._get_all_time_player_stats_df(show_message)
        download_dataframe(FileName.alltimeplayer, df)
