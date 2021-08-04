#!/usr/bin/env/python

""" Work with Pandas Dataframe """

import pandas as pd
from audl.stats.library.data import teams
from audl.stats.library.data import teams_columns_name
from audl.stats.library.data import team_col_id, team_col_abr, team_col_full_name, team_col_nickname, team_col_city, team_col_state
from audl.stats.library.data import team_index_full_name, team_index_state, team_index_city, team_index_id, team_index_year_founded


def _get_teams_df():
    return pd.DataFrame(teams, columns=teams_columns_name)


def _find_value_in_column(substring: str, column_name: str) -> list:
    df = _get_teams_df()
    return [value for value in list(df[column_name]) if substring in value]


def find_teams_by_full_name(substring: str) -> list:
    return _find_value_in_column(substring, team_index_full_name)


def find_teams_by_state(substring: str) -> list:
    return _find_value_in_column(substring, team_index_state)


def find_teams_by_city(substring: str) -> list:
    return _find_value_in_column(substring, team_index_city)


def _find_row_by_col_args(col_val: str, column_name: str) -> list:
    df = _get_players_df()
    row = df.loc[df[column_name] == col_val]
    return row.values.flatten().tolist()


def find_team_row_by_full_name(full_name: str) -> list:
    return _find_row_by_col_args(full_name, team_col_full_name)


def find_team_row_by_city(full_name: str) -> list:
    return _find_row_by_col_args(full_name, team_col_city)
