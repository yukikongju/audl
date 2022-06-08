#!/usr/bin/env/python

from audl.stats.library.parameters import season_dict


def get_season_id(year: int) -> str:
    return season_dict.get(year)

FIRST_SEASON_YEAR = 2012

