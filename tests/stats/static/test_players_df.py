#!/usr/bin/env/python

from audl.stats.static import players


def test_find_value_in_column():  # Successfully tested
    print(players.find_players_by_full_name("Rowan McDonnell"))


def test_find_row_by_args():  # Successfully tested
    print(players.find_player_row_by_full_name("Rowan McDonnell"))
    print(players.find_player_row_by_id("rmcdonnel"))


def test_find_rows_with_same_col_value():  # Successfully tested
    print(players.find_df_players_who_share_first_name("Matthew"))
    print(players.find_df_players_who_share_last_name("Williams"))


def test_find_cell_value_from_player_col_value():  # Successfully tested
    print(players.find_player_id_from_full_name("Rowan McDonnell"))
    print(players.find_player_full_name_from_id("rmcdonnel"))


if __name__ == "__main__":
    test_find_value_in_column()
    test_find_row_by_args()
    test_find_rows_with_same_col_value()
    test_find_cell_value_from_player_col_value()
