#!/usr/bin/env/python
"""
Endpoint wrapper for AUDL team season statistics.

Fetches aggregated team stats from the UFA stats API:
    https://www.backend.ufastats.com/web-v1/team-stats?limit=50

Equivalent to the table shown at:
    https://theaudl.com/stats/team

Usage
-----
>>> from audl.stats.endpoints.teamstats import TeamStats
>>> df = TeamStats('career', 'game', 'opponent').get_table()
"""

import sys
import pandas as pd
import requests
from audl.stats.endpoints._base import Endpoint


#  old: https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50&year=2019&perGame=true&opponent=true
#  new: https://www.backend.audlstats.com/web-api/team-stats?limit=50


class TeamStats(Endpoint):
    """Aggregated team statistics for a given season, per-unit, and side.

    Wraps ``GET /web-v1/team-stats`` on the UFA stats backend. Results mirror
    the table at https://theaudl.com/stats/team.

    Parameters
    ----------
    season : str or int
        ``'career'`` for all-time totals, or a specific year (e.g. ``2022``).
        Valid range: ``'career'``, 2012–present.
    per : str
        Aggregation unit. One of ``'total'`` (season totals) or ``'game'``
        (per-game averages).
    team : str
        Perspective. ``'team'`` for the team's own stats; ``'opponent'`` for
        opponent stats faced by each team.

    Examples
    --------
    >>> TeamStats('career', 'total', 'team').get_table()
    >>> TeamStats(2022, 'game', 'opponent').get_table()
    """

    def __init__(self, season, per, team):
        """
        Parameters
        ----------
        season: string or int
            choices: ['career', 2022, 2019, ..., 2012]
        per: string
            choices: ['total', 'game']
        team: string
            choices: ['team', 'opponent']


        Examples
        --------
        >>> TeamStats('career', 'total', 'team')
        >>> TeamStats(2022, 'game', 'opponent')

        """

        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50")
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/team-stats?limit=50"
        )

        self.season = season
        self.per = per
        self.team = team

    def get_table(self):
        """
        Function that return page results table as dataframe

        Returns
        -------
        df: pandas.DataFrame
            dataframe of all team stats


        Raises
        ------



        Examples
        --------
        >>> TeamStats(2019, 'game', 'opponent').get_table()

        """
        url = self._get_url()
        try:
            results = requests.get(url).json()
            teams = results["stats"]
            df = pd.DataFrame(teams)
        except Exception as e:
            print(
                f"The following error has occured when fetching the results from url {url}: {e}"
            )
            sys.exit(1)

        return df

    def _get_url(self):
        """
        Function that return complete url

        Returns
        -------
        url: string
            url of the heroku API request

        Examples
        --------
        >>> TeamStats(2019, 'game', 'opponent')._get_url()
        >>> https://audl-stat-server.herokuapp.com/web-api/team-stats?limit=50&year=2019&perGame=true&opponent=true

        """
        is_per_game = "true" if self.per == "game" else "false"
        is_opponent = "true" if self.team == "opponent" else "false"
        if self.season == "career":
            return f"https://www.backend.ufastats.com/web-api/team-stats?limit=50&perGame={is_per_game}&opponent={is_opponent}"
        else:
            return f"https://www.backend.ufastats.com/web-api/team-stats?limit=50&year={self.season}&perGame={is_per_game}&opponent={is_opponent}"


def main():
    team = TeamStats(2022, "total", "team")
    print(team.get_table())


if __name__ == "__main__":
    main()
