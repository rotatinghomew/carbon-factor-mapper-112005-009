import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = 'carbon_factor_mapper'

def read_csv(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))

def read_json(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

class ContractTests(unittest.TestCase):
    def test_package_name_and_data_directory(self):
        self.assertTrue(PACKAGE)
        self.assertTrue((ROOT / 'data').is_dir())

    def test_factor_units_match_activity_units_when_direct(self):
        activities = read_csv('activity_data.csv')
        factors = read_csv('factor_catalog.csv')
        factor_units = {row['factor_id']: row['unit'] for row in factors}
        self.assertTrue(factor_units['F001'] == next(row['unit'] for row in activities if row['activity_id'] == 'ACT01'))

    def test_withdrawn_factor_is_visible(self):
        rows = read_csv('factor_catalog.csv')
        self.assertTrue(next(row for row in rows if row['factor_id'] == 'F004')['status'] == 'withdrawn')
