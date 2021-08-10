#!/usr/bin/env/python

import json
import pandas as pd

from audl.stats.endpoints.gamestats import GameStats
from audl.stats.library.parameters import team_roster_columns_name


class GameStatsRosters(GameStats):

    def __init__(self, game_id: str):
        super().__init__(game_id)

    def get_roster_home_metadata(self):
        return self._get_roster_home_team_df()

    def get_roster_away_metadata(self):
        return self._get_roster_away_team_df()
