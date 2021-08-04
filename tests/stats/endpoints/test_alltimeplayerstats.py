#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.alltimeplayerstats import AllTimePlayerStats


def test_download_all_time_player_stats():
    AllTimePlayerStats().download_all_time_player_stats()
