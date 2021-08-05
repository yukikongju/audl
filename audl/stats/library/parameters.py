#!/usr/bin/env/python

class Division:
    altantic = 'Atlantic'
    central = 'Central'
    west = 'West'
    canada = 'Canada Cup'


class StatisticsDescription:
    YR = 'Year'
    G = 'Games Played'
    PP = 'Points Played'
    TM = 'Team'
    AST = 'Assists'
    GLS = 'Goals'
    BLK = 'Blocks'
    PLUS_MINUS = 'Plus Minus'
    CMP = 'Completions'
    CMP_PERC = 'Completion Percentage'
    TY = 'Throwing Yards'
    RY = 'Receiving Yards'
    HA = 'Hockey Assists'
    T = 'Throwaways'
    S = 'Stall'
    C = 'Callahan'
    D = 'Drops'
    OPP = 'Offensive Points Played'
    DPP = 'Defensive Points Played'
    P = 'Pulls'


class StatisticAbbreviation:
    stat_col_year = 'YR'
    stat_col_games_played = 'G'
    stat_col_points_played = 'PP'
    stat_col_team = 'TM'
    stat_col_assists = 'AST'
    stat_col_goals = 'GLS'
    stat_col_blocks = 'BLK'
    stat_col_plus_minus = '+/-'
    stat_col_completions = 'CMP'
    stat_col_completion_perc = 'CMP%'
    stat_col_throwing_yards = 'TY'
    stat_col_receiving_yards = 'RY'
    stat_col_hockey_assists = 'HA'
    stat_col_throwaways = 'T'
    stat_col_stalls = 'S'
    stat_col_callahans = 'C'
    stat_col_drops = 'D'
    stat_col_offensive_points_played = 'OPP'
    stat_col_defensive_points_played = 'DPP'
    stat_col_pulls = 'P'


class FileName:
    alltimeplayer = 'AllTimePlayerStats'
    seasonplayerstats = 'SeasonPlayerStats'


#######################################################################
#                            Miscellaneous                            #
#######################################################################


season_dict = {
    2021: '1',
    2019: '2',
    2018: '3',
    2017: '4',
    2015: '5',
    2016: '6',
    2014: '7',
    2013: '8',
    2012: '9',
}
