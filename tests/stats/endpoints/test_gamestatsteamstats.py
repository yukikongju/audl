#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.gamestatsteamstats import GameStatsTeamStats


class TestGameStatsTeamStats(unittest.TestCase):

    def test_get_team_stats(self):
        print(GameStatsTeamStats("2021-07-16-DAL-SEA").get_team_stats())
