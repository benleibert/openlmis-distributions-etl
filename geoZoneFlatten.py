
import csv
from datetime import datetime
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import re
import types
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def geoZoneFlatten(geoZone, geoZoneTable):
    """
    Given a leaf geographic zone, will loop up to each geographic zone parent until the heirachy is flat.
    Returns a dict that's keyed off of the geographic level code
    """
    gz = {}
    while geoZone is not None:
        gz[geoZone['geo_level_code']] = geoZone
        geoZone = geoZoneTable.get(geoZone['parentid'])

    return gz


geoZone = {
    'id': 12,
    'geo_level_code': 'dist',
    'parentid': 9
}

#Note that the geoZoneTable below has been passed to rowToTable(), and is thus a bunch of key(id)-value(row) pairs
geoZoneTable = {
    1:  {'id': 1, 'geo_level_code': 'country', 'parentid': None},
    2:  {'id': 2, 'geo_level_code': 'country', 'parentid': None},
    3:  {'id': 3, 'geo_level_code': 'state', 'parentid': 1},
    4:  {'id': 4, 'geo_level_code': 'prov', 'parentid': 3},
    5:  {'id': 5, 'geo_level_code': 'dist', 'parentid': 4},
    6:  {'id': 6, 'geo_level_code': 'state', 'parentid': 2},
    7:  {'id': 7, 'geo_level_code': 'state', 'parentid': 2},
    8:  {'id': 8, 'geo_level_code': 'state', 'parentid': 2},
    9:  {'id': 9, 'geo_level_code': 'prov', 'parentid': 6},
    10: {'id': 10, 'geo_level_code': 'prov', 'parentid': 7},
    11: {'id': 11, 'geo_level_code': 'prov', 'parentid': 8},
    12: {'id': 12, 'geo_level_code': 'dist', 'parentid': 9},
    13: {'id': 13, 'geo_level_code': 'dist', 'parentid': 9},
    14: {'id': 14, 'geo_level_code': 'dist', 'parentid': 9},
    15: {'id': 15, 'geo_level_code': 'dist', 'parentid': 10},
    16: {'id': 16, 'geo_level_code': 'dist', 'parentid': 10},
    17: {'id': 17, 'geo_level_code': 'dist', 'parentid': 10},
    18: {'id': 18, 'geo_level_code': 'dist', 'parentid': 11},
    19: {'id': 19, 'geo_level_code': 'dist', 'parentid': 11},
    20: {'id': 20, 'geo_level_code': 'dist', 'parentid': 11},
    21: {'id': 21, 'geo_level_code': 'prov', 'parentid': 2},
    22: {'id': 22, 'geo_level_code': 'dist', 'parentid': 21}
}

gz = geoZoneFlatten(geoZone, geoZoneTable)
print gz

"""
prints:
{
    'dist':    {'id': 12, 'geo_level_code': 'dist', 'parentid': 9},
    'prov':    {'id': 9, 'geo_level_code': 'prov', 'parentid': 6},
    'state':   {'id': 6, 'geo_level_code': 'state', 'parentid': 2},
    'country': {'id': 2, 'geo_level_code': 'country', 'parentid': None}
}

So, as seen by the output, the name "geoZoneFlatten" isn't quite right. Instead, the method takes a geoZone (and geoZoneTable)
and returns a dict containing the specified geoZone along with all of its parent geoZones.
"""