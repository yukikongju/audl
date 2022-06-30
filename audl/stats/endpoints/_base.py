#!/usr/bin/env/python

import pandas as pd


class Endpoint(object):

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.endpoint = None
        self.url = None

    def _fetch_dfs_from_url(self):
        return pd.read_html(self.url)

    def _get_url(self) -> str:
        return f"{self.base_url}{self.endpoint}"


    def _get_endpoint(self) -> str:
        pass
