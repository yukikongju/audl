#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.teamseasonplayerstats import TeamSeasonPlayerStats


class TestTeamSeasonPlayerStats(unittest.TestCase):

    def test_get_team_season_player_stats(self):
        print(TeamSeasonPlayerStats("Montreal Royal",
              2021).get_team_season_player_stats())
