import math

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

def get_throw_type(x1, y1, x2, y2, event_type): # FIXME: dish?
    """ 
    Function that returns throwing type from coordinates

    Parameters
    ----------
    x1, x2: int
        distance in x-axis in meters
    y1, y2: int
        distance in y-axis in meters

    Returns 
    -------
    throwing_type: string
        pass, huck, swing, dump, dish, throwaway, drop

    Notes
    -----
        What's the difference between swing and dish
    """
    x, y = x2 - x1, y2 - y1
    dist = math.sqrt(x**2 + y**2)
    #  angle = math.sin(x/y)

    if event_type == 8:
        return "throwaway"
    elif event_type == 19:
        return "drop"
    elif dist >= 40:
        return "huck"
    elif y <= 0: 
        return "dump"
    elif y <= 5: 
        return "swing"
    else: 
        return "pass"


def get_throwing_distance(x1, y1, x2, y2):
    """ 
    Function that return distance from thrower and receiver

    Parameters
    ----------
    x1, x2: int
        distance in x-axis in meters
    y1, y2: int
        distance in y-axis in meters

    Returns 
    -------
    distance: double
        distance between thrower and receiver
    """
    x, y = x2 - x1, y2 - y1
    return  math.sqrt(x**2 + y**2)
    
def get_throw_angle(x1, y1, x2, y2):
    """ 
    Function that return throwing angle
    """
    x, y = x2 - x1, y2 - y1
    return math.sin(x/y)
    
