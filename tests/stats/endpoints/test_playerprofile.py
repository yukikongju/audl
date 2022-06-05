#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.playerprofile import PlayerProfile


class TestPlayerProfile(unittest.TestCase):

    def test_existing_palyer(self):
        player = PlayerProfile('cbrock')
        reg = player.get_regular_seasons_career()
        playoffs = player.get_playoffs_career()
        season = player.get_season_stats(2019)

    def test_non_existing_players(self):
        pass

    def test_non_existing_year(self):
        pass

    def test_non_existing_playoffs(self):
        pass
