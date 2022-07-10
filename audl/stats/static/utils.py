

def get_all_players():
    pass
    
def get_quarter(scoring_time):
    """ 
    Function that returns quarter based on scoring time

    Remark: Games are timed with four-quarters of 12 minutes each, 
        including a 15-minute halftime. If the score is tied, a five 
        minutes overtime period is played. If the score remains tied after
        overtime, a second overtime is played in which the first team 
        to score wins.

    Parameters 
    ----------
    scoring_time: int
        time when point was scored in second

    Returns
    -------
    quarter: string 
        ex: 'Q1', 'Q2', 'Q3', 'Q4', 'OT1', 'OT2'
        
    Examples
    --------
    >>> GameStats()._get_quarter(456)

    """
    quarter_end = { 'Q1': 720, 'Q2': 1440, 'Q3': 2160, 'Q4': 2880, 'OT1': 3180 }

    for quarter, end_time in quarter_end.items():
        if scoring_time < end_time:
            return quarter

    return 'OT2'
