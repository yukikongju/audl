#!/usr/bin/env/python

""" Work with Pandas Dataframe """

import pandas as pd
from audl.stats.library.data import players
from audl.stats.library.data import players_columns_name
from audl.stats.library.data import player_col_id, player_col_full_name, player_col_first_name, player_col_last_name
from audl.stats.library.data import player_index_id, player_index_full_name, player_index_first_name, player_index_last_name


def _get_players_df():
    return pd.DataFrame(players, columns=players_columns_name)


def _find_value_in_column(substring: str, column_name: str) -> list:
    df = _get_players_df()
    values = []
    for value in list(df[column_name]):
        if substring in value:
            values.append(value)
    return values


def find_players_by_full_name(substring: str) -> list:
    return _find_value_in_column(substring, player_col_full_name)


def _find_row_by_col_args(col_val: str, column_name: str) -> list:
    df = _get_players_df()
    row = df.loc[df[column_name] == col_val]
    return row.values.flatten().tolist()


def find_player_row_by_full_name(full_name: str) -> list:
    return _find_row_by_col_args(full_name, player_col_full_name)


def find_player_row_by_id(player_id: str) -> list:
    return _find_row_by_col_args(player_id, player_col_id)


def _find_rows_with_same_col_value(shared_value: str, column_name: str):
    df = _get_players_df()
    rows = []
    for index, value in enumerate(list(df[column_name])):
        if value == shared_value:
            row = df.iloc[index]
            rows.append(list(row))
    return rows


def find_df_players_who_share_first_name(first_name: str) -> list:
    data = _find_rows_with_same_col_value(first_name, player_col_first_name)
    return pd.DataFrame(data=data, columns=players_columns_name)


def find_df_players_who_share_last_name(last_name: str) -> list:
    data = _find_rows_with_same_col_value(last_name, player_col_last_name)
    return pd.DataFrame(data=data, columns=players_columns_name)


def _find_cell_value_from_col_value(col_value: str, col_name_input: str, col_index_output: int):
    row = _find_row_by_col_args(col_value, col_name_input)
    return row[col_index_output]


def find_player_full_name_from_id(player_id: str) -> str:
    return _find_cell_value_from_col_value(player_id, player_col_id, player_index_full_name)


def find_player_id_from_full_name(full_name: str) -> str:
    return _find_cell_value_from_col_value(full_name, player_col_full_name, player_index_id)


def _get_dataframe_column_as_list(col_name: str):
    return list(_get_players_df()[col_name])


def get_list_players_by_name() -> list:
    return _get_dataframe_column_as_list(player_col_full_name)


def get_list_players_id() -> list:
    return _get_dataframe_column_as_list(player_col_id)
