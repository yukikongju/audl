#!/usr/bin/env/python
"""
Endpoint wrappers for AUDL game schedule data.

Fetches game schedule information from the UFA stats API:
    https://www.backend.ufastats.com/web-v1/games?limit=10

Equivalent to the schedule shown at:
    https://theaudl.com/league/game-search

Four classes are provided for different filtering scopes:

- ``AllSchedule`` – every game ever played.
- ``SeasonSchedule`` – all games in a given season.
- ``TeamSeasonSchedule`` – all games for one team in a given season.
- ``TeamSeasonAgainstOpponentSchedule`` – games between two specific teams.

All classes expose a single ``get_schedule()`` method that returns a
``pandas.DataFrame``.

Usage
-----
>>> from audl.stats.endpoints.seasonschedule import (
...     SeasonSchedule, TeamSeasonSchedule,
...     AllSchedule, TeamSeasonAgainstOpponentSchedule,
... )
>>> SeasonSchedule(2022).get_schedule()
>>> TeamSeasonSchedule(2022, 'royal').get_schedule()
"""

import pandas as pd
import requests

#  import json
import sys

#  from bs4 import BeautifulSoup

from audl.stats.endpoints._base import Endpoint

#  old: https://audl-stat-server.herokuapp.com/web-api/games?limit=10&years=2022&teamID=alleycats
#  new: https://www.backend.audlstats.com/web-api/games?limit=10&years=2022&teamID=alleycats


class ScheduleEndpoint(Endpoint):
    """Base class for all schedule endpoint variants.

    Handles paginated fetching from the games API. Subclasses implement
    ``_get_prefix_url()`` to add their filter parameters (season, team, etc.)
    before the ``&page=N`` suffix that this class appends on each iteration.
    """

    def __init__(self):
        """Initialise with the UFA games base URL (10 results per page)."""
        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/games?limit=10")
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/games?limit=10"
        )

    def _get_prefix_url(self):
        """Return the base URL with all filter query parameters applied.

        ``get_schedule()`` appends ``&page=N`` to this string on each
        iteration. Subclasses override this to inject year, team, and
        opponent parameters.

        Returns
        -------
        str
            Fully-qualified URL prefix ready for page-number appending.
        """
        pass

    def get_schedule(self):
        """
        Function that fetch all games from prefix url.  This function will be called from the children class

        Returns
        -------
        schedule: pandas.DataFrame
            dataframe with all schedule infos


        """
        # get prefix url
        prefix_url = self._get_prefix_url()

        # fetch all games by fetching all pages
        i = 1
        has_games = True
        dfs = pd.DataFrame()
        while has_games:
            url = f"{prefix_url}&page={i}"
            print(url)
            try:
                page = requests.get(url)
            except BaseException:
                print("An error occured when fetching the data. Exiting...")
                sys.exit(1)
            results = page.json()
            games = results["games"]
            df = pd.json_normalize(games)
            if df.size == 0:
                has_games = False
            i = i + 1
            dfs = pd.concat([dfs, df], axis=0)

        return dfs


class AllSchedule(ScheduleEndpoint):
    """Schedule for every game across all seasons.

    Fetches from:
        https://www.backend.ufastats.com/web-v1/games?limit=10

    Examples
    --------
    >>> schedule = AllSchedule().get_schedule()
    """

    def __init__(self):
        super().__init__()

    def _get_prefix_url(self):
        """Return the base URL with no additional filters."""
        return self.base_url


class SeasonSchedule(ScheduleEndpoint):
    """Schedule for all games played in a single season.

    Parameters
    ----------
    season : int
        Four-digit season year, e.g. ``2022``.

    Examples
    --------
    >>> schedule = SeasonSchedule(2022).get_schedule()
    """

    def __init__(self, season):
        """
        Parameters
        ----------
        season : int
            Four-digit season year (e.g. ``2022``).
        """
        super().__init__()
        self.season = season

    def _get_prefix_url(self):
        """Return the base URL filtered to ``self.season``."""
        return f"{self.base_url}&years={self.season}"


class TeamSeasonSchedule(ScheduleEndpoint):
    """Schedule for all games played by one team in a given season.

    Parameters
    ----------
    season : int
        Four-digit season year, e.g. ``2022``.
    team : str
        Team external ID (e.g. ``'royal'``, ``'rush'``, ``'breeze'``).

    Examples
    --------
    >>> schedule = TeamSeasonSchedule(2022, 'breeze').get_schedule()
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
        super().__init__()
        self.season = season
        self.team = team

    def _get_prefix_url(self):
        """Return the base URL filtered to ``self.season`` and ``self.team``."""
        return f"{self.base_url}&years={self.season}&teamID={self.team}"


class TeamSeasonAgainstOpponentSchedule(ScheduleEndpoint):
    """Schedule for all matchups between two specific teams in a given season.

    Parameters
    ----------
    season : int
        Four-digit season year, e.g. ``2022``.
    team : str
        Team external ID of the primary team (e.g. ``'royal'``).
    opponent : str
        Team external ID of the opposing team (e.g. ``'rush'``).

    Examples
    --------
    >>> schedule = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()
    """

    def __init__(self, season, team, opponent):
        """
        Parameters
        ----------
        season : int
            Four-digit season year (e.g. ``2022``).
        team : str
            Primary team external ID (e.g. ``'royal'``).
        opponent : str
            Opposing team external ID (e.g. ``'rush'``).
        """
        super().__init__()
        self.season = season
        self.team = team
        self.opponent = opponent

    def _get_prefix_url(self):
        """Return the base URL filtered to season, team, and opponent."""
        return f"{self.base_url}&years={self.season}&teamID={self.team}&opposingTeamID={self.opponent}"


#  --------------------------------------------------------------------------


def main():
    schedule = SeasonSchedule(2022)
    print(schedule.get_schedule())


if __name__ == "__main__":
    main()
