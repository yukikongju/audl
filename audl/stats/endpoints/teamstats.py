#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.static.miscellaneous import get_season_id


class TeamStats(Endpoint):

    def __init__(self, year: int):
        super().__init__("https://theaudl.com/stats/team?year=")
        self.year = year
        self.url = self._get_url()

    def _get_url(self):
        season_id = get_season_id(self.year)
        return f"{self.base_url}{season_id}"

    def get_teams_stats_by_season(self):
        dfs = self._fetch_dfs_from_url()
        return dfs[0]
