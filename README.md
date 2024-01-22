# AUDL API

Unofficial AUDL api for python users

What it does: 
- [X] Fetch Data directly from [audl website](https://theaudl.com)
- [ ] Update database from Web Scrapping using workflow
- [ ] Generate pdf reports for player, team and games

[See Documentation](https://htmlpreview.github.io/?https://github.com/yukikongju/audl/blob/master/docs/audl/index.html)

To download the package: `pip install audl`


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
```

#### How to fetch season schedule

![image](https://user-images.githubusercontent.com/34996954/178094543-d6c57f95-6f1f-4aae-a7a4-a6687ab46afb.png)


```python

from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

# Fetch complete season schedule from "https://theaudl.com/league/game-search"

from audl.stats.endpoints.seasonschedule import SeasonSchedule, TeamSeasonSchedule, AllSchedule, TeamSeasonAgainstOpponentSchedule

# Fetch complete season schedule from "https://theaudl.com/league/game-search"

season_schedule = SeasonSchedule(2022).get_schedule()
team_season_schedule = TeamSeasonSchedule(2022, 'royal').get_schedule()
all_schedule = AllSchedule().get_schedule()
team_season_against_opponent = TeamSeasonAgainstOpponentSchedule(2022, 'royal', 'rush').get_schedule()

```

#### How to get game statistics

```python

from audl.stats.endpoints.gamestats import GameStats

# Fetching Box Scores from "https://theaudl.com/stats/game/2021-06-05-RAL-ATL"
game = GameStats("2021-06-05-RAL-ATL")
teams = game.get_teams_metadata()
players = game.get_players_metadata()
game_metadata = game.get_game_metadata()
team_stats = game.get_team_stats()
roster = game.get_roster_stats()
scoring_time = game._get_scoring_time()
boxscores = game.get_boxscores()
events = game.get_events()
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


