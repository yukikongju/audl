#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.seasonplayerstats import TeamSeasonPlayerStats


def test_download_season_player_stats():
    TeamSeasonPlayerStats('2015').download_season_player_stats()

