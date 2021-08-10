#!/usr/bin/env/python

import json
import pandas as pd

from audl.stats.endpoints.gamestats import GameStats

# TODO
class GameStatsEvent(GameStats):

    def __init__(self):
        super().__init__()
        self.t = None
