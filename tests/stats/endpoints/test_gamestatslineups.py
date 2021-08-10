#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.gamestatslineups import GameStatsLineups


class TestGameStatsLineups(unittest.TestCase):

    def test_get_lineups_home(self):
        print(GameStatsLineups(
            "2021-07-16-DAL-SEA").get_home_points_by_points_lineups())

    def test_get_lineups_away(self):
        print(GameStatsLineups(
            "2021-07-16-DAL-SEA").get_away_points_by_points_lineups())
