#!/usr/bin/env/python

import pandas as pd
import requests
import json 
import sys

from bs4 import BeautifulSoup

from audl.stats.endpoints._base import Endpoint
from audl.stats.library.parameters import game_schedule_columns_name
from audl.stats.library.parameters import FileName

#  https://audl-stat-server.herokuapp.com/web-api/games?limit=10&years=2022&teamID=alleycats

class SeasonSchedule(Endpoint):

    def __init__(self):
        super().__init__("https://audl-stat-server.herokuapp.com/web-api/games?limit=10")

    def _get_url(self, season, team, opponent):
        if team == None and season == None and opponent == None: # get_all_games_ever_played()
            return self.base_url
        elif opponent == None and team == None: # get_season_schedule()
            return f"{self.base_url}&years={season}"
        elif opponent == None: # get_team_season_schedule()
            return f"{self.base_url}&years={season}&teamID={team}"
        else: # get_team_season_schedule_against_opponent()
            return f"{self.base_url}&years={season}&teamID={team}&opposingTeamID={opponent}"


    def _fetch_data_from_url(self, url):
        try:
            page = requests.get(url)
            results = page.json()
            games = results['games']
            df = pd.json_normalize(games)
        except:
            print(f'An error occured when fetching the data. Exiting...')
            sys.exit(1)
        return df
        
    def get_all_games_ever_played(self):
        """ 
        Fetch all games played ever
        return [df]
        """
        url = self._get_url(None, None, None)
        df = self._fetch_data_from_url(url)
        return df


    def get_season_schedule(self, season):
        """ 
        Fetch all games played in a season (all teams)
        param [season]
        return [df]
        """
        url = self._get_url(season, None, None)
        df = self._fetch_data_from_url(url)
        return df

    def get_team_season_schedule(self, team, season):
        """ 
        Fetch all games played by a team in a given season
        param [team] : team_id
        param [season]: year 
        return [df]
        """
        url = self._get_url(season, team, None)
        df = self._fetch_data_from_url(url)
        return df

    def get_team_season_schedule_against_opponent(self, season, team, opponent):
        """ 
        Fetch all games played by a team against opponent in a given season
        param [team] : team_id
        param [season]: year 
        param [opponent]: opponent
        return [df]
        """
        url = self._get_url(season, team, opponent)
        df = self._fetch_data_from_url(url)
        return df


#  class SeasonSchedule(Endpoint):

#      def __init__(self):
#          super().__init__("https://theaudl.com/league/schedule/week-")

#      def _get_url(self, page: int) -> str:
#          return f"{self.base_url}{page}"

#      def _get_response(self, url: str) ->list:
#          return requests.get(url)

#      def _fetch_page_games(self, soup: list) -> list:
#          links = soup.findAll('span', {"class": "audl-schedule-gc-link"} )
#          times = soup.findAll('span', {"class": "audl-schedule-start-time-text"} )
#          locations = soup.findAll('td', {"class": "audl-schedule-location"} )
#          teams = soup.findAll('td', {"class": "audl-schedule-team-name"} )
#          scores = soup.findAll('td', {"class": "audl-schedule-team-score"} )
#          games = []

#          # get value inside tags
#          stadiums = [location.text.strip() for location in locations]

#          i = 0 # index to keep track of teams
#          for index, _ in enumerate(locations):
#              # find game id
#              href = links[index].find('a')['href']
#              game_id = href.replace('/league/game/', '')

#              # find game time
#              time = times[index].text

#              # find stadium
#              stadium = stadiums[index]

#              # find home team
#              away_team = teams[i].text
#              away_score = scores[i].text
#              i += 1

#              # find away team
#              home_team = teams[i].text
#              home_score = scores[i].text
#              i += 1

#              # add game to data
#              game = [away_team, home_team, time, stadium, game_id, away_score, home_score]
#              games.append(game)
#          return games

#      def get_season_schedule_df(self):
#          has_game_left = True
#          page = 1
#          data = []
#          while(has_game_left):
#              # fetch games from page url
#              url = self._get_url(page)
#              response = self._get_response(url)
#              soup = BeautifulSoup(response.text, "lxml")
#              game_divs = soup.findAll('table', {"class":"audl-schedule-box"})
#              # check if there are games in page
#              if not game_divs:
#                  has_game_left = False
#                  break

#              # fetch games in pages
#              games = self._fetch_page_games(soup)
#              data.append(games)
#              page += 1
#          data = SeasonSchedule._flatten_3D_to_2D(data)
#          df = pd.DataFrame(data, columns = game_schedule_columns_name)
#          return df

#      def download_season_schedule_as_csv(self):
#          df = self._get_season_schedule_df()
#          file_name = f"{FileName.seasonschedule}_.csv"
#          df.to_csv(file_name, sep=',', index=False)

#      @staticmethod
#      def _flatten_3D_to_2D(data: list) -> list:
#          return [item for sublist in data for item in sublist]

