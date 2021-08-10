#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.gamestatsrosters import GameStatsRosters


class TestGameStatsRosters(unittest.TestCase):

    def test_get_roster_home(self):
        print(GameStatsRosters("2021-07-16-DAL-SEA").get_roster_home_metadata())

    def test_get_roster_away(self):
        print(GameStatsRosters("2021-07-16-DAL-SEA").get_roster_away_metadata())
