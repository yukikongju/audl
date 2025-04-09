#!/usr/bin/env/python

import pandas as pd
import json
import requests
import sys

from audl.stats.endpoints._base import Endpoint

#  old: https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20&year=2019&per=possessions&team=aviators
#  old: https://theaudl.com/stats/player-stats?page=2&per=possessions&team=aviators&year=2019

#  new: https://www.backend.audlstats.com/web-api/player-stats?limit=20


class PlayerStats(Endpoint):
    """class that download data from https://theaudl.com/stats/player-stats
    based on [Season], [Per], [Team]

    Parameters
    ----------
    season: string or int
        choices: ['career', 2022, 2019, ..., 2012]
    per: string
        choices: ['total', 'game']
    team: string
        choices: ['all', 'aviators', ..., '<ext_team_id>']
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
            choices: ['all', 'aviators', ..., '<ext_team_id>']


        Examples
        --------
        >>> PlayerStats('career', 'total', 'all')
        >>> PlayerStats(2022, 'minutes', 'breeze')

        """
        self.season = season
        self.per = per
        self.team = team
        #  super().__init__('https://audl-stat-server.herokuapp.com/web-api/player-stats?limit=20')
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/player-stats?limit=20"
        )

    def fetch_table(self, show_message=False):
        """
        Function that fetch stats for all players as dataframe

        Parameters
        ----------
        show_message: bool
            False by default. Print page number when fetching

        Returns
        -------
        players_df: pandas.DataFrame
            dataframe with all players stats for given season, per, team param

        Examples
        --------
        >>> PlayerStats('career', 'total', 'all').fetch_table(show_message=True)

        """
        hasPlayerLeft = True
        all_players = []
        page = 1
        # add all players
        while hasPlayerLeft:
            players = self._fetch_page_players_as_json(page, show_message)
            if not players:
                break
            all_players = all_players + players  # concatenating
            page = page + 1

        # turn json as dataframe
        df = pd.DataFrame(all_players)

        return df.drop_duplicates()

    def _get_url(self, page_num: int) -> str:
        """
        Function that return the url by concatening the base url with its page number

        Parameters
        ----------
        page_num: int
            page number of the url

        Returns
        -------
        url: string
            complete url of herodoku database requests

        Examples
        --------
        >>> PlayerStats(2019, 'possessions', 'aviators')._get_url(3)
        >>> https://www.backend.audlstats.com/stats/player-stats?page=3&per=possessions&team=aviators&year=2019


        """
        if self.season == "career" and self.team == "all":
            return f"{self.base_url}&page={page_num}&per={self.per}"
        elif self.season == "career":
            return f"{self.base_url}&page={page_num}&per={self.per}&team={self.team}"
        elif self.team == "all":
            return f"{self.base_url}&page={page_num}&year={self.season}&per={self.per}"
        return f"{self.base_url}&page={page_num}&year={self.season}&per={self.per}&team={self.team}"

    def _fetch_page_players_as_json(self, page_num, show_message=False):
        """
        Function that fetch players in page as json

        Parameters
        ----------
        page_num: int
            page number of the url
        show_message: bool
            False by default. True if we print message

        Returns
        -------
        player_json: json
            json document of player page request

        Examples
        --------
        >>> PlayerStats(2019, 'possessions', 'aviators')._fetch_page_players_as_json(3)

        """
        try:
            url = self._get_url(page_num)
            page = requests.get(url)
            results = page.json()
            players = results["stats"]
            if show_message:
                print(f"Fetching from {url}")
        except:
            print(f"An error has occured when fetching the data from {url}")
            sys.exit(1)

        return players

    def download_stats_as_dataframe(self, file_path_name, show_message=True):
        """
        Function that download players stats as csv file

        Parameters
        ----------
        file_path_name: string
            path were the file should be downloaded
        show_message: bool
            True by default. Print message when page has been fetched

        Returns
        -------
        flag: bool
            True is file has been downloaded successfully, else False

        Examples
        --------
        >>> PlayerStats(2019, 'possessions', 'aviators').download_stats_as_dataframe('../database/filename.csv')

        """
        flag = False
        try:
            df = self.fetch_table()
            df.to_csv(file_path_name, sep=",", index=False)
            print(f"Downloaded csv file at {file_path_name}")
            flag = True
        except:
            print("An error has occured when saving the file as csv")
        return flag


#  -----------------------------------------------------------------------------


def main():
    stats = PlayerStats(2022, "game", "aviators")
    print(stats.fetch_table())


if __name__ == "__main__":
    main()
