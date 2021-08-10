#!/usr/bin/env/python

import json
import pandas as pd
import numpy as np
import requests

from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players
#  from audl.stats.library.parameters import TeamStatsName
#  from audl.stats.library.parameters import team_stats_perc_columns_names, team_stats_row_names
from audl.stats.library.parameters import quarters_clock_dict
from audl.stats.library.parameters import HerokuPlay
#  from audl.stats.library.parameters import team_points_by_points_columns_names
from audl.stats.library.parameters import team_roster_columns_name


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://audl-stat-server.herokuapp.com/stats-pages/game/")
        self.game_id = game_id
        self.endpoint = game_id
        self.url = self._get_url()
        self.json = self._get_json_from_url()
        #  self.roster_home = self._get_roster_home_team_df()
        #  self.roster_away = self._get_roster_away_team_df()

    def _get_json_from_url(self):
        return requests.get(self.url).json()

    #  def _get_game_metadata(self):
        #  game = self.json['game']
        #  team_season_home = game['team_season_home']
        #  team_season_away = game['team_season_away']
        #  score_home = game['score_home']
        #  score_away = game['score_away']
        #  score_times_home = game['score_times_home'][1:]
        #  score_times_away = game['score_times_away'][1:]
        #  pass

    def _get_teams_full_name(self):
        game = self.json['game']
        team_season_home = game['team_season_home']
        team_season_away = game['team_season_away']
        home_name = team_season_home['team']['name']
        home_city = team_season_home['city']
        home_full_name = f"{home_city} {home_name}"
        away_name = team_season_away['team']['name']
        away_city = team_season_away['city']
        away_full_name = f"{away_city} {away_name}"
        return home_full_name, away_full_name

    def _get_roster_df(self, roster):
        rows = []
        for index, player in enumerate(roster):
            players = roster[index]
            identification_num = player['id']
            jersey_number = player['jersey_number']
            first_name = player['player']['first_name']
            last_name = player['player']['last_name']
            player_id = player['player']['ext_player_id']
            row = [identification_num, first_name,
                   last_name, jersey_number, player_id]
            rows.append(row)

        # create data frame
        df = pd.DataFrame(rows, columns=team_roster_columns_name)
        return df

    def _get_roster_home_team_df(self):
        home_roaster = self.json['rostersHome']
        return self._get_roster_df(home_roaster)

    def _get_roster_away_team_df(self):
        away_roaster = self.json['rostersAway']
        return self._get_roster_df(away_roaster)

    @staticmethod
    def _round_2_decimals(perc: float) -> float:
        return round(perc, 2)

    @staticmethod
    def _format_perc_to_string(perc: float) -> str:
        return "{:.0%}".format(perc)

    @staticmethod
    def _transpose_list(data: list) -> list:
        return np.array(data).T.tolist()

    def _get_team_lineups_from_line(self, events: list) -> list:
        data = []
        for event in json.loads(events):
            #  print(event)
            if event["t"] == HerokuPlay.OLineIndex:
                lineup_ids = event["l"]
                row = ["O-Line", lineup_ids]
                data.append(row)
            elif event["t"] == HerokuPlay.DLineIndex:
                lineup_ids = event["l"]
                row = ["D-Line", lineup_ids]
                data.append(row)
        return data

    def _get_all_scores_time(self):
        game = self.json['game']
        score_times_home = game['score_times_home'][1:]
        score_times_away = game['score_times_away'][1:]
        times = score_times_away + score_times_home
        times.sort()
        return times

    def _get_lineup_from_lineup_ids(self, team_lineup_df: list, lineup_ids: list) -> list:
        players = []
        for player_id in lineup_ids:
            player_index = team_lineup_df[team_lineup_df['identification_num']
                                          == player_id].index[0]
            last_name = team_lineup_df.iloc[player_index]['last_name']
            players.append(last_name)
        players.sort()
        return players

    @staticmethod
    def _get_endquarter_point_duration(last_scoring_time: int) -> str:
        time_til_end_quarter = min(
            quarters_clock_dict['Q1_end'] - last_scoring_time,
            quarters_clock_dict['Q2_end'] - last_scoring_time,
            quarters_clock_dict['Q3_end'] - last_scoring_time,
            quarters_clock_dict['Q4_end'] - last_scoring_time,
            quarters_clock_dict['OT1_end'] - last_scoring_time
        )
        return GameStats._convert_seconds_to_minutes_string(time_til_end_quarter)

    @staticmethod
    def _convert_time_to_clock(time: int):
        if time <= quarters_clock_dict['Q1_end']:
            return GameStats._convert_time_to_minutes(quarters_clock_dict['Q1_end'] - time)
        elif time <= quarters_clock_dict['Q2_end']:
            return GameStats._convert_time_to_minutes(quarters_clock_dict['Q2_end'] - time)
        elif time <= quarters_clock_dict['Q3_end']:
            return GameStats._convert_time_to_minutes(quarters_clock_dict['Q3_end'] - time)
        elif time <= quarters_clock_dict['Q4_end']:
            return GameStats._convert_time_to_minutes(quarters_clock_dict['Q4_end'] - time)
        elif time <= quarters_clock_dict['OT1_end']:
            return GameStats._convert_time_to_minutes(quarters_clock_dict['OT1_end'] - time)

    # TOFIX: put in event class
    @staticmethod
    def _convert_time_to_quarter(time: int) -> str:
        if time <= quarters_clock_dict['Q1_end']:
            return "Q1"
        elif time <= quarters_clock_dict['Q2_end']:
            return "Q2"
        elif time <= quarters_clock_dict['Q3_end']:
            return "Q3"
        elif time <= quarters_clock_dict['Q4_end']:
            return "Q4"
        elif time <= quarters_clock_dict['OT1_end']:
            return "OT1"

    @staticmethod
    def _convert_times_to_point_durations(times: list) -> list:
        point_durations = []
        last_point_time = 0
        for time in times:
            point_duration = time - last_point_time
            string_duration = GameStats._convert_seconds_to_minutes_string(
                point_duration)
            point_durations.append(string_duration)
            last_point_time = time
        return point_durations

    @ staticmethod
    def _convert_time_to_minutes(seconds: int) -> str:
        # mm:ss
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        return '{:2d}:{:02d}'.format(m, s).strip()

    @staticmethod
    def _convert_seconds_to_minutes_string(seconds: int) -> str:
        # 1m50s
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        return '{:2d}m{:02d}s'.format(m, s).strip()

    def _get_home_team_events(self) -> list:
        tsgHome = self.json['tsgHome']
        events = tsgHome['events']
        return events

    def _get_away_team_events(self) -> list:
        tsgAway = self.json['tsgAway']
        events = tsgAway['events']
        return events

    @staticmethod
    def _flatten_2D_to_1D(data):
        return [item for sublist in data for item in sublist]

    # DUMY

    def _print_events(self):
        events = self._get_home_team_events()
        for _, event in enumerate(json.loads(events)):
            if event['t'] == HerokuPlay.Goal:
                receiver_id = event['r']
                receiver = self._get_player_last_name_from_identification(
                    receiver_id, self.roster_home)
                x = event['x']
                y = event['y']
                print(f"Scored by: {receiver} x: {x} y: {y}")
            elif event['t'] == HerokuPlay.OLineIndex:
                # get lineup + convert ids to name
                lineup_ids = event['l']
                lineup = self._get_lineup_from_lineup_ids(
                    self.roster_home, lineup_ids)
                print(f"Lineup O-Line: {lineup}")
            elif event['t'] == HerokuPlay.DLineIndex:
                lineup_ids = event['l']
                lineup = self._get_lineup_from_lineup_ids(
                    self.roster_home, lineup_ids)
                print(f"Lineup D-Line: {lineup}")
            elif event['t'] == HerokuPlay.TimeoutDefense:
                lineup_ids = event['l']
                lineup = self._get_lineup_from_lineup_ids(
                    self.roster_home, lineup_ids)
                print(f"Timeout Defense: {lineup}")
            elif event['t'] == HerokuPlay.TimeoutOffense:
                lineup_ids = event['l']
                lineup = self._get_lineup_from_lineup_ids(
                    self.roster_home, lineup_ids)
                print(f"Timeout Offense: {lineup}")
            elif event['t'] == HerokuPlay.EndOfQ1:
                print(f"EndOfQ1")
            elif event['t'] == HerokuPlay.EndOfQ2:
                print(f"EndOfQ2")
            elif event['t'] == HerokuPlay.EndOfQ3:
                print(f"EndOfQ3")
            elif event['t'] == HerokuPlay.EndOfQ4:
                print(f"EndOfQ4")
            elif event['t'] == HerokuPlay.PassCompleted:
                receiver_id = event['r']
                receiver = self._get_player_last_name_from_identification(
                    receiver_id, self.roster_home)
                x = event['x']
                y = event['y']
                print(f"Pass to {receiver} x: {x} y: {y}")
            elif event['t'] == HerokuPlay.Block:
                receiver_id = event['r']
                receiver = self._get_player_last_name_from_identification(
                    receiver_id, self.roster_home)
                print(f"Blocked by {receiver}")
            elif event['t'] == HerokuPlay.ThrowawayCaused:
                print(f"Throwaway caused")
            elif event['t'] == HerokuPlay.ScoredOn:
                print("Scored On")
            elif event['t'] == HerokuPlay.Pull:
                receiver_id = event['r']
                receiver = self._get_player_last_name_from_identification(
                    receiver_id, self.roster_home)
                print(f"Pull by {receiver}")
            elif event['t'] == HerokuPlay.Throwaway:
                print("Throwaway from ")
            else:
                print(f"Unknown {event['t']}")

    def _download_play_by_play(self):
        pass

    def _get_player_last_name_from_identification(self, identification: int, team_lineup_df: list) -> str:
        player_index = team_lineup_df[team_lineup_df['identification_num']
                                      == identification].index[0]
        last_name = team_lineup_df.iloc[player_index]['last_name']
        return last_name
