#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.gamestatsboxscores import GameStatsBoxScores


class TestGameStatsBoxScores(unittest.TestCase):

    def test_get_boxscores(self):
        print(GameStatsBoxScores("2021-07-16-DAL-SEA").get_box_scores())
