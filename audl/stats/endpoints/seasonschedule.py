#!/usr/bin/env/python

import pandas as pd
import requests

#  import json
import sys

#  from bs4 import BeautifulSoup

from audl.stats.endpoints._base import Endpoint

#  old: https://audl-stat-server.herokuapp.com/web-api/games?limit=10&years=2022&teamID=alleycats
#  new: https://www.backend.audlstats.com/web-api/games?limit=10&years=2022&teamID=alleycats


class ScheduleEndpoint(Endpoint):

    def __init__(self):
        """"""
        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/games?limit=10")
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/games?limit=10"
        )

    def _get_prefix_url(self):
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

    def __init__(self):
        """
        Examples
        --------
        >>> schedule = AllSchedule().get_schedule()

        """
        super().__init__()

    def _get_prefix_url(self):
        return self.base_url


class SeasonSchedule(ScheduleEndpoint):

    def __init__(self, season):
        """
        Examples
        --------
        >>> schedule = SeasonSchedule(2022).get_schedule()

        """
        super().__init__()
        self.season = season

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}"


class TeamSeasonSchedule(ScheduleEndpoint):

    def __init__(self, season, team):
        """
        Examples
        --------
        >>> schedule = TeamSeasonSchedule(2022, 'breeze').get_schedule()

        """
        super().__init__()
        self.season = season
        self.team = team

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}&teamID={self.team}"


class TeamSeasonAgainstOpponentSchedule(ScheduleEndpoint):

    def __init__(self, season, team, opponent):
        """
        Examples
        --------
        >>> schedule = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()

        """
        super().__init__()
        self.season = season
        self.team = team
        self.opponent = opponent

    def _get_prefix_url(self):
        return f"{self.base_url}&years={self.season}&teamID={self.team}&opposingTeamID={self.opponent}"


#  --------------------------------------------------------------------------


def main():
    schedule = SeasonSchedule(2022)
    print(schedule.get_schedule())


if __name__ == "__main__":
    main()
