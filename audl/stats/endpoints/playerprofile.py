#!/usr/bin/env/python

import pandas as pd
from audl.stats.static import players


class PlayerProfile(object):

    BASE_URL = "https://theaudl.com/league/players/"

    def __init__(self, player_id: str):
        self.player_id = player_id
        self.url = BASE_URL + player_id
        self.full_name = players.find_player_by_id(player_id)

    def get_all_regular_seasons_stats(self):
        dfs = pd.read_html(self.url)
        return dfs[0]

    def get_regular_season_by_year(self, year: str):
        df_all = get_regular_season_career()
        df_season = df_all.loc[df['YR'] == year]
        if df_season is None:
            raise Exception(f"{self.full_name} did not play in {year}")
        else:
            return df_season

    def get_regular_season_career(self):
        return get_regular_season_career().loc[df['YR'] == 'Career']

    def get_all_playoffs_stats(self):
        pass

    def get_playoff_by_year(self):
        pass

    def get_playoff_career(self):
        pass
