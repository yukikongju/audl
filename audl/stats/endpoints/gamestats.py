#!/usr/bin/env/python

import json
import math
import pandas as pd
import numpy as np
import requests

from audl.stats.endpoints._base import Endpoint
from audl.stats.endpoints.playerprofile import PlayerProfile

from audl.stats.library.game_event import GameEventSimple, GameEventLineup, GameEventReceiver
from audl.stats.static.utils import get_quarter, get_throw_type, get_throwing_distance

#  old: https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TOR-MTL
#  new: https://www.backend.audlstats.com/stats-pages/game/2022-07-31-DET-MIN


class GameStats(Endpoint):

    def __init__(self, game_id: str):
        super().__init__("https://www.backend.audlstats.com/stats-pages/game/")
        self.game_id = game_id
        self.json = self._get_json_from_url()
        self.home_team = self._get_home_team_ext_id()
        self.away_team = self._get_away_team_ext_id()

    def _get_home_team_ext_id(self):
        """ 
        Function that return team external id for home team

        Returns
        -------
        ext_team_id: string
            External Team ID (ex: 'royal', 'rush', ...)

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_home_team_ext_id()

        """
        return self.json['game']['team_season_home']['team']['ext_team_id']
        
    def _get_away_team_ext_id(self):
        """ 
        Function that return team external id for away team

        Returns
        -------
        ext_team_id: string
            External Team ID (ex: 'royal', 'rush', ...)

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_away_team_ext_id()

        """
        return self.json['game']['team_season_away']['team']['ext_team_id']

    def _get_url(self):
        """ 
        Function that return complete url

        Returns
        -------
        url: string
            url of the heroku API request
        
        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_url()

        """
        return f"{self.base_url}{self.game_id}"
    

    def _get_json_from_url(self):
        """ 
        Function that retrieves requests data as JSON document

        Returns 
        -------
        json_doc: json
            json document from the get requests

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_json_from_url()

        """
        url = self._get_url()
        return requests.get(url).json()

    def get_game_metadata(self):
        """ 
        Function that retrieve game metadata

        Returns
        ------- 
        game_metadata: pandas.Dataframe
            Dataframe with the following columns
                - is_regular_season (bool)
                - home_team, away_team
                - home_score, away_score
                - stadium_name (from location_id)

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_game_metadata()

        """
        game = self.json['game']
        df = pd.json_normalize(game)
        return df

    def get_boxscores(self):
        """ 
        Function that return team scores by quarter
        
        Returns
        -------
        df_boxscores: pandas.DataFrame
            Dataframe with team goals by quarter 


        Examples
        --------
        The dataframe should look like this

                    Q1	Q2	Q3	Q4	T
            rush	4	6	4	7	21
            royal	4	7	4	5	20

        >>> GameStats('2022-06-11-TB-ATL').get_boxscores()

        """
        # get scoring times from json 
        scores = self._get_scoring_time()

        # pivot table
        scores = scores.pivot_table(values='scoring_time', 
                index='ext_team_id', columns=['quarter'], aggfunc=np.count_nonzero)

        # add total column
        scores['T'] = scores[list(scores.columns)].sum(axis=1)

        return scores

    def _get_scoring_time(self):
        """ 
        Function that return scoring time for each team

        Returns 
        -------
        scorin_time: pandas.DataFrame   
            Dataframe with the following columns:
                - scoring_time (int): time when point was scored in second
                - ext_team_id (string): team external id ie 'royal'
                - quarter (string): quarter in which point has been scored ie 'Q1'

        Examples
        --------
        The dataframe should look like this

                    scoring_time ext_team_id   quarter
           rush             353         231         Q1
           rush             586         231         Q1
           royal            786         231         Q2

        >>> GameStats('2022-06-11-TB-ATL')._get_scoring_time()

        """
        # get scoring time for both teams
        score_times_home = self.json['game']['score_times_home'][1:]
        score_times_away = self.json['game']['score_times_away'][1:]

        # create dataframes
        home_df = pd.DataFrame(score_times_home, columns=['scoring_time'])
        away_df = pd.DataFrame(score_times_away, columns=['scoring_time'])
        home_df['ext_team_id'] = self._get_home_team_ext_id()
        away_df['ext_team_id'] = self._get_away_team_ext_id()
        scores = pd.concat([home_df, away_df])
        
        # calculate quarter columns
        scores['quarter'] = scores['scoring_time'].apply(
                lambda x: get_quarter(x))

        return scores

        
    def get_scores(self):
        """ 
        Function that retrieves scores by times

        Returns
        -------
        scores_df: pandas.DataFrame 
            Dataframe with the following columns:
                - team: "home" or "away"
                - time: time when the team scored
                - goal: who scored the goal
                - assist: who assisted the goal
                - hockey: who made the hockey pass

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_scores()

        """
        raise NotImplementedError("This function hasn't been implemented yet!")
        pass

    def get_roster_stats(self):
        """ 
        Function that retrieves stats for all players that played this games
        
        Returns
        -------
        roster_df: pandas.Dataframe
            Dataframe with roster stats

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_roster_stats()

        """
        # get external ids for all players that played
        roster_ext_ids = self._get_roster_ext_ids()

        roster_stats = pd.DataFrame()
        for player_id in roster_ext_ids:
            # get all games played in game's season
            #  print(player_id)
            player = PlayerProfile(player_id)
            year = self._get_season_from_game_id()
            games = player.get_season_games_stats(year) # FIXME: game info is not there anymore
            #  print(games)

            # filter by gameID and add player_id, city_id
            player_stat = games[games['gameID'] == self.game_id] 
            player_stat['ext_player_id'] = player_id
            # FIXME: use .iloc instead #  is_home = player_stat.at[0,'isHome']
            is_home = player_stat['isHome'].values[0]
            player_stat['team_abbrev'] = self._get_city_abbrev_from_game_id(is_home)

            roster_stats = pd.concat([roster_stats, player_stat])

        # change columns order
        roster_stats.insert(0, 'ext_player_id', roster_stats.pop('ext_player_id'))
        roster_stats.insert(1, 'team_abbrev', roster_stats.pop('team_abbrev'))

        return roster_stats

    def _get_city_abbrev_from_game_id(self, is_home):
        """ 
        Function that return season from game_id

        Parameters
        ----------
        is_home: bool 
            True if home, False if away


        Returns
        -------
        season : int 
            season year (ex: 2022)


        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_city_abbrev_from_game_id(True)
        >>> IND
        >>> GameStats('2022-06-11-TB-ATL')._get_city_abbrev_from_game_id(False)
        >>> ATL

        """
        if is_home:
            return self.game_id.split('-')[4]
        else:
            return self.game_id.split('-')[3]
        


    def _get_season_from_game_id(self):
        """ 
        Function that return season from game_id 

        Returns
        -------
        season : int
            season year 


        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_season_from_game_id()
        >>> 2022

        """
        return int(self.game_id.split('-')[0])


        
    def _get_roster_ext_ids(self):
        """ 
        Function that return all players that played this game (rosterIds)

        Returns
        -------
        roster_ext_ids: list
            List of ext_player_id 

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._get_roster_ext_ids()
        >>> ['pbisson', 'thodge']

        """
        # get all player_id who have played as list
        rosterHome = self.json['tsgHome']['rosterIds']
        rosterAway= self.json['tsgAway']['rosterIds']
        roster_ids = rosterHome + rosterAway

        # get player_ext_ids
        players = self.get_players_metadata()
        roster_df = players[players['id'].isin(roster_ids)]
        ext_player_ids = roster_df['player.ext_player_id'].tolist()

        return ext_player_ids


    def get_team_stats(self):
        """ 
        Function that retrieves teams stats

        Returns
        -------
        team_stats: pandas.DataFrame
            Dataframe with the following columns:

           'id', 'teamSeasonId', 'gameId', 'source', 'startOnOffense',
           'updateMoment', 'statusId', 'completionsNumer', 'completionsDenom',
           'hucksNumer', 'hucksDenom', 'blocks', 'turnovers', 'oLineScores',
           'oLinePoints', 'oLinePossessions', 'dLineScores', 'dLinePoints',
           'dLinePossessions', 'redZoneScores', 'redZonePossessions', 'road',
           'completionsPerc', 'hucksPerc', 'holdPerc', 'oLineConversionPerc',
           'dLineConversionPerc', 'breakPerc', 'redZoneConversionPerc'

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_team_stats()

        """
        tsg_home = self._read_teams_tsg_json(self.json['tsgHome'])
        tsg_home['road'] = 'home'
        tsg_home['team'] = self.home_team
        tsg_away = self._read_teams_tsg_json(self.json['tsgAway'])
        tsg_away['road'] = 'away'
        # concatenate home and away dataframes
        tsg = pd.concat([tsg_home, tsg_away])

        # calculate percentage columns
        tsg['completionsPerc'] = tsg['completionsNumer'] / tsg['completionsDenom'] 
        tsg['hucksPerc'] = tsg['hucksNumer'] / tsg['hucksDenom'] 
        tsg['holdPerc'] = tsg['oLineScores'] / tsg['oLinePoints'] 
        tsg['oLineConversionPerc'] = tsg['oLineScores'] / tsg['oLinePossessions'] 
        tsg['dLineConversionPerc'] = tsg['dLineScores'] / tsg['dLinePossessions'] 
        tsg['breakPerc'] = tsg['dLineScores'] / tsg['dLinePoints'] 
        tsg['redZoneConversionPerc'] = tsg['redZoneScores'] / tsg['redZonePossessions'] 

        return tsg


    def _read_teams_tsg_json(self, team_tsg):
        """ 
        Function that retrieves scoring information in json.tsgHome or json.tsgAway

        Parameters
        ----------
        team_tsg: json 
            json dictionary of tsgHome or tsgAway

        Returns
        -------
        tsg_df: pandas.DataFrame
            dataframe of the tsg
            
        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL')._read_teams_tsg_json(self.json['tsgHome'])
        >>> GameStats('2022-06-11-TB-ATL')._read_teams_tsg_json(self.json['tsgAway'])

        """
        # read json
        tsg = pd.json_normalize(team_tsg, max_level=1)

        # drop columns
        cols_to_drop = [
                'events', 
                'scoreTimesOur',
                'scoreTimesTheir',
                'rosterIds'
            ]
        tsg = tsg.drop(cols_to_drop, axis=1)

        return tsg


    def get_players_metadata(self):
        """ 
        Function that retrieves all players from both team (even those who 
        are not playing)

        Returns
        -------
        players_metadata: pandas.DataFrame
            Dataframe with all data from json.rostersHome and json.rostersAway
                - player_game_id: id used in events
                - jersey_number
                - player_id
                - first_name:
                - last_name
                - ext_player_id: 'pbisson'
                - ext_team_id: 'royal'
                - city

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_players_metadata()

        """
        # get home and away roster
        homeJSON = self.json['rostersHome']
        home_players = pd.json_normalize(homeJSON)
        home_players['road'] = 'home'
        home_players['team'] = self.home_team
        awayJSON = self.json['rostersAway']
        away_players = pd.json_normalize(awayJSON)
        away_players['road'] = 'away'
        away_players['team'] = self.away_team

        # concatenate dataset
        players = pd.concat([home_players, away_players])
        return players 

    def get_teams_metadata(self):
        """ 
        Function that retrieve team and city name for home and away team

        Returns
        -------
        teams_metadata: pandas.DataFrame
            Datafram with all data from games.team_season_home and games.team_season_away
                - team_season_id
                - team_id
                - city: 'Monteal'
                - city_abbrev: 'MTL'
                - name: 'Royal'
                - ext_team_id: 'royal'

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_teams_metadata()

        """
        # retrieve df from home and away team
        game = self.json['game']
        home = pd.json_normalize(game['team_season_home'])
        away = pd.json_normalize(game['team_season_away'])
        home['road'] = 'home'
        away['road'] = 'away'

        # concatenate home and away dataframes
        teams = pd.concat([home, away])
        return teams

    def get_lineup_by_points(self): 
        """ 
        Function that returns lineup for each point played

        Returns
        -------
        points_results: json
            [
                {'point': 1,
                'offensive_team': royal, 
                'defensive_team': rush, 
                'offensive_lineup': [1096, ...],
                'defensive_lineup': [1056, ...],
                'outcome': royal
                }
            ]

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_lineup_by_points()
        """
        # retrieve events from json
        home_events = json.loads(self.json['tsgHome']['events'])
        away_events = json.loads(self.json['tsgAway']['events'])

        num_home_events = len(home_events)
        num_away_events = len(away_events)
        i, j = 0, 0


        # find lineups index for home and away team
        index_home, index_away = [], []
        while i < num_home_events and j < num_away_events:
            while i < num_home_events and home_events[i]['t'] not in [1, 2] : i += 1
            while j < num_away_events and away_events[j]['t'] not in [1, 2] : j += 1

            try:
                index_home.append(i)
                index_away.append(j)
            except:
                break

            i += 1
            j += 1

        # generate json lineups
        outcomes_home = [i-1 for i in index_home[1:]]
        outcomes_away = [i-1 for i in index_away[1:]]
        outcomes_home.append(num_home_events-2)
        outcomes_away.append(num_away_events-2)

        num_points = min(len(index_home), len(index_away), len(outcomes_home), len(outcomes_away))

        # FIXME: why does winner team has one more entries than losing team
        all_lineups = []
        for i in range(num_points-1):
            lineup_home = home_events[index_home[i]]['l']
            lineup_away = away_events[index_away[i]]['l']

            #  get outcome: t==21, t==22
            home_outcome = home_events[outcomes_home[i]]['t']
            if home_outcome == 21: # home lost point
                outcome = self.away_team
            elif home_outcome == 22: # home win
                outcome = self.home_team
            else:
                outcome = 'incomplete'

            point = i+1

            if home_events[i]['t'] == 1: # home team starts in offense
                lineup = {
                        'point': point,
                        'offense': self.home_team,
                        'defense': self.away_team, 
                        'lineup_offense': lineup_home,
                        'lineup_defense': lineup_away,
                        'outcome': outcome
                }
            else:
                lineup = {
                        'point': point,
                        'offense': self.away_team,
                        'defense': self.home_team, 
                        'lineup_offense': lineup_away,
                        'lineup_defense': lineup_home,
                        'outcome': outcome
                }

            all_lineups.append(lineup)

        return all_lineups



    def get_point_results(self): 
        """ 
        Function that returns (events) in a given point for a given team

        Parameters
        ----------
        None

        Returns
        -------


        More:
            json doc with the following information
            - team_on_off (string): team on offense (ext_team_id)
            - team_on_def (string): team on defense (ext_team_id)
            - lineup_off (list): lineup in off (7 players) (t:1)
            - lineup_def (list): lineup in def (7 players) (t:2)
            - result (string): ext_team_id of team who won the point
            - scorer (string): ext_player_id of person who scored the point (t:22)
            - assist (string): ext_player_id of person who assisted (prev t:20)
            - hockey (string): ext_player_id of person who made the hockey assist 
            - catcher (string): ext_player_id of player who caught the pull
            - center (string): ext_player_id of player who caught the second pass
            - scoring_time (int):
            - timeout_called (bool): True if timeout was called

        """
        raise NotImplementedError("This function hasn't been implemented yet!")
        

    def get_events_sequential(self):
        """ 
        Function that return the event of each points in sequential order

        Returns
        -------
        events_df: pandas.DataFrame
            Dataframe with the following columns:
                - point (int): ith point played
                - team_on_off (string): team on offense
                - team_on_def (string): team on defense
                - lineup_def (list): lineup in def (7 players)
                - lineup_off (list): lineup in off (7 players)

        
        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').get_events()

        """
        raise NotImplementedError("This function hasn't been implemented yet!")

    def get_events(self):
        """ 
        Function that fetch all events for all points for each team
        """

        # retrieve events from json
        home_events = json.loads(self.json['tsgHome']['events'])
        away_events = json.loads(self.json['tsgAway']['events'])

        # get events by points
        home_points = self._get_team_events_by_points(home_events)
        away_points = self._get_team_events_by_points(away_events)

        events_dict = {'homeEvents': home_points, 'awayEvents': away_points}

        return events_dict

    def get_all_events(self):
        """ 
        Function that fetch all events (raw) for home and away team for each team
        """

        # retrieve events from json
        home_events = json.loads(self.json['tsgHome']['events'])
        away_events = json.loads(self.json['tsgAway']['events'])

        events_dict = {'homeEvents': home_points, 'awayEvents': away_points}

        return events_dict

        
    def _get_team_events_by_points(self, events):
        """ 
        Function that return a list of dict with all points events

        Parameters
        ----------
        events: json dict
            self.json['tsgHome']['events'] or self.json['tsgAway']['events']

        Examples
        --------
        >>> 
        >>> [{'point': 0, 'events': []},
        >>>  {'point': 1,
        >>>    'events': [{'t': 1, 'l': [9246, 9237, 9323, 9262, 9241, 9568, 9242]},
        >>>     {'t': 20, 'r': 9262, 'x': 12.89, 'y': 18.93},
        >>>     {'t': 20, 'r': 9246, 'x': 4, 'y': 33.13},
        >>>     {'t': 20, 'r': 9323, 'x': 20.47, 'y': 47.18},
        >>>     {'t': 20, 'r': 9262, 'x': 0.94, 'y': 43.83},
        >>>     ...

        """
        point_played = 0
        all_events, point_events = [], []
        for i, event in enumerate(events):
            event_type = int(event['t'])
            if event_type not in [1,2]:
                point_events.append(event)
            else:
                all_events.append({'point': point_played, 'events': point_events})
                point_events = []
                point_played += 1

        return all_events
        
    def get_throw_selection(self):
        """ 
        Function that count throws types for all players

        Returns
        -------
        df: pandas dataframe
            players x types of throws (pass, dump, huck, swing, throwaway, dish)

        Example
        -------

        """
        # get events
        home_events = json.loads(self.json['tsgHome']['events'])
        away_events = json.loads(self.json['tsgAway']['events'])
         

        # get players id
        players = self.get_players_metadata()
        players = players[['id', 'player.first_name', 'player.last_name', 
            'player.ext_player_id']]

        # initialize df
        type_of_throws = ['pass', 'huck', 'swing', 'dump', 'dish', 'throwaway', 'drop']
        freq = [[0 for _ in range(len(type_of_throws))] for _ in range(len(players))]
        df = pd.DataFrame(freq, columns=type_of_throws)
        df['player'] = list(players['player.ext_player_id'])

        # reorder columns
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        # count throw freq
        self._count_throw_frequency(home_events, players, df)
        self._count_throw_frequency(away_events, players, df)


        # count total
        df['total'] = df.sum(axis=1)

        return df

    def _count_throw_frequency(self, events, players, df):
        """ 
        Helper function for get_throw_selection() that count throw frequency
        for a team 
        """
        # count throw frequency
        x1, y1, player1 = None, None, None
        for i, event in enumerate(events):
            event_type = int(event['t'])
            if event_type in [8, 19, 20, 22]: # event has x and y
                x2, y2 = event['x'], event['y']
                if event_type != 8:
                    player2 = int(event['r'])
                if x1 and y1 and player1:
                    # get player
                    player_id = players[players['id'] == player1]['player.ext_player_id'].tolist()[0]

                    # get distance and throw selection
                    #  dist = get_throwing_distance(x1, y1, x2, y2)
                    throw = get_throw_type(x1, y1, x2, y2, event_type)
                    #  print(player_id, throw, dist)

                    # increment player throw selection
                    df.loc[df['player'].isin([player_id]), throw] += 1
                x1, y1 = x2, y2
                if event_type != 8:
                    player1 = player2
            else: 
                x1, y1, player1 = None, None, None


    def get_thrower_receiver_count(self, is_home):
        """ 
        Function that returns the thrower-receiver count only if throw was 
        successful. Useful to view players chemistry

        Parameters
        ----------
        is_home: bool

        Returns
        -------
        df: pandas dataframe
            players x players: +1 if thrower attempted a pass to receiver

        Example
        -------
        """
        if is_home: 
            events = json.loads(self.json['tsgHome']['events'])
            players = pd.json_normalize(self.json['rostersHome'])
        else: 
            events = json.loads(self.json['tsgAway']['events'])
            players = pd.json_normalize(self.json['rostersAway'])

        # initialize df
        list_players = list(players['player.ext_player_id'])
        freq = [[0 for _ in range(len(list_players))] for _ in range(len(list_players))]
        df = pd.DataFrame(freq, columns=list_players)
        df['player'] = list_players

        # reorder columns
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        # count thrower-receiver freq 
        self._count_thrower_receiver(events, players, df)

        # count total throws
        df['total'] = df.sum(axis=1)

        return df

    def _count_thrower_receiver(self, events, players, df):
        """ 
        Helper function for get_thrower_receiver_count() to count thrower and
        receiver for team event
        """
        player1 = None
        for i, event in enumerate(events):
            event_type = int(event['t'])
            if event_type in [20, 22]: # removed 19 because dropped
                player2 = int(event['r'])
                if player1:
                    # get player
                    player1_id = players[players['id'] == player1]['player.ext_player_id'].tolist()[0]
                    player2_id = players[players['id'] == player2]['player.ext_player_id'].tolist()[0]

                    # increment thrower-receiver 
                    df.loc[df['player'].isin([player1_id]), player2_id] += 1
                player1 = player2
            else: 
                player1 = None

    def get_lineup_frequency(self, is_home): 
        """ 
        Function that calculates the number of time a player is on the same 
        line as teamate. Only counts starting lineup (ie starting on offense 
        or defense, not after timeout)

        Parameters
        ----------
        is_home: bool

        Returns
        -------
        df: pandas dataframe
            players x players: +1 if player i and j are on the same line
        """
        if is_home: 
            events = json.loads(self.json['tsgHome']['events'])
            players = pd.json_normalize(self.json['rostersHome'])
        else: 
            events = json.loads(self.json['tsgAway']['events'])
            players = pd.json_normalize(self.json['rostersAway'])

        # initialize df
        list_players = list(players['player.ext_player_id'])
        freq = [[0 for _ in range(len(list_players))] for _ in range(len(list_players))]
        df = pd.DataFrame(freq, columns=list_players)
        df['player'] = list_players

        # reorder columns
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        # count lineup freq
        self._count_lineup_frequency(events, players, df)

        return df

    def _count_lineup_frequency(self, events, players, df): 
        """ 
        Helper function for get_lineup_frequency()
        """
        for i, event in enumerate(events):
            event_type = int(event['t']) 
            if event_type in [1,2]:
                l = event['l']
                lineup = [players[players['id'] == int(player_id)]['player.ext_player_id'].tolist()[0] for player_id in l]
                #  print(lineup)
                for i in range(len(lineup)):
                    for j in range(len(lineup)):
                        if i != j:
                            player1, player2 = lineup[i], lineup[j]
                            df.loc[df['player'].isin([player1]), player2] += 1
        

    def get_teamates_selection(self, player_id, is_home):
        """ 
        For a given thrower, return throw selection for each teamates

        Parameters
        ----------
        is_home: bool
            True if player is in home team, else false
        player_id: str
            player external id

        Returns
        -------
        df: pandas dataframe
            teamates x throwing_type

        Example
        -------
        >>> game.get_thrower_receiver_selection('cbrock', True)
        """
        if is_home: 
            events = json.loads(self.json['tsgHome']['events'])
            players = pd.json_normalize(self.json['rostersHome'])
        else: 
            events = json.loads(self.json['tsgAway']['events'])
            players = pd.json_normalize(self.json['rostersAway'])

        # check if player_id in players list
        list_players = list(players['player.ext_player_id'])
        if player_id not in list_players:
            raise ValueError("player_id doesn't exist. Please check!")

        # initialize dataframe
        type_of_throws = ['pass', 'huck', 'swing', 'dump', 'dish', 'throwaway', 'drop']
        selection = [[0 for _ in range(len(type_of_throws))] for _ in range(len(list_players))]
        df = pd.DataFrame(selection, columns=type_of_throws)
        df['player'] = list_players

        # reorder columns
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        # count teamates selection
        self._count_teamate_selection(events, players, player_id, df)

        # total throws by teamates
        df['total'] = df.sum(axis=1)

        return df
        
    def _count_teamate_selection(self, events, players, thrower, df): 
        """ 
        Helper Function for get_teamates_selection()
        """
        x1, y1, player1 = None, None, None
        for i, event in enumerate(events):
            event_type = int(event['t'])
            if event_type in [19, 20, 22]: # event has x and y
                x2, y2 = event['x'], event['y']
                player2 = int(event['r'])
                player_id = players[players['id'] == player2]['player.ext_player_id'].tolist()[0]
                if x1 and y1 and player1 == thrower:
                    # get distance and throw selection
                    throw = get_throw_type(x1, y1, x2, y2, event_type)

                    # increment player throw selection
                    df.loc[df['player'].isin([player_id]), throw] += 1
                x1, y1 = x2, y2
                player1 = player_id
            else: 
                x1, y1, player1 = None, None, None

        
    def print_team_events(self, is_home): 
        """ 
        Function that print events for home and away teams

        Parameters
        ----------
        is_home : bool
            True if we print events of home team, else false

        Examples
        --------
        >>> GameStats('2022-06-11-TB-ATL').print_team_events(True)
        >>> GameStats('2022-06-11-TB-ATL').print_team_events(False)

        """
        events = self.json['tsgHome']['events'] if is_home else self.json['tsgAway']['events']

        # FIXME: convert columns double values to int
        #  cols_to_int = ['t', 'ms', 's', 'c']
        #  for col in cols_to_int:
        #      events[col] = events[col].astype('int', errors='ignore')

        # get players_metadata
        players = self.get_players_metadata()
        players = players[['id', 'player.first_name', 'player.last_name', 
            'player.ext_player_id']]


        # print all events
        for _, row in enumerate(json.loads(events)):
            t = row['t']
            if t in [1,2, 40, 41]:
                # print lineup
                l = row['l']
                lineup = [players[players['id'] == int(player_id)]['player.ext_player_id'].tolist()[0] for player_id in l
]
                print(f"t: {t}; lineup: {lineup}")
            elif t in [3,5,19,20,22]:
                # print receiver
                try:
                    receiver = players[players['id'] == int(row['r'])]['player.ext_player_id'].tolist()[0]
                except: 
                    receiver = 'NaN'
                if t in [3,19,20,22]:
                    print(f"t: {t}; r: {receiver}; x: {row['x']}; y: {row['y']}")
                else: 
                    print(f"t: {t}; r: {receiver}")
            elif t in [14, 15, 42, 43]:
                # print s
                print(f"t: {t}; s: {row['s']}")
            else: 
                print(f"t: {t}")

#  ---------------------------------------------------------------------

def main():
    game_id = '2022-07-22-NY-PHI'
    #  game_id = '2022-07-31-DET-MIN'
    game = GameStats(game_id)
    #  print(game.get_boxscores()) # works
    #  print(game.get_events()) # works
    #  print(game.get_game_metadata()) # works
    #  print(game.get_players_metadata()) # works
    #  print(game.get_point_results()) 
    #  print(game.get_teams_metadata()) # works
    #  print(game.get_team_stats()) # works
    #  print(game.get_roster_stats()) # works
    lineups = game.get_lineup_by_points()
    #  for lineup in lineups:
    #      print(lineup)
    #  print(lineups)
    #  print(len(lineups))
    

if __name__ == "__main__":
    main()
