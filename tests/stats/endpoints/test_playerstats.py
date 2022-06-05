import unittest
from audl.stats.endpoints.playerstats import PlayerStats


def test_fetch_player_stats():
    playerstats = PlayerStats(2022, 'points', 'breeze') # works
    playerstats = PlayerStats(2022, 'total', 'breeze') # works
    playerstats = PlayerStats(2022, 'total', 'all') # works



def test_download_player_stats():
    flag = PlayerStats(2022, 'total', 'breeze').download_stats_as_dataframe('tmp.csv') # works

