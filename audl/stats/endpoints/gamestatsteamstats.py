#!/usr/bin/env/python

import json
import pandas as pd

from audl.stats.endpoints.gamestats import GameStats
from audl.stats.library.parameters import TeamStatsName
from audl.stats.library.parameters import team_stats_perc_columns_names, team_stats_row_names


class GameStatsTeamStats(GameStats):

    def __init__(self, game_id: str):
        super().__init__(game_id)

    def get_team_stats(self) -> list:
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
        return df

    def _get_away_team_stats_formatted(self) -> list:
        tsgAway = self.json['tsgAway']
        df = self._get_team_stats_col_formatted(tsgAway)
        return df

    def _get_team_stats_blocks_turnovers(self, tsg: list) -> [int, int]:
        blocks = tsg['blocks']
        turnovers = tsg['turnovers']
        #  start_on_offense = tsg['startOnOffense']
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
