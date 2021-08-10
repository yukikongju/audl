#!/usr/bin/env/python

import json
import pandas as pd

from audl.stats.endpoints.gamestats import GameStats
from audl.stats.library.parameters import quarters_clock_dict, box_scores_columns_names


class GameStatsBoxScores(GameStats):

    def __init__(self, game_id: str):
        super().__init__(game_id)
        #  self.home_team_full_name, self.away_team_full_name = self._get_teams_full_name()

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

    # TODO: Fix if overtime
    def _get_team_box_scores(self, team_final_score: int, scores_times: list) -> list:
        # TODO: Add team name here?
        has_overtime, quarters_scores = self._get_team_scores_count_by_quarter(
            scores_times)
        #  print(has_overtime)
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
