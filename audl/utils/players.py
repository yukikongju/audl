"""
Utilities for fetching AUDL player identifiers.

Player external IDs (e.g. ``'cbrock'``, ``'mmcdonnel'``) are the string keys
used across every endpoint in this library. This module provides helpers for
fetching them in bulk from:
    https://www.watchufa.com/league/players
"""

import requests

from typing import List


def get_all_players_ext_ids():
    """Fetch all player external IDs by scraping the UFA player directory.

    Iterates the player listing at:
        https://www.watchufa.com/league/players

    Returns
    -------
    list of str
        Player external IDs (e.g. ``['cbrock', 'mmcdonnel', ...]``). Returns
        ``None`` until implemented.

    Notes
    -----
    Not yet implemented. For a working alternative that pulls IDs from the
    stats API, use ``audl.stats.endpoints.utils.get_all_players_ext_ids()``.
    """
    base_url = "https://www.watchufa.com/league/players"
    pass
