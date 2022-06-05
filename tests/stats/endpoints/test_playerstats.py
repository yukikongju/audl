import unittest
from audl.stats.endpoints.playerstats import PlayerStats


def test_fetch_player_stats():
    playerstats = PlayerStats(2022, 'points', 'breeze') # works
    playerstats = PlayerStats(2022, 'total', 'breeze') # works
    playerstats = PlayerStats(2022, 'total', 'all') # works
    players_stats = PlayerStats(2019, 'game', 'all')
    playerstats = PlayerStats('career', 'total', 'breeze')
    players_stats = PlayerStats('career', 'total', 'all')
    players_stats = PlayerStats('career', 'game', 'all')



def test_download_player_stats():
    flag = PlayerStats(2022, 'total', 'breeze').download_stats_as_dataframe('tmp.csv') # works

