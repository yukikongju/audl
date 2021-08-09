#!/usr/bin/env/python

import pandas as pd
import requests
from bs4 import BeautifulSoup

from audl.stats.endpoints._base import Endpoint
from audl.stats.static.teams import find_team_name_from_full_name
from audl.stats.library.parameters import game_schedule_columns_name

class TeamSeasonSchedule(Endpoint):

    def __init__(self, full_name: str ):
        super().__init__("https://theaudl.com/")
        self.full_name = full_name
        self.team_name_id = find_team_name_from_full_name(self.full_name).lower()
        self.endpoint = self._get_endpoint()
        self.url = self._get_url()


    def _get_endpoint(self):
        return f"{self.team_name_id}/schedule"

    def _get_response(self):
        return requests.get(self.url)

    def _get_team_games_id(self):
        response = self._get_response()
        soup = BeautifulSoup(response.text, "lxml")
        spans = soup.findAll('span', {"class": "audl-schedule-gc-link"})
        games_id =[]
        for index, span  in enumerate(spans):
            href = span.find('a')['href']
            game_id = href.replace(f"/{self.team_name_id}/game/","")
            games_id.append(game_id)
        return games_id

    def get_team_schedule(self):
        response = self._get_response()
        soup = BeautifulSoup(response.text, "lxml")
        # fetch page
        links = soup.findAll('span', {"class": "audl-schedule-gc-link"} )
        times = soup.findAll('span', {"class": "audl-schedule-start-time-text"} )
        locations = soup.findAll('td', {"class": "audl-schedule-location"} )
        teams = soup.findAll('td', {"class": "audl-schedule-team-name"} )
        scores = soup.findAll('td', {"class": "audl-schedule-team-score"} )
        data = []
        i = 0 # index to keep track of teams
        for index, _ in enumerate(locations):
            # find game id
            href = links[index].find('a')['href']
            game_id = href.replace(f"/{self.team_name_id}/game/","")

            # find game time
            time = times[index].text

            # find stadium
            stadium = locations[index].find('a')['href']

            # find home team
            away_team = teams[i].text
            away_score = scores[i].text
            i += 1

            # find away team
            home_team = teams[i].text
            home_score = scores[i].text
            i += 1

            # add game to data
            game = [away_team, home_team, time, stadium, game_id, away_score, home_score]
            data.append(game)
        # create dataframe
        df = pd.DataFrame(data, columns=game_schedule_columns_name)
        return df



