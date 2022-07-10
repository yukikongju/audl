#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.playerprofile import PlayerProfile


class TestPlayerProfile(unittest.TestCase):

    def test_existing_player(self):
        player = PlayerProfile('cbrock')
        career = player.get_career_stats()
        reg = player.get_regular_seasons_career()
        playoffs = player.get_playoffs_career()
        season = player.get_season_games_stats(2019)
        games_stats = player.get_career_games_stats()


    def test_get_playoffs(self):
        pass

    def test_non_existing_year(self):
        pass

    def test_non_existing_playoffs(self):
        pass

if __name__ == "__main__":
    unittest.main()
