#!/usr/bin/env/python

import re
from audl.stats.library.data import players
from audl.stats.library.data import player_index_id, player_index_full_name, player_index_first_name, player_index_last_name


def _find_players(regex_pattern: str, col_id: int) -> list:
    players_found = []
    for player in players:
        if re.search(regex_pattern, str(player[col_id]), flags=re.I):
            players_found.append(_get_player_dict(player))
    return players_found


def _get_player_dict(player_row):
    return {
        'id': player_row[player_index_id],
        'full_name': player_row[player_index_full_name],
        'first_name': player_row[player_index_first_name],
        'last_name': player_row[player_index_last_name],
        #  'is_active': player_row[player_index_is_active],
    }


def find_players_by_full_name(regex_pattern):
    return _find_players(regex_pattern, player_index_full_name)


def find_players_by_first_name(regex_pattern):
    return _find_players(regex_pattern, player_index_first_name)


def find_players_by_last_name(regex_pattern):
    return _find_players(regex_pattern, player_index_last_name)


#  def find_active_players():
    #  return _find_players("True", player_index_is_active)


#  def find_inactive_players():
    #  return _find_players("False", player_index_is_active)


def find_player_by_id(player_id: str) -> str:
    regex_pattern = '^{}$'.format(player_id)
    players_list = _find_players(regex_pattern, player_index_id)
    if len(players_list) > 1:
        raise Exception('Found more than 1 id')
    elif not players_list:
        return None
    else:
        return players_list[0]


def get_all_players():
    return [_get_player_dict(player) for player in players]
