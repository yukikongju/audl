#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.gamestats import GameStats


class TestGameStats(unittest.TestCase):

    def test_get_teams_metadata(self):
        teams = GameStats('2022-06-11-TOR-MTL').get_teams_metadata()

    def test_get_players_metadata(self):
        players = GameStats('2022-06-11-TOR-MTL').get_players_metadata()

    def test_get_team_stats(self, ):
        stats = GameStats('2022-06-11-TOR-MTL').get_team_stats()
        

