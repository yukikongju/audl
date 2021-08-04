#!/usr/bin/env/python

import unittest
from audl.stats.static import teams_df


class TestTeamDf(unittest.TestCase):

    def test_get_teams_df(self):  # Successfully tested!
        print(teams_df._get_teams_df())

    def test_find_value_in_column(self):  # Successfully tested!
        print(teams_df.find_teams_containing_substring_in_full_name("Montreal Royal"))
        print(teams_df.find_teams_containing_substring_in_city("M"))

    def test_find_row_by_col_args(self):  # Successfully tested!
        print(teams_df.find_team_row_by_full_name("Montreal Royal"))
        print(teams_df.find_team_row_by_city("Montreal"))

    # TO FIX: 2015 prints out SJ -> creation:2014
    def test_find_rows_with_same_col_value(self):
        print(teams_df.find_df_teams_with_same_state("California"))
        print(teams_df.find_df_teams_with_same_creation_date("2015"))

    def test_find_cell_value_from_player_col_value(self):
        self.assertEqual(
            teams_df.find_team_full_name_from_id('4'), "Chicago Union")
        self.assertEqual(teams_df.find_team_full_name_from_team_abreviation(
            'ATL'), "Atlanta Hustle")
        self.assertEqual(teams_df.find_id_from_team_full_name(
            "Montreal Royal"), '12')
        self.assertEqual(teams_df.find_id_from_team_abreviation('ATL'), '1')
        self.assertEqual(teams_df.find_team_abreviation_from_id('4'), 'ABR')
        self.assertEqual(
            teams_df.find_team_abreviation_from_team_full_name("Montreal Royal"), 'MTL')


if __name__ == "__main__":
    unittest.main()
