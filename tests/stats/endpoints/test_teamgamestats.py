#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.teamgamestats import AllTeamGameStats, SeasonGameStats, TeamSeasonGameStats


class TestTeamSeasonSchedule(unittest.TestCase):

    def test_get_game_stats(self):
        gamestats = TeamSeasonGameStats(2022, 'royal')
        gamestats = AllTeamGameStats()
        gamestats = SeasonGameStats(2022)
        print(gamestats.get_game_stats())

if __name__ == "__main__":
    unittest.main()

