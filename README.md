# AUDL API

[![PyPI version](https://badge.fury.io/py/audl.svg)](https://pypi.org/project/audl/)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://pypi.org/project/audl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Unofficial AUDL api for python users

[See Documentation](https://htmlpreview.github.io/?https://github.com/yukikongju/audl/blob/master/docs/audl/index.html)

To install: `pip install audl`

## Requirements

- Python 3.7+
- pandas, requests, lxml, html5lib

## Usage

#### How to get player profile

```python
from audl.stats.endpoints.playerprofile import PlayerProfile

# Fetching dataframe from "https://theaudl.com/league/players/cbrock"
player = PlayerProfile('cbrock')
career = player.get_career_stats()
reg = player.get_regular_seasons_career()
playoffs = player.get_playoffs_career()
season = player.get_season_games_stats(2019)
games_stats = player.get_career_games_stats()
player_metadata = player.get_personal_information()
```

#### How to get Team Stats

![image](https://user-images.githubusercontent.com/34996954/172069063-9499e31a-aab3-4a58-9345-106555f41b7a.png)

Season=['career', 2022, ..., 2012]
Per=['total', 'game']
Team=['team', 'opponent']


```python
from audl.stats.endpoints.teamstats import TeamStats

# fetching from "https://theaudl.com/stats/team"
team_stats = TeamStats('career', 'game', 'opponent') # TeamStats(season, per, team)
df = team_stats.get_table()
```

#### How to get Player Stats

![image](https://user-images.githubusercontent.com/34996954/172069041-48e55c45-717c-4e99-a7aa-777658833ac6.png)

Season=['career', 2022, ..., 2012]
Per=['total', 'game', 'points', 'possessions', 'minutes']

```python
from audl.stats.endpoints.playerstats import PlayerStats

# from "https://theaudl.com/stats/player-stats"
playerstats = PlayerStats('career', 'total', 'breeze').fetch_table()  # PlayerStats(season, per, team)

# save to CSV
playerstats_obj = PlayerStats('career', 'total', 'breeze')
playerstats_obj.download_stats_as_dataframe('output/player_stats.csv')
```

#### How to fetch season schedule

![image](https://user-images.githubusercontent.com/34996954/178094543-d6c57f95-6f1f-4aae-a7a4-a6687ab46afb.png)


```python
from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

# Fetch complete season schedule from "https://theaudl.com/league/game-search"
season_schedule = SeasonSchedule(2022).get_schedule()
team_season_schedule = TeamSeasonSchedule(2022, 'royal').get_schedule()
all_schedule = AllSchedule().get_schedule()
team_season_against_opponent = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()
```

#### How to get game statistics

Game IDs follow the format `YYYY-MM-DD-AWAY-HOME` (e.g. `2021-06-05-RAL-ATL` is the
June 5 2021 game where Raleigh visited Atlanta).

```python
from audl.stats.endpoints.gamestats import GameStats

# Fetching Box Scores from "https://theaudl.com/stats/game/2021-06-05-RAL-ATL"
game = GameStats("2021-06-05-RAL-ATL")
teams = game.get_teams_metadata()
players = game.get_players_metadata()
game_metadata = game.get_game_metadata()
team_stats = game.get_team_stats()
roster = game.get_roster_stats()
boxscores = game.get_boxscores()
events = game.get_events()
all_events = game.get_all_events()           # raw home + away events as dict
events_seq = game.get_events_sequential()    # events in sequential point order
point_results = game.get_point_results()     # offense/defense lineups and outcome per point
lineup_by_points = game.get_lineup_by_points()
throw_selection = game.get_throw_selection()
thrower_receiver_count = game.get_thrower_receiver_count(True)
lineup = game.get_lineup_frequency(True)
teamates = game.get_teamates_selection('ataylor', True)
df_throws = game.get_throws_dataframe()

# print game events
game.print_team_events(True)
game.print_team_events(False)
```

#### How to get Team Game Stats

![image](https://user-images.githubusercontent.com/34996954/178094574-43272b29-8d47-4d15-8207-0536dd2ca30c.png)


```python
from audl.stats.endpoints.teamgamestats import AllTeamGameStats, SeasonGameStats, TeamSeasonGameStats

team_season = TeamSeasonGameStats(2022, 'royal').get_game_stats()
all_games = AllTeamGameStats().get_game_stats()
season_games = SeasonGameStats(2022).get_game_stats()
```

## Examples

Jupyter notebooks with worked examples are in the [`examples/`](examples/) directory:

- [Player Profile](examples/Endpoints%20-%20Player%20Profile.ipynb)
- [Player Stats](examples/Endpoints%20-%20Player%20Stats.ipynb)
- [Game Statistics](examples/Endpoints%20-%20Game%20Statistics.ipynb)
- [Season Schedule](examples/Endpoints%20-%20Season%20Schedule.ipynb)
- [Team Game Stats](examples/Endpoints%20-%20Team%20Game%20Stats.ipynb)
