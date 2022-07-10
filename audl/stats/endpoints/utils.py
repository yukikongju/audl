from audl.stats.endpoints.playerstats import PlayerStats
import pandas as pd


def get_all_players_ext_ids(show_message=False):
    """ 
    Function that retrieves all players external id as list

    Fetching all 'playerID' from AUDL player's page at https://theaudl.com/stats/player-stats

    url: https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20&page=2

    Parameters
    ----------
    show_message: bool
        False by default. Print page number when fetching

    Returns
    -------
    players_ext_ids: list
        list of players_ext_ids

    Examples
    --------
    >>> from audl.stats.endpoints.utils import get_players_ext_id()
    >>> get_players_ext_ids()
    >>> ['rgross', 'kplew', ...]
    """
    df = PlayerStats('career', 'total', 'all').fetch_table(show_message)
    return(df['playerID'].tolist())



    
