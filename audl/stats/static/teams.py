#!/usr/bin/env/python

""" Work with Pandas Dataframe """

import pandas as pd
from audl.stats.library.data import teams
from audl.stats.library.data import teams_columns_name
from audl.stats.library.data import team_col_id, team_col_abr, team_col_full_name, team_col_team_name	, team_col_city, team_col_state, team_col_year_founded
from audl.stats.library.data import team_index_full_name, team_index_state, team_index_city, team_index_id, team_index_year_founded, team_index_abbreviation, team_index_team_name


def _get_teams_df():
    return pd.DataFrame(teams, columns=teams_columns_name)


def _find_value_in_column(substring: str, column_name: str) -> list:
    df = _get_teams_df()
    values = []
    for value in list(df[column_name]):
        if substring in value:
            values.append(value)
    return values


def find_teams_containing_substring_in_full_name(substring: str) -> list:
    return _find_value_in_column(substring, team_col_full_name)


def find_teams_containing_substring_in_city(substring: str) -> list:
    return _find_value_in_column(substring, team_col_city)


def _find_row_by_col_args(col_val: str, column_name: str) -> list:
    df = _get_teams_df()
    row = df.loc[df[column_name] == col_val]
    return row.values.flatten().tolist()


def find_team_row_by_full_name(full_name: str) -> list:
    return _find_row_by_col_args(full_name, team_col_full_name)


def find_team_row_by_city(full_name: str) -> list:
    return _find_row_by_col_args(full_name, team_col_city)


def _find_rows_with_same_col_value(shared_value: str, column_name: str):
    df = _get_teams_df()
    rows = []
    for index, value in enumerate(list(df[column_name])):
        if value == shared_value:
            row = df.iloc[index]
            rows.append(list(row))
    return rows


def find_df_teams_with_same_state(state: str):
    data = _find_rows_with_same_col_value(state, team_col_state)
    return pd.DataFrame(data, columns=teams_columns_name)


def find_df_teams_with_same_creation_date(year: str):  # TOFIX: error with 2015
    data = _find_rows_with_same_col_value(year, team_col_year_founded)
    return pd.DataFrame(data, columns=teams_columns_name)


def _find_cell_value_from_col_value(col_value: str, col_name_input: str, col_index_output: int):
    row = _find_row_by_col_args(col_value, col_name_input)
    return row[col_index_output]


def find_team_full_name_from_id(team_id: str) -> str:
    return _find_cell_value_from_col_value(team_id, team_col_id, team_index_full_name)


def find_id_from_team_full_name(full_name: str) -> str:
    return _find_cell_value_from_col_value(full_name, team_col_full_name, team_index_id)


def find_id_from_team_abreviation(abreviation: str) -> str:
    return _find_cell_value_from_col_value(abreviation, team_col_abr, team_index_id)


def find_team_abreviation_from_id(team_id: str) -> str:
    return _find_cell_value_from_col_value(team_id, team_col_id, team_index_abbreviation)


def find_team_full_name_from_team_abreviation(abreviation: str) -> str:
    return _find_cell_value_from_col_value(abreviation, team_col_abr, team_index_full_name)


def find_team_abreviation_from_team_full_name(full_name: str) -> str:
    return _find_cell_value_from_col_value(full_name, team_col_full_name, team_index_abbreviation)


def find_team_name_from_full_name(full_name:str) ->str:
    return _find_cell_value_from_col_value(full_name, team_col_full_name, team_index_team_name)

def get_list_teams_by_name() -> list:
    return _get_dataframe_column_as_list(team_col_full_name)


def get_list_teams_id() -> list:
    return _get_dataframe_column_as_list(team_col_id)

