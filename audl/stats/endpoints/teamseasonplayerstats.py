#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.static.miscellaneous import get_season_id
from audl.stats.static.teams import find_id_from_team_full_name


class TeamSeasonPlayerStats(Endpoint):

    def __init__(self, team_name: str, year: int):
        super().__init__("https://theaudl.com/stats/team-season-players")
        self.team_name = team_name
        self.year = year
        self.endpoint = self._get_endpoint()
        self.url = self._get_url()

    def _get_endpoint(self):
        season_id = get_season_id(self.year)
        team_id = find_id_from_team_full_name(self.team_name)
        return f"?year={season_id}&aw_team_id={team_id}"

    def get_team_season_player_stats(self):
        """ 
        [deprecated]
        Function that fetch team season player stats from https://theaudl.com/stats/team-season-players and download file as csv
        """
        return self._fetch_dfs_from_url()[0]
