# AUDL API

Unofficial AUDL api for python users

## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)


## [Requirements](#requirements)

Download package with `` pip install audl ``

## [Features](#features)

- [X] Fetch Data from
	- [X] [Player Profile](https://theaudl.com/league/players/mmcdonnel)
	- [X] [Team Stats](https://theaudl.com/stats/team?year=1)
	- [X] [Team Season Player Stats](https://theaudl.com/stats/team-season-players)
	- [X] [All-Time Player Stats](https://theaudl.com/stats/players-all-time)
	- [X] [Season Player Stats](https://theaudl.com/stats/player-season)
	- [X] [Team Season Schedule](https://theaudl.com/hustle/schedule)
	- [X] [Season Schedule](https://theaudl.com/league/schedule/week)
	- [ ] [Game Stats](https://theaudl.com/stats/team-game-stats)

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

```python

from audl.stats.endpoints.seasonplayerstats import SeasonPlayerStats

# Downloading season player stats from https://theaudl.com/stats/player-season?year={all_pages}
SeasonPlayerStats(2021).download_season_player_stats()

```

#### How to get team season schedule

```python

from audl.stats.endpoints.teamseasonschedule import TeamSeasonSchedule

# fetch schedule from https://theaudl.com/hustle/schedule as Data Frame
schedule = TeamSeasonSchedule("Atlanta Hustle").get_team_schedule()

```

#### How to download season schedule

```python

from audl.stats.endpoints.seasonschedule import SeasonSchedule

# Fetch complete season schedule from https://theaudl.com/league/schedule/ as Data Frame
schedule = SeasonSchedule().get_season_schedule_df()

# Download season schedule as csv
SeasonSchedule().download_season_schedule_as_csv()

```

#### How to get game information

