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

def get_throw_type(x1, y1, x2, y2):
    """ 
    Get complete information on the throw

    - throwing_type: pass, dump, swing, huck, dish
    - throw_side: right, left
    - distance: float
    - angle: float

    """
    # compute angle
    x_delta, y_delta = x2 - x1, y2 - y1
    throw_dist = math.sqrt(x_delta**2 + y_delta**2)
    angle_degrees = math.degrees(math.atan(y_delta / (x_delta + 0.001)))

    # compute throw_type
    threshold_lateral = 15
    threshold_vertical = 40
    if (x_delta == 0.0) and (y_delta == 0.0):
        throw_type = 'stall'
    elif -threshold_lateral <= angle_degrees <= threshold_lateral and y_delta <= 0:
        throw_type = 'swing'
    elif -threshold_lateral <= angle_degrees <= threshold_lateral and y_delta > 0: 
        throw_type = 'dish'
    elif y_delta > 40:
        throw_type = 'huck'
    elif y_delta <= 0 and abs(angle_degrees) > threshold_lateral:
        throw_type = 'dump'
    else: 
        throw_type = 'pass'

    # compute throw side
    if angle_degrees >=0 : 
        throw_side = 'right'
    else:
        throw_side = 'left'

    # rounding
    signif_number = 3
    x_delta, y_delta = round(x_delta, signif_number), round(y_delta, signif_number)
    throw_dist = round(throw_dist, signif_number)

    return throw_type, throw_side, throw_dist, x_delta, y_delta, angle_degrees


#  def get_throw_type(x1, y1, x2, y2, event_type): # deprecated
#      """ 
#      Function that returns throwing type from coordinates

#      Parameters
#      ----------
#      x1, x2: int
#          distance in x-axis in meters
#      y1, y2: int
#          distance in y-axis in meters

#      Returns 
#      -------
#      throwing_type: string
#          pass, huck, swing, dump, dish, throwaway, drop

#      Notes
#      -----
#          What's the difference between swing and dish
#      """
#      x, y = x2 - x1, y2 - y1
#      dist = math.sqrt(x**2 + y**2)
#      #  angle = math.sin(x/y)

#      if event_type == 8:
#          return "throwaway"
#      elif event_type == 19:
#          return "drop"
#      elif dist >= 40:
#          return "huck"
#      elif y <= 0: 
#          return "dump"
#      elif y <= 5: 
#          return "swing"
#      else: 
#          return "pass"


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
    
