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

    def test_get_game_metadata(self):
        metadata = GameStats('2022-06-11-TOR-MTL').get_game_metadata()

    def test_get_roster_stats(self):
        roster = GameStats('2022-06-11-TOR-MTL').get_roster_stats()
        

    def test_get_quarter(self):
        self.assertEqual(GameStats._get_quarter(243), 'Q1')
        self.assertEqual(GameStats._get_quarter(720), 'Q2')
        self.assertEqual(GameStats._get_quarter(1324), 'Q3')
        

    def test_get_scoring_time(self):
        game = GameStats('2022-06-11-TOR-MTL')._get_scoring_time()


    def test_get_boxscores(self):
        game = GameStats('2022-06-11-TOR-MTL').get_boxscores()


    def test_print_events(self):
        game = GameStats('2022-06-11-TOR-MTL')
        events = game.print_team_events(True)
        events = game.print_team_events(False)

    def test_get_events(self):
        events = GameStats('2022-06-11-TOR-MTL').get_events()


    def test_get_throw_selection(self):
        throws = GameStats('2022-06-11-TOR-MTL').get_throw_selection()
        
    def test_get_thrower_receiver_count(self):
        thrower_receiver_count = GameStats('2022-06-11-TOR-MTL').get_thrower_receiver_count(True)
        thrower_receiver_count = GameStats('2022-06-11-TOR-MTL').get_thrower_receiver_count(False)

    def test_lineup_frequency(self):
        lineup = GameStats('2022-06-11-TOR-MTL').get_lineup_frequency(True)
        lineup = GameStats('2022-06-11-TOR-MTL').get_lineup_frequency(False)

    def test_get_teamates_selection(self):
        teamates = GameStats('2022-06-11-TOR-MTL').get_teamates_selection('jbrissett', True)
        
        
        

