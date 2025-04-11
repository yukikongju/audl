## BUGS


- FAILED test_gamestats.py::TestGameStats::test_get_events - AssertionError: <class 'dict'> != 'dict'
- FAILED test_gamestats.py::TestGameStats::test_get_teamates_selection - TypeError: can only concatenate str (not "int") to str
- FAILED test_gamestats.py::TestGameStats::test_get_throw_selection - TypeError: can only concatenate str (not "int") to str
- FAILED test_gamestats.py::TestGameStats::test_get_thrower_receiver_count - TypeError: can only concatenate str (not "int") to str


## [Features](#features)


[AUDL Stats](https://theaudl.com/league/stats)

- [O] Fetch Data from [Player Profile](https://theaudl.com/league/players/mmcdonnel)
	- [X] [Team Stats](https://theaudl.com/stats/team)
	    - [ ] Merge team and opponent columns into single df
	- [X] [Player Stats](https://theaudl.com/stats/player-stats)
	- [X] [Season Schedule](https://theaudl.com/league/game-search)
	- [X] [Game Stats](https://theaudl.com/stats/team-game-stats)
	- [X] [Team Game Stats](https://theaudl.com/stats/team-game-stats)
- [ ] Utils
    - [ ] Get Type of throw from x, y coordinates
    - [ ] Get previous thrower
- [ ] Game Events
    - [ ] Thrower and Receiver

TODOs for integration:
 - [ ] Transition url request to "backend.udastats.com/web-v1/player-stats"
 - [X] Black formatting before commit => [precommit hook](https://medium.com/@0xmatriksh/how-to-setup-git-hooks-pre-commit-commit-msg-in-my-project-11aaec139536)
 - [X] Setup pre-commit hook commit-msg with comitizen
 - [ ] Setup pre-commit hook to generate docs
 - [ ] Setup Github actions for tests before merging => [github action local hook](https://www.youtube.com/watch?v=itI2q7dca5Y)
 - [ ] FastAPI integration

TODOs for project:
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



## [Exploration](#exploration)

- [ ] Proportion of touches per player on offensive points
- [ ] Proportion of passes to teamates for each players (see connection)
- [ ] Who is the best in the rain? (player efficiency vs temperature)
- [ ] Most likely player to blow up
- [ ] Player Report


## Tree


## How to ...


**How to deploy pip package**

Update: 2024-01-21. Need to get API token as described [here](https://pypi.org/manage/account/token/).


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

**How to setup pre-commit hoooks**

After initializing the precommit hook with `pre-commit init` (it's already done),
the `.prec-commit-config.yaml` file should be created. To activate this
pre-commit hook, do

```{bash}
pre-commit install
```

If the files are not properly linted, the lint test will fail and will automatically
lint it for us. We only need to add the files back with `git add -u` and try
to commit again.


**How to commit using commitizen**

Use `cz commit` or `python3 -m commitizen commit`

## How to contribute


## Ressources

- [Deploy pip packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Deploy pip package using setup.py](https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3)
- [Basketball Ref API](https://github.com/vishaalagartha/basketball_reference_scraper)
- [Sample Project](https://github.com/pypa/sampleproject)
- [Sports Analytics Project](https://github.com/wyattowalsh/sports-analytics)
- [Generating Documentation with Docstring using pdoc3](https://pdoc3.github.io/pdoc/)
