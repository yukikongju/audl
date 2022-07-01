# AUDL API

Unofficial AUDL api for python users

## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)
- [Exploration](#exploration)


## [Requirements](#requirements)

Download package with `` pip install audl ``

## [Features](#features)


[AUDL Stats](https://theaudl.com/league/stats)

- [O] Fetch Data from
	- [X] [Player Profile](https://theaudl.com/league/players/mmcdonnel)
	- [X] [Team Stats](https://theaudl.com/stats/team)
	- [X] [Player Stats](https://theaudl.com/stats/player-stats)
	- [X] [Season Schedule](https://theaudl.com/league/game-search)
	- [ ] [Game Stats](https://theaudl.com/stats/team-game-stats)

TODOs:
 - [ ] Game Stats
     - [ ] Team Metadata
     - [ ] Players Metadata
     - [ ] Box Scores
     - [ ] Scores
     - [ ] Team Stats
     - [ ] Print play by play by players name
     - [ ] Disc movement


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

df = SeasonSchedule(2022).get_schedule()
df = TeamSeasonSchedule(2022, 'royal').get_schedule()
df = AllSchedule().get_schedule()
df = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()

```

#### How to get game statistics

```python

from audl.stats.endpoints.gamestatsboxscores import GameStatsBoxScores
from audl.stats.endpoints.gamestatsrosters import GamesStatsRosters
from audl.stats.endpoints.gamestatslineups import GameStatsLineups
from audl.stats.endpoints.gamestatsteamstats import GameStatsTeamStats

# Fetching Box Scores from https://theaudl.com/stats/game/2021-06-05-RAL-ATL
box_scores = GameStatsBoxScores("2021-06-05-RAL-ATL").get_box_scores()

# Fetching Roster Metadata
rosters = GamesStatsRosters("2021-06-05-RAL-ATL")
roster_home = rosters.get_roster_home_metadata()
roster_away = rosters.get_roster_away_metadata()

# Fetching Lineups Points by Points
lineups = GameStatsLineups("2021-07-16-DAL-SEA")
lineup_home = lineups.get_home_points_by_points_lineups())
lineup_away = lineups.get_away_points_by_points_lineups())

# Fetching Team Stats
team_stats = GameStatsTeamStats("2021-07-16-DAL-SEA").get_team_stats()
```

## [Exploration](#exploration)

- [ ] Proportion of touches per player on offensive points
- [ ] Proportion of passes to teamates for each players (see connection)
- [ ] Who is the best in the rain? (player efficiency vs temperature)
- [ ] Most likely player to blow up





