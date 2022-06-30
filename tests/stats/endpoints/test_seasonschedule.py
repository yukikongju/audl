#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

class TestSeasonSchedule(unittest.TestCase):

    def test_all_schedule(self):
        df = AllSchedule().get_schedule()

    def test_season_schedule(self):
        df = SeasonSchedule(2022).get_schedule()

    def test_team_season_schedule(self):
        df = TeamSeasonSchedule(2022, 'royal').get_schedule()

    def test_team_season_against_opponent_schedule(self):
        df = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()

