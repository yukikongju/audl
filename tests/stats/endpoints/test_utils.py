#!/usr/bin/env/python

import unittest
from audl.stats.endpoints.utils import get_all_players_ext_ids


class TestTeamStats(unittest.TestCase):

    def test_get_all_players_ext_ids(self):
        ids = get_all_players_ext_ids(True) 
        self.assertEqual(type(ids), 'list')

if __name__ == "__main__":
    main()


