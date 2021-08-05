#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players


class PlayerProfile(Endpoint):

    def __init__(self, full_name: str):
        super().__init__("https://theaudl.com/league/players/")
        self.full_name = full_name
        self.endpoint = self._get_endpoint()
        self.url = self._get_url()

    def _get_endpoint(self):
        return players.find_player_id_from_full_name(self.full_name)

    def _is_audl_player(self) -> bool:
        player_names = players.get_list_players_by_name()
        for name in player_names:
            if name == self.full_name:
                return True
        return False

    def get_regular_seasons_career(self) -> list:
        dfs = pd.read_html(self.url)
        return dfs[0]

    def get_playoffs_career(self):
        pass
