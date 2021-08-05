#!/usr/bin/env/python

import pandas as pd
from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://theaudl.com/stats/game/")
        self.game_id = game_id
        self.endpoint = game_id
        self.url = self._get_url()

    def _fetch_url(self):
        driver = webdriver.Chrome()
        response = driver.get(self.url)
        print(response)

    def get_box_scores(self):
        pass

    def get_team_stats(self):
        pass

    def _get_player_stats_both_teams(self):
        pass

    def get_player_stats_home_team(self):
        pass

    def get_player_stats_away_team(self):
        pass

    def _get_play_by_play_lineups(self):
        pass
