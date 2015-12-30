import csv
from datetime import datetime
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import re
import types
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


GEO_LEVEL = {'district': 'dist',
             'province': 'prov' }


geoKeys = [geoPrefix + '_id' for geoPrefix in GEO_LEVEL]
print geoKeys

"""
prints:
    ['province_id', 'district_id']
"""