import unittest
from audl.stats.endpoints.playerstats import PlayerStats


def test_fetch_player_stats():
    playerstats = PlayerStats(2022, 'points', 'breeze').fetch_table()
    playerstats = PlayerStats(2022, 'total', 'breeze').fetch_table()
    playerstats = PlayerStats(2022, 'total', 'all') .fetch_table()
    players_stats = PlayerStats(2019, 'game', 'all').fetch_table()
    playerstats = PlayerStats('career', 'total', 'breeze').fetch_table()
    players_stats = PlayerStats('career', 'total', 'all').fetch_table()
    players_stats = PlayerStats('career', 'game', 'all').fetch_table()



def test_download_player_stats():
    flag = PlayerStats(2022, 'total', 'breeze').download_stats_as_dataframe('tmp.csv') # works

