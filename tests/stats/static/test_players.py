#!/usr/bin/env/python

#  from __future__ import absolute_import
import unittest
import sys
from audl.stats.static import players


class TestPlayers(unittest.TestCase):

    def test_find_players_by_full_name(self):
        print(players.find_players_by_full_name("Rowan McDonnell"))
        print(players.find_players_by_full_name("Brien"))

    def test_find_players_by_id(self):
        print(players.find_player_by_id("rmcdonnel"))


if __name__ == "__main__":
    unittest.main()
