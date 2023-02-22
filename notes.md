## [Features](#features)


[AUDL Stats](https://theaudl.com/league/stats)

- [O] Fetch Data from
	- [X] [Player Profile](https://theaudl.com/league/players/mmcdonnel)
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

