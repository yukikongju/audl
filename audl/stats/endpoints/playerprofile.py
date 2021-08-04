#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players_df
from audl.stats.library.parameters import StatisticAbbreviation


class PlayerProfile(Endpoint):

    def __init__(self, full_name: str):
        super().__init__("https://theaudl.com/league/players/")
        self.full_name = full_name
        self.endpoint = self._get_endpoint()
        self.url = self._get_url()

    def _get_endpoint(self):
        return players_df.find_player_id_from_full_name(self.full_name)

    def get_all_regular_seasons(self):
        dfs = pd.read_html(self.url)
        return dfs[0]

    def _is_audl_player(self) -> bool:
        player_names = players_df.get_list_players_by_name()
        for name in player_names:
            if name == self.full_name:
                return True
        return False

    def get_regular_season_by_year(self, year: int):
        df_all = self.get_all_regular_seasons()
        df_season = df_all.loc[df_all[StatisticAbbreviation.stat_col_year] == str(
            year)]
        if df_season is None:
            raise Exception(f"{self.full_name} did not play in {year}")
            #  return None
        else:
            return df_season

    def get_regular_season_career(self):
        df = self.get_all_regular_seasons()
        return df.loc[df[StatisticAbbreviation.stat_col_year] == 'Career']

    def get_all_playoffs_stats(self):
        pass

    def get_playoff_by_year(self):
        pass

    def get_playoff_career(self):
        pass
