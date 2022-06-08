#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.seasonschedule import SeasonSchedule


class TestSeasonSchedule(unittest.TestCase):

    def test_get_team_season_schedule_against_opponent(self, ):
        schedule = SeasonSchedule()
        games = schedule.get_all_games_ever_played()
        games = schedule.get_season_schedule(2022)
        games = schedule.get_team_season_schedule('aviators', 2022)
        games = schedule.get_team_season_schedule_against_opponent(
                2022, 'aviators', 'growlers')
        

    #  def test_get_schedule_df(self):
    #      schedule = SeasonSchedule().get_season_schedule_df()
    #      print(schedule)

    #  def test_download_team_schedule(self):
    #      SeasonSchedule("Atlanta Hustle").download_season_schedule_as_csv()


