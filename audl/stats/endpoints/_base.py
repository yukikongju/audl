#!/usr/bin/env/python
"""
Abstract base class for all AUDL API endpoint wrappers.

Every endpoint class in ``audl.stats.endpoints`` inherits from ``Endpoint``.
Subclasses implement ``_get_url()`` to produce the full request URL and expose
results through public ``get_*()`` methods that return ``pandas.DataFrame``
objects.

The underlying data is served by the UFA stats backend at:
    https://www.backend.ufastats.com
"""

import pandas as pd


class Endpoint(object):
    """Abstract base for AUDL API endpoints.

    Provides URL construction and raw HTML table fetching. All concrete
    endpoint classes (``PlayerStats``, ``GameStats``, etc.) inherit from this
    class and override ``_get_url()`` to assemble their specific request URLs.

    Parameters
    ----------
    base_url : str
        Root URL for the endpoint, e.g.
        ``"https://www.backend.ufastats.com/web-v1/player-stats?limit=20"``.
    """

    def __init__(self, base_url: str):
        """
        Parameters
        ----------
        base_url : str
            Root URL used by ``_get_url()`` to construct the full request URL.
        """
        self.base_url = base_url
        self.endpoint = None
        self.url = None

    def _fetch_dfs_from_url(self):
        """Fetch all HTML tables at ``self.url`` as a list of DataFrames.

        Uses ``pandas.read_html`` to parse every ``<table>`` element on the
        page.

        Returns
        -------
        list of pandas.DataFrame
            One DataFrame per ``<table>`` element found at the URL.
        """
        return pd.read_html(self.url)

    def _get_url(self) -> str:
        """Build and return the full request URL.

        Returns
        -------
        str
            ``base_url`` concatenated with ``self.endpoint``.
        """
        return f"{self.base_url}{self.endpoint}"

    def _get_endpoint(self) -> str:
        """Return the endpoint suffix appended to ``base_url``.

        Subclasses override this when the suffix requires dynamic construction.

        Returns
        -------
        str or None
        """
        pass
