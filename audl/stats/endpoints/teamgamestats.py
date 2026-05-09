#!/usr/bin/env/python
"""
Endpoint wrappers for AUDL per-game team statistics.

Fetches team-level box-score stats for individual games from:
    https://www.backend.ufastats.com/web-v1/team-game-stats?limit=20

Equivalent to the table shown at:
    https://theaudl.com/stats/team-game-stats

Three classes are provided:

- ``AllTeamGameStats`` – every team-game across all seasons.
- ``SeasonGameStats`` – all team-games for a specific season.
- ``TeamSeasonGameStats`` – all games for one team in a specific season.

All classes expose ``get_game_stats()`` which iterates pages automatically
and returns a single combined ``pandas.DataFrame``.

Usage
-----
>>> from audl.stats.endpoints.teamgamestats import (
...     AllTeamGameStats, SeasonGameStats, TeamSeasonGameStats,
... )
>>> TeamSeasonGameStats(2022, 'royal').get_game_stats()
"""

import sys
import pandas as pd
import requests
from audl.stats.endpoints._base import Endpoint

# old: https://audl-stat-server.herokuapp.com/web-api/team-game-stats?limit=20
# old: https://audl-stat-server.herokuapp.com/web-api/team-game-stats?limit=20&page=1&year=2021
# old: https://audl-stat-server.herokuapp.com/web-api/team-game-stats?limit=20&page=1&year=2021&team=cascades

#  new: https://www.backend.audlstats.com/web-api/team-game-stats?limit=20&page=1&year=2021&team=cascades


class TeamGameStatsEndpoint(Endpoint):
    """
    Fetching Team Game Stats from https://theaudl.com/stats/team-game-stats
    """

    def __init__(self, season, team):
        """
        Parameters
        ----------
        season: string or int
            choices: ['career', 2022, 2019, ..., 2012]
        team: string
            choices: ['all', 'aviators', ..., '<ext_team_id>']


        Examples
        --------
        >>> TeamGameStats('career', 'all')
        >>> TeamGameStats(2022, 'rush')

        """

        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/team-game-stats?limit=20")
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/team-game-stats?limit=20"
        )
        self.season = season
        self.team = team

    def get_game_stats(self, show_message=True):
        """
        Function that return game statistics

        Parameters
        ----------
        show_message: bool
            True by default. Print page when fetching

        Returns
        -------
        game_stats: pandas.DataFrame

        Examples
        --------
        >>> gamestats = AllTeamGameStats().get_game_stats()
        >>> gamestats = SeasonGameStats(2022).get_game_stats()
        >>> gamestats = TeamSeasonGameStats(2022, 'royal').get_game_stats()

        """
        suffix_url = self._get_suffix_url()

        # fetch all games by fetching all pages
        i = 1
        has_games = True
        dfs = pd.DataFrame()
        while has_games:
            url = f"{self.base_url}&page={i}{suffix_url}"
            if show_message:
                print(url)
            try:
                page = requests.get(url)
            except BaseException:
                print("An error occured when fetching the data. Exiting...")
                sys.exit(1)
            results = page.json()
            games = results["stats"]
            #  print(games)
            df = pd.json_normalize(games)
            if df.size == 0:
                has_games = False
            i = i + 1
            dfs = pd.concat([dfs, df], axis=0)

        return dfs

    def _get_suffix_url(self):
        """Return the query-string suffix appended after ``&page=N``.

        Subclasses override this to inject ``year`` and ``team`` filters.

        Returns
        -------
        str
            Query-string fragment, e.g. ``'&year=2022&team=royal'``, or ``''``
            for no additional filtering.
        """
        pass


class AllTeamGameStats(TeamGameStatsEndpoint):
    """Team-game stats for every game across all seasons.

    Examples
    --------
    >>> AllTeamGameStats().get_game_stats()
    """

    def __init__(self):
        """Initialise with no season or team filter."""
        super().__init__("career", "all")

    def _get_suffix_url(self):
        """Return an empty suffix (no year or team filter)."""
        return ""


class SeasonGameStats(TeamGameStatsEndpoint):
    """Team-game stats for every game played in a single season.

    Parameters
    ----------
    season : int
        Four-digit season year, e.g. ``2022``.

    Examples
    --------
    >>> SeasonGameStats(2022).get_game_stats()
    """

    def __init__(self, season):
        """
        Parameters
        ----------
        season : int
            Four-digit season year (e.g. ``2022``).
        """
        super().__init__(season, "all")

    def _get_suffix_url(self):
        """Return the year filter suffix."""
        return f"&year={self.season}"


class TeamSeasonGameStats(TeamGameStatsEndpoint):
    """Team-game stats for one team across all games in a given season.

    Parameters
    ----------
    season : int
        Four-digit season year, e.g. ``2022``.
    team : str
        Team external ID (e.g. ``'royal'``, ``'rush'``, ``'empire'``).

    Examples
    --------
    >>> TeamSeasonGameStats(2022, 'royal').get_game_stats()
    """

    def __init__(self, season, team):
        """
        Parameters
        ----------
        season : int
            Four-digit season year (e.g. ``2022``).
        team : str
            Team external ID (e.g. ``'royal'``).
        """
        super().__init__(season, team)

    def _get_suffix_url(self):
        """Return the year and team filter suffix."""
        return f"&year={self.season}&team={self.team}"
