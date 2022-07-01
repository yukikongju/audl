#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.teamstats import TeamStats


class TestTeamStats(unittest.TestCase):

    def test_get_page_results_as_dataframe(self):
        team_stats = TeamStats('career', 'game', 'team')        # works
        team_stats = TeamStats('career', 'total', 'team')       # works
        team_stats = TeamStats(2019, 'total', 'team')           # works

        res = team_stats.get_table()



