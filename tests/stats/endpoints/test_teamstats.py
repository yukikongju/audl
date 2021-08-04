#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.teamstats import TeamStats


class TestTeamStats(unittest.TestCase):

    def test_get_teams_stats_by_season(self):
        print(TeamStats(2021).get_teams_stats_by_season())
