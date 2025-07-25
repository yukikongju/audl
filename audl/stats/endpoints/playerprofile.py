#!/usr/bin/env/python

import pandas as pd
import requests
import sys

from bs4 import BeautifulSoup
from datetime import datetime

from audl.stats.endpoints._base import Endpoint
from audl.stats.static.constants import FIRST_SEASON_YEAR

#  old: https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=cbrock
#  old: https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID=cbrock&year=2022

#  new: https://www.backend.audlstats.com/web-api/roster-stats-for-player?playerID=abartlett
#  new: https://www.backend.audlstats.com/web-api/roster-game-stats-for-player?playerID=wbrandt&year=2022


class PlayerProfile(Endpoint):

    def __init__(self, player_id: str):
        #  super().__init__("https://audl-stat-server.herokuapp.com/web-api/roster-stats-for-player?playerID=")
        super().__init__(
            "https://www.backend.ufastats.com/web-v1/roster-stats-for-player?playerID="
        )
        self.player_id = player_id

    def _get_url(self):
        """
        Function that return complete url

        Returns
        -------
        url: string
            url of the heroku API request

        Examples
        --------
        >>> PlayerProfile('cbrock')._get_url()

        """
        return f"{self.base_url}{self.player_id}"

    def get_career_stats(self):
        """
        Function that return player regular and playoffs stats as a dataframe

        Returns
        -------
        career_stats: pandas.DataFrame
            dataframe with player regular and playoffs season stats

        Examples
        --------
        >>> PlayerProfile('cbrock').get_career_stats()
        """
        try:
            # create dataframe
            url = self._get_url()
            results = requests.get(url).json()
            df = pd.DataFrame(results["stats"])
            return df
        except BaseException:
            print("An error has occured when fetching regular season dataframe")
            sys.exit(1)

    def get_regular_seasons_career(self):
        """
        Function that return a player's regular season stats as dataframe

        Returns
        -------
        regular_season: pandas.DataFrame
            dataframe with player regular season stats


        Examples
        --------
        >>> PlayerProfile('cbrock').get_regular_seasons_career()

        """
        df = self.get_career_stats()
        df["player_ext_id"] = self.player_id
        regular_season = df[df["regSeason"]]  # check if regular season is True
        return regular_season

    def get_playoffs_career(self):
        """
        Function that returns a player's playoff stats as dataframe

        Returns
        -------
        playoffs: pandas.DataFrame
            dataframe with player playoffs stats


        Examples
        --------
        >>> PlayerProfile('cbrock').get_playoffs_career()

        """
        df = self.get_career_stats()
        playoffs = df[~df["regSeason"]]
        return playoffs

    def get_season_games_stats(self, year):
        """
        Function that returns stats per game in a given season

        Parameters
        ----------
        year: int
            season

        Returns
        -------
        season_games: pandas.DataFrame


        Examples
        --------
        >>> PlayerProfile('cbrock').get_season_games_stats(2022)

        """
        try:
            #  url = f"https://audl-stat-server.herokuapp.com/web-api/roster-game-stats-for-player?playerID={self.player_id}&year={year}"
            url = f"https://www.backend.ufastats.com/web-v1/roster-game-stats-for-player?playerID={self.player_id}&year={year}"
            results = requests.get(url).json()
            df = pd.DataFrame(results["stats"])
            df["ext_player_id"] = self.player_id
            return df
        except BaseException:
            print("An error has occured when fetching season stats dataframe")
            sys.exit(1)

    def get_career_games_stats(self):
        """
        Function that return dataframe of all games played by a player

        Returns
        -------
        career_games: pandas.DataFrame
            dataframe with all games played

        Examples
        --------
        >>> PlayerProfile('cbrock').get_career_games_stats()

        """
        df = pd.DataFrame()
        current_year = int(datetime.today().strftime("%Y"))
        for year in range(FIRST_SEASON_YEAR, current_year + 1):
            df_season = self.get_season_games_stats(year)
            df = pd.concat([df, df_season], axis=0)
        df["player_ext_id"] = self.player_id
        return df

    def get_personal_information(self) -> pd.DataFrame:
        """
        Function that returns dataframe with player metadata. Columns include
        the following:
        - Name
        - Team
        - Jersey Number
        - Height
        - Weight
        - College
        - Hometown
        - Bio

        ex: https://www.watchufa.com/league/players/mmcdonnel
        """
        BASE_URL = "https://www.watchufa.com/league/players"
        url = f"{BASE_URL}/{self.player_id}"

        try:
            response = requests.get(url)
        except Exception as e:
            raise ConnectionError(
                f"The following error occured when fetching {url}: {e}"
            )

        try:
            soup = BeautifulSoup(response.text)
            name = soup.find(
                "div", class_="audl-player-display-name"
            ).text.strip()
            team_position = soup.find(
                "div", class_="audl-player-current-team-position"
            ).text.strip()
            jersey_number = soup.find(
                "div", class_="audl-player-jersey-number"
            ).text.strip()

            # Extract personal stats
            stats = {}
            for item in soup.find_all("div", class_="audl-personal-stats-item"):
                label = item.find(
                    "span", class_="audl-personal-stats-label"
                ).text.strip()
                value = item.find(
                    "span", class_="audl-personal-stats-value"
                ).text.strip()
                stats[label] = value

            # Extract player bio text and hometown
            bio_paragraphs = soup.select(".audl-player-bio-text p")
            bio_text = " ".join(
                [p.text for p in bio_paragraphs if "Hometown:" not in p.text]
            )
            hometown = ""
            for p in bio_paragraphs:
                if "Hometown:" in p.text:
                    hometown = p.text.split("Hometown:")[-1].strip()

            # Combine all into a dictionary
            player_data = {
                "ext_player_id": self.player_id,
                "name": name,
                "team_position": team_position,
                "jersey_number": jersey_number,
                "height": stats.get("HEIGHT"),
                "weight": stats.get("WEIGHT"),
                "dob": stats.get("AGE/DOB"),
                "college": stats.get("COLLEGE"),
                "hometown": hometown,
                "bio": bio_text,
            }

            # Convert to DataFrame
            df = pd.DataFrame([player_data])
        except Exception as e:
            raise ValueError("An error occured when processing player metadata")

        return df


#  ------------------------------------------------------------------------


def main():
    #  player = PlayerProfile('bbergmeie')
    player = PlayerProfile("wbrandt")

    #  print(player.get_career_games_stats())
    print(player.get_career_stats())
    #  print(player.get_playoffs_career())
    #  print(player.get_regular_seasons_career())
    #  print(player.get_season_games_stats(2022))


if __name__ == "__main__":
    main()
