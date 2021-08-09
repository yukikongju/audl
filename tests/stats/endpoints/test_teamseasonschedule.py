#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.teamseasonschedule import TeamSeasonSchedule


class TestTeamSeasonSchedule(unittest.TestCase):

    def test_get_team_schedule_id(self):
        games_id = TeamSeasonSchedule("Atlanta Hustle")._get_team_games_id()
        print(games_id)

    def test_get_team_schedule(self):
        schedule = TeamSeasonSchedule("Atlanta Hustle").get_team_schedule()
        print(schedule)

