# AUDL API

Unofficial AUDL api for python users

## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)


## [Requirements](#requirements)

Download package with `` pip install audl ``

## [Features](#features)

- [O] Fetch Data from
	- [X] [Player Profile](https://theaudl.com/league/players/mmcdonnel)
	- [X] [Team Stats](https://theaudl.com/stats/team?year=1)
	- [X] [Team Season Player Stats](https://theaudl.com/stats/team-season-players)
	- [X] [All-Time Player Stats](https://theaudl.com/stats/players-all-time)
	- [X] [Season Player Stats](https://theaudl.com/stats/player-season)
	- [ ] [Season Schedule](https://theaudl.com/league/schedule/week)
	- [ ] [Team Season Schedule](https://theaudl.com/hustle/schedule)
	- [X] [Game Stats](https://theaudl.com/stats/team-game-stats)

## [Usage](#usage)


#### How to get player profile

```python

from audl.stats.endpoints.playerprofile import PlayerProfile

# Fetching dataframe from https://theaudl.com/league/players/mmcdonnel
player = PlayerProfile("Rowan McDonnell")

# Get player's regular season and playoffs stats
regular_season = player.get_regular_seasons_career()
playoffs = player.get_playoffs_career()
```

#### How to get team stats by season

```python

from audl.stats.endpoints.teamstats import TeamStats

# Fetching dataframe from https://theaudl.com/stats/team
season = TeamStats(2021).get_teams_stats_by_season()
```

#### How to get team season player stats by team and by season

```python

from audl.stats.endpoints.teamseasonplayerstats import TeamSeasonPlayerStats

# Fetching dataframe from https://theaudl.com/stats/team-season-players?year=1&aw_team_id=12
royal_mtl = TeamSeasonPlayerStats("Montreal Royal", 2021).get_team_season_player_stats()
```

#### How to download all-time player stats

```python

from audl.stats.endpoints.alltimeplayerstats import AllTimePlayerStats

# Downloading all-time player stats from https://theaudl.com/stats/players-all-time as .csv file
AllTimePlayerStats.download_all_time_player_stats(show_message=True)
```

#### How to download all players stats by season


#### How to get game statistics

```python

from audl.stats.endpoints.gamestats import GameStats
from audl.stats.endpoints.gamestatsboxscores import GameStatsBoxScores

# Fetching data from https://theaudl.com/stats/game/2021-06-05-RAL-ATL
box_scores = GameStatsBoxScores("2021-06-05-RAL-ATL").get_box_scores()

```


