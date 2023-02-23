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



#######################################################################
#                             Box Scores                              #
#######################################################################

# Absolute time in seconds for each quarter
# Regular time: 12 min per quarter
# 1rst OT: 5 minutes
# 2nd OT: sudden death
quarters_clock_dict = {
    "Q1_start": 1,      # 0 min
    "Q1_end": 720,      # 12 min
    "Q2_start": 721,    # 12 min
    "Q2_end": 1440,     # 24 min
    "Q3_start": 1441,   # 24 min
    "Q3_end": 2160,     # 36 min
    "Q4_start": 2161,   # 36 min
    "Q4_end": 2880,        # 48 min
    "OT1_start": 2881,     # 48 min
    "OT1_end": 3180,       # 53 min
    "OT2_start": 3181,     # 53 min
    #  "OT2_end": 0,       # ? min
}

#######################################################################
#                          Games Parameters                           #
#######################################################################

# Types of throws and their id :\t on heroku server


class GameEventAction:
    # Types of events defined on heroku server
    # Block
    # Dish
    # Dump
    # Huck throwaway
    # Pass
    # Pull
    # Score
    # Swing
    pass


# \t: number mapings
# \r: receiver
# \l: lineup
# \x: disc absolute position in x
# \y: disc absolut position in y
# \s: ???





class HerokuPlay:
    OLineIndex = 1
    DLineIndex = 2
    Pull = 3
    #  Block = 5
    PointIncompleteEndQuarterOffense = 5 #?
    ThrowawayCaused = 8 # block
    Throwaway = 9
    EndOfQ1 = 23
    EndOfQ2 = 24
    EndOfQ3 = 25
    EndOfQ4 = 26
    PassCompleted = 20
    ScoredOn = 21
    Goal = 22
    TimeoutDefense = 40
    TimeoutOffense = 41

game_event_dict = {
    1: 'Offensive Point', # l is the lineup: list of player_id
    2: 'Defensive Point', # l is the lineup: list of player_id
    3: 'Pull', # r is the person who performed the pull
    5: 'Block', # r is the person who made the block
    8: 'Throw away',  # check previous player
    9: 'Throwaway Caused', # check 13
    #  10: '', 
    #  11: '', # always between 8,9
    12: 'call on the field?', # c is call type?
    13: 'switch from off to def?', # check 9
    14: 'Time Out called (we are on off)', # s is 
    15: 'Time Out called (we are on def)', # s is ? (not the time)
    19: 'Pass dropped', # r is the person who dropped the catch (thrower is prev)
    20: 'Pass Completed', # r is the person who caught the catch (thrower is prev)
    21: 'They score', # s is 
    22: 'We Score', # r is the person who scored the point
    23: 'End of Q1', 
    24: 'End of Q2', 
    25: 'End of Q3', 
    26: 'End of Q4', 
    #  27: 'End of OT1', 
    #  28: 'End of OT2', 
    40: 'Timeout: defense unit comes to the field', # l is lineup
    41: 'Timeout: offense unit comes to the field', # l is lineup
    #  42: '', # s is 
    #  43: '', # s is 
    44: 'Offside', # r is the person who made the offside (if we don't know who it is, then we dont have row['r'])
    50: 'Start Game', 
}


# sequence: 13, 54, 53, 21 (we)
        

