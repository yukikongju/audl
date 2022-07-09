# AUDL API

Unofficial AUDL api for python users

What it does: 
- [X] Fetch Data directly from [audl website](https://theaudl.com)
- [ ] Update database from Web Scrapping using workflow
- [ ] Generate pdf reports for player, team and games

[See Documentation](https://htmlpreview.github.io/?https://github.com/yukikongju/audl/blob/master/docs/audl/index.html)


## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)
- [Exploration](#exploration)


## [Requirements](#requirements)

1. Install requirements ```pip install -r requirements```
2. Having sqlite3: ```sudo apt install sqlite3```

Download package with `` pip install audl ``



## [Features](#features)


[AUDL Stats](https://theaudl.com/league/stats)

- [X] Fetch Data from
	- [X] [Player Profile](https://theaudl.com/league/players/mmcdonnel)
	- [X] [Team Stats](https://theaudl.com/stats/team)
	- [X] [Player Stats](https://theaudl.com/stats/player-stats)
	- [X] [Season Schedule](https://theaudl.com/league/game-search)
	- [X] [Game Stats](https://theaudl.com/stats/team-game-stats)
	- [X] [Team Game Stats](https://theaudl.com/stats/team-game-stats)

TODOs:
 - [ ] Create database from web scrapper (sql, database, workflows)
     - [ ] Teams
     - [ ] Players
     - [ ] Schedule
     - [ ] Player Game Stats
     - [ ] Team Game Stats
     - [ ] 
 - [ ] Write Scripts to fetch data daily/weekly/monthly
 - [ ] Write examples in notebook
 - [ ] Generate Reports
     - [ ] Game Report
	 - [ ] Stadium
	 - [ ] Temperature
	 - [ ] Roster
	 - [ ] Box Scores, Player Stats, Team Stats
	 - [ ] More: Injury Report
	 - [ ] More: Points events (point duration, number of TO/pass, throws 
		choices)
	 - [ ] More: Outstanding performance
	 - [ ] More: Point differential graph
     - [ ] Player Report
	 - [ ] Biography: height, weight, nickname, college, position, number
	 - [ ] Team History
	 - [ ] More: Teamate connection by season
	 - [ ] More: points distribution and efficiency
	 - [ ] More: Favorite throws
	 - [ ] More: Favorite cuts
	 - [ ] More: Stats Projection
	 - [ ] More: quick facts (performance vs league/team average)
	 - [ ] More: Injury Report
     - [ ] Team Report
	 - [ ] Biography: Stadium, city, year founded
	 - [ ] Roster by season
	 - [ ] More: Current Injuries
	 - [ ] More: Wins/Loss home/road
	 - [ ] More: Who are the team handler, dump, cutter, mid
	 - [ ] More: What game play?
	 - [ ] More: How the team rank vs other teams
	 - [ ] More: Best Lineups (and predictions)


## [Usage](#usage)


#### How to get player profile

```python

from audl.stats.endpoints.playerprofile import PlayerProfile

# Fetching dataframe from https://theaudl.com/league/players/cbrock
player = PlayerProfile('cbrock')
reg = player.get_regular_seasons_career()
playoffs = player.get_playoffs_career()
games = player.get_season_games_stats(2019)
```

#### How to get Team Stats

![image](https://user-images.githubusercontent.com/34996954/172069063-9499e31a-aab3-4a58-9345-106555f41b7a.png)

Season=['career', 2022, ..., 2012]
Per=['total', 'game']
Team=['team', 'opponent']


```python
from audl.stats.endpoints.teamstats import TeamStats

# fetching from: https://theaudl.com/stats/team
team_stats = TeamStats('career', 'game', 'opponent') # TeamStats(season, per, team)
df = team_stats.get_table()
```

#### How to get Player Stats

![image](https://user-images.githubusercontent.com/34996954/172069041-48e55c45-717c-4e99-a7aa-777658833ac6.png)

Season=['career', 2022, ..., 2012]
Per=['total', 'game', 'points', 'possessions', 'minutes']

```python
from audl.stats.endpoints.playerstats import PlayerStats

# from https://theaudl.com/stats/player-stats
playerstats = PlayerStats('career', 'total', 'breeze').fetch_table()  # PlayerStats(season, per, team)
```

#### How to fetch season schedule

```python

from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

# Fetch complete season schedule from https://theaudl.com/league/game-search

from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

# Fetch complete season schedule from https://theaudl.com/league/game-search

season_schedule = SeasonSchedule(2022).get_schedule()
team_season_schedule = TeamSeasonSchedule(2022, 'royal').get_schedule()
all_schedule = AllSchedule().get_schedule()
team_season_against_opponent = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()

```

#### How to get game statistics

```python

from audl.stats.endpoints.gamestats import GameStats

# Fetching Box Scores from https://theaudl.com/stats/game/2021-06-05-RAL-ATL
game = GameStats("2021-06-05-RAL-ATL")
teams = game.get_teams_metadata()
players = game.get_players_metadata()
game_metadata = game.get_game_metadata()
team_stats = game.get_team_stats()
roster = game.get_roster_stats()
scoring_time = game._get_scoring_time()
boxscores = game.get_boxscores()
events = game.get_team_events()

# print game events
game.print_team_events(True)
game.print_team_events(False)


```

#### How to get Team Game Stats

```python
from audl.stats.endpoints.teamgamestats import AllTeamGameStats, SeasonGameStats, TeamSeasonGameStats

team_season = TeamSeasonGameStats(2022, 'royal').get_game_stats()
all_games = AllTeamGameStats().get_game_stats()
season_games = SeasonGameStats(2022).get_game_stats()

```

## [Exploration](#exploration)

- [ ] Proportion of touches per player on offensive points
- [ ] Proportion of passes to teamates for each players (see connection)
- [ ] Who is the best in the rain? (player efficiency vs temperature)
- [ ] Most likely player to blow up
- [ ] Player Report


## Tree


## How to ...





**How to deploy pip package**


```bash
python3 -m build
python3 -m twine upload --repository testpypi dist/*
twine upload dist/*
```

**How to generate documentation with pdoc3**

```bash 
pdoc --html audl
mv html/ docs/
```


## How to contribute


## Ressources

- [Deploy pip packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Deploy pip package using setup.py](https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3)
- [Basketball Ref API](https://github.com/vishaalagartha/basketball_reference_scraper)
- [Sample Project](https://github.com/pypa/sampleproject)
- [Sports Analytics Project](https://github.com/wyattowalsh/sports-analytics)
- [Generating Documentation with Docstring using pdoc3](https://pdoc3.github.io/pdoc/)



