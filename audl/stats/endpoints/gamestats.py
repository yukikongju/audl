#!/usr/bin/env/python

import json
import pandas as pd
import numpy as np
import requests

from audl.stats.endpoints._base import Endpoint
from audl.stats.static import players
from audl.stats.library.parameters import TeamStatsName
from audl.stats.library.parameters import team_stats_perc_columns_names, team_stats_row_names
from audl.stats.library.parameters import quarters_clock_dict, box_scores_columns_names
from audl.stats.library.parameters import HerokuPlay
from audl.stats.library.parameters import team_points_by_points_columns_names
from audl.stats.library.parameters import team_roster_columns_name


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://audl-stat-server.herokuapp.com/stats-pages/game/")
        self.game_id = game_id
        self.endpoint = game_id
        self.url = self._get_url()
        self.json = self._get_json_from_url()
        self.roster_home = self._get_roster_home_team_df()
        self.roster_away = self._get_roster_away_team_df()

    def _get_json_from_url(self):
        return requests.get(self.url).json()

    def _get_game_metadata(self):
        game = self.json['game']
        team_season_home = game['team_season_home']
        team_season_away = game['team_season_away']
        score_home = game['score_home']
        score_away = game['score_away']
        score_times_home = game['score_times_home'][1:]
        score_times_away = game['score_times_away'][1:]
        pass

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
        # get data from json
        rows = []
        for index, player in enumerate(roster):
            players = roster[index]
            identification_num = player['id']
            jersey_number = player['jersey_number']
            first_name = player['player']['first_name']
            last_name = player['player']['last_name']
            #  full_name = f"{first_name} {last_name}"
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

    def _get_team_stats_blocks_turnovers(self, tsg: list) -> [int, int]:
        blocks = tsg['blocks']
        turnovers = tsg['turnovers']
        start_on_offense = tsg['startOnOffense']
        return blocks, turnovers

    def _get_team_stats_df_perc_from_json(self, tsg: list) -> list:
        # get stats from json
        completions_numerator = tsg['completionsNumer']
        completions_denominator = tsg['completionsDenom']
        d_lines_breaks_numerator = tsg['dLineBreaksNumer']
        d_lines_breaks_denominator = tsg['dLineBreaksDenom']
        hucks_numerator = tsg['hucksNumer']
        hucks_denominator = tsg['hucksDenom']
        o_line_holds_numerator = tsg['oLineHoldsNumer']
        o_line_holds_denominator = tsg['oLineHoldsDenom']
        red_zone_numerator = tsg['redZoneNumer']
        red_zone_denominator = tsg['redZoneDenom']

        # calculate percentage
        completion_perc = GameStats._round_2_decimals(
            completions_numerator / completions_denominator)
        hucks_perc = GameStats._round_2_decimals(
            hucks_numerator / hucks_denominator)
        offensive_holds_perc = GameStats._round_2_decimals(
            o_line_holds_numerator / o_line_holds_denominator)
        defensive_breaks_perc = GameStats._round_2_decimals(
            d_lines_breaks_numerator / d_lines_breaks_denominator)
        red_zone_perc = GameStats._round_2_decimals(
            red_zone_numerator / red_zone_denominator)

        # create dataframe
        data = [
            [TeamStatsName.Completions,
                completions_numerator, completions_denominator, completion_perc],
            [TeamStatsName.Hucks,
                hucks_numerator, hucks_denominator, hucks_perc],
            [TeamStatsName.Offensive_holds,
                o_line_holds_numerator, o_line_holds_denominator, offensive_holds_perc],
            [TeamStatsName.Defensive_breaks,
                d_lines_breaks_numerator, d_lines_breaks_denominator, defensive_breaks_perc],
            [TeamStatsName.Red_zone_possessions,
                red_zone_numerator, red_zone_denominator, red_zone_perc],
        ]
        df_perc = pd.DataFrame(data, columns=team_stats_perc_columns_names)
        return df_perc

    @staticmethod
    def _format_perc_to_string(perc: float) -> str:
        return "{:.0%}".format(perc)

    def _get_team_stats_col_formatted(self, tsg: list) -> list:
        # get percentage df and reformat into single column
        df_perc = self._get_team_stats_df_perc_from_json(tsg)
        df_perc['Percentage'] = df_perc['Percentage'].apply(
            GameStats._format_perc_to_string)
        df_perc['Concat'] = df_perc['Percentage'].map(
            str) + '(' + df_perc['Successful'].map(str) + '/' + df_perc['Opportunities'].map(str) + ')'

        # get blocks and turnovers count
        blocks, turnovers = self._get_team_stats_blocks_turnovers(tsg)
        column = list(df_perc['Concat'])
        column.append(blocks)
        column.append(turnovers)
        return column

    def _get_home_team_stats_formatted(self) -> list:
        tsgHome = self.json['tsgHome']
        df = self._get_team_stats_col_formatted(tsgHome)
        #  df = self._get_team_stats_df_perc_from_json(tsgHome)
        return df

    def _get_away_team_stats_formatted(self) -> list:
        tsgAway = self.json['tsgAway']
        df = self._get_team_stats_col_formatted(tsgAway)
        #  df = self._get_team_stats_df_perc_from_json(tsgAway)
        return df

    def get_team_stats(self) -> list:  # same format as audl
        # get column stats for each team
        home_team_name, away_team_name = self._get_teams_full_name()
        home_col_formatted = self._get_home_team_stats_formatted()
        away_col_formatted = self._get_away_team_stats_formatted()

        # combine columns into dataframe
        data = [team_stats_row_names,
                away_col_formatted, home_col_formatted]
        data_transposed = GameStats._transpose_list(data)
        header = ['', away_team_name, home_team_name]
        df = pd.DataFrame(data_transposed, columns=header)
        return df

    def _get_player_stats_both_teams(self):
        pass

    def get_player_stats_home_team(self):
        pass

    def get_player_stats_away_team(self):
        pass

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
            #  first_name = team_lineup_df.iloc[player_index]['first_name']
            last_name = team_lineup_df.iloc[player_index]['last_name']
            #  full_name = f"{first_name} {last_name}"
            #  players.append(full_name)
            players.append(last_name)
        players.sort()
        return players

    def _get_team_points_by_points_df(self, events: list, team_scoring_times: list, team_lineup_df: list):
        # TOFIX : deal with changement de ligne
        # get points durations + clock
        all_scoring_times = self._get_all_scores_time()
        points_durations = GameStats._convert_times_to_point_durations(
            all_scoring_times)

        # get data
        score_home = 0
        score_away = 0
        last_scoring_time = 0
        index = 0
        data = []
        for _, event in enumerate(json.loads(events)):
            if event['t'] == HerokuPlay.OLineIndex or event['t'] == HerokuPlay.DLineIndex:
                # get line type
                line = "O-Line" if event['t'] == HerokuPlay.OLineIndex else "D-Line"
                # get lineup + convert ids to name
                lineup_ids = event['l']
                lineup = self._get_lineup_from_lineup_ids(
                    team_lineup_df, lineup_ids)

            if event['t'] == HerokuPlay.Goal:  # Goal is scored
                # add point duration
                points_duration = points_durations[index]
                # add clock
                clock = GameStats._convert_time_to_clock(
                    all_scoring_times[index])
                # get quarter
                quarter = GameStats._convert_time_to_quarter(
                    all_scoring_times[index])
                # add outcome
                outcome = "Win"
                # add current score
                score_home += 1
                current_score = f"{score_home}-{score_away}"

                #  add row
                row = [current_score, line, clock,
                       points_duration, quarter, lineup]
                data.append(row)
                last_scoring_time = all_scoring_times[index]
                index += 1
                print(row)
            elif event['t'] == HerokuPlay.ScoredOn:
                # add point duration
                points_duration = points_durations[index]
                # add clock
                clock = GameStats._convert_time_to_clock(
                    all_scoring_times[index])
                # get quarter
                quarter = GameStats._convert_time_to_quarter(
                    all_scoring_times[index])
                # add outcome
                outcome = "Lost"
                score_away += 1
                current_score = f"{score_home}-{score_away}"

                #  add row
                row = [current_score, line, clock,
                       points_duration, quarter, lineup]
                data.append(row)
                last_scoring_time = all_scoring_times[index]
                index += 1
                print(row)
            elif event['t'] == HerokuPlay.EndOfQ1 or event['t'] == HerokuPlay.EndOfQ2 or event['t'] == HerokuPlay.EndOfQ3 or event['t'] == HerokuPlay.EndOfQ4:
                # set outcome to NA -> point not finished
                outcome = "NA"
                #  current_score = f"{score_home}-{score_away}"
                # get quarter
                quarter = GameStats._convert_time_to_quarter(last_scoring_time)
                # get point duration
                point_duration = GameStats._get_endquarter_point_duration(
                    last_scoring_time)
                # get clock
                clock = "0:00"
                # add row
                row = [current_score, line, clock,
                       points_duration, quarter, lineup]
                data.append(row)
                print(row)
                #  print(index)
        df = pd.DataFrame(data, columns=team_points_by_points_columns_names)
        return df

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

    def _get_play_by_play_lineups_home_team(self):
        home_events = self._get_home_team_events()
        game = self.json['game']
        score_times_home = game['score_times_home'][1:]
        df = self._get_team_points_by_points_df(
            home_events, score_times_home, self.roster_home)
        return df

    def _get_play_by_play_lineups_away_team(self):
        away_events = self._get_away_team_events()
        game = self.json['game']
        score_times_away = game['score_times_away'][1:]
        pass

    def _get_home_team_events(self) -> list:
        tsgHome = self.json['tsgHome']
        events = tsgHome['events']
        return events

    def _get_away_team_events(self) -> list:
        tsgAway = self.json['tsgAway']
        events = tsgAway['events']
        return events

    def get_box_scores(self):
        # get team name
        home_team_name, away_team_name = self._get_teams_full_name()
        # get teams score count by quarter
        game = self.json['game']
        home_team_row = self._get_home_team_box_scores(game)
        away_team_row = self._get_away_team_box_scores(game)
        # create dataframe
        data = [away_team_row, home_team_row]
        df = pd.DataFrame(data)
        # add team name column to df
        teams = [away_team_name, home_team_name]
        df.insert(loc=0, column='Teams', value=teams)
        df.columns = box_scores_columns_names
        return df

    def _get_home_team_box_scores(self, game: list) -> list:
        final_score_home = game['score_home']
        score_times_home = game['score_times_home'][1:]
        box_scores = self._get_team_box_scores(
            final_score_home, score_times_home)
        return box_scores

    def _get_away_team_box_scores(self, game: list) -> list:
        final_score_away = game['score_away']
        score_times_away = game['score_times_away'][1:]
        box_scores = self._get_team_box_scores(
            final_score_away, score_times_away)
        return box_scores

    @staticmethod
    def _flatten_2D_to_1D(data):
        return [item for sublist in data for item in sublist]

        # TODO: Fix if overtime
    def _get_team_box_scores(self, team_final_score: int, scores_times: list) -> list:
        # TODO: Add team name here?
        has_overtime, quarters_scores = self._get_team_scores_count_by_quarter(
            scores_times)
        print(has_overtime)
        quarters_scores.append(team_final_score)
        return quarters_scores

    # TOFIX: handle Overtime
    def _get_team_scores_count_by_quarter(self, scores_time: list) -> [bool, list]:
        Q1_count, Q2_count, Q3_count, Q4_count, OT1_count = 0, 0, 0, 0, 0
        for score in scores_time:
            if score <= quarters_clock_dict['Q1_end']:
                Q1_count += 1
            elif score <= quarters_clock_dict['Q2_end']:
                Q2_count += 1
            elif score <= quarters_clock_dict['Q3_end']:
                Q3_count += 1
            elif score <= quarters_clock_dict['Q4_end']:
                Q4_count += 1
            elif score <= quarters_clock_dict['OT1_end']:
                OT1_count += 1
        if OT1_count > 0:  # there was an overtime
            return True, [Q1_count, Q2_count, Q3_count, Q4_count, OT1_count]
        else:
            return False, [Q1_count, Q2_count, Q3_count, Q4_count]

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

    def _get_player_last_name_from_identification(self, identification: int, team_lineup_df: list) -> str:
        player_index = team_lineup_df[team_lineup_df['identification_num']
                                      == identification].index[0]
        last_name = team_lineup_df.iloc[player_index]['last_name']
        return last_name
