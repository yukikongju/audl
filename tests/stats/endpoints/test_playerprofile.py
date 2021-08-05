#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.playerprofile import PlayerProfile


class TestPlayerProfile(unittest.TestCase):

    def test_get_regular_seasons_career(self):
        print(PlayerProfile("Rowan McDonnell").get_regular_seasons_career())

    def test_is_audl_player(self):
        print(PlayerProfile("Rowan McDonnell")._is_audl_player())
