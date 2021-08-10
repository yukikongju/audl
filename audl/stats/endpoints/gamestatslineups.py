#!/usr/bin/env/python

import json
import pandas as pd

from audl.stats.endpoints.gamestats import GameStats
from audl.stats.library.parameters import team_points_by_points_columns_names
from audl.stats.library.parameters import HerokuPlay


class GameStatsLineups(GameStats):

    def __init__(self, game_id: str):
        super().__init__(game_id)

    def get_home_points_by_points_lineups(self):
        home_events = self._get_home_team_events()
        game = self.json['game']
        score_times_home = game['score_times_home'][1:]
        df = self._get_team_points_by_points_df(
            home_events, score_times_home, self._get_roster_home_team_df())
        return df

    def get_away_points_by_points_lineups(self):
        away_events = self._get_away_team_events()
        game = self.json['game']
        score_times_away = game['score_times_away'][1:]
        df = self._get_team_points_by_points_df(
            away_events, score_times_away, self._get_roster_away_team_df())
        return df

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
                # get quarter
                # get point duration
                quarter = GameStats._convert_time_to_quarter(last_scoring_time)
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
