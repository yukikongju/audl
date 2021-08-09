#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.seasonschedule import SeasonSchedule


class TestSeasonSchedule(unittest.TestCase):

    def test_get_schedule_df(self):
        schedule = SeasonSchedule().get_season_schedule_df()
        print(schedule)

    def test_download_team_schedule(self):
        SeasonSchedule("Atlanta Hustle").download_season_schedule_as_csv()


