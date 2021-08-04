#!/usr/bin/env/python

import pandas as pd


class Endpoint(object):

    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint
        self.url = base_url + endpoint

    def fetch_dfs_from_url(self):
        return pd.read_html(self.url)
