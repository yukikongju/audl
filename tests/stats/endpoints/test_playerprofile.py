#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.playerprofile import PlayerProfile


class TestPlayerProfile(unittest.TestCase):

    def test_get_all_regular_seasons(self):
        print(PlayerProfile("Rowan McDonnell").get_all_regular_seasons())

    def test_is_audl_player(self):
        print(PlayerProfile("Rowan McDonnell")._is_audl_player())

    def test_get_regular_season_by_year(self):
        print(PlayerProfile("Rowan McDonnell").get_regular_season_by_year(2021))
