#!/usr/bin/env/python

import pandas as pd


def download_dataframe(path: str, dataframe: list) -> None:
    dataframe.to_csv(path, sep=',', index=False)
