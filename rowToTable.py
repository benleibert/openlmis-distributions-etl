import csv
from datetime import datetime
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import re
import types
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def toUtf(string):
    """
    Encodes a string into utf-8.  Returns same object if not a string or is already a unicode object.
    No attempt is made to determine/convert a unicode object is made.

    @param string: a string to convert to unicode using the utf-8 encoding
    @return a unicode object using utf-8. Or the same object as passed if the string parameter wasn't a
	subtype of basestring or was already a subtype of unicode.

    """

    if not isinstance(string, types.StringTypes): return string
    if isinstance(string, unicode): return string
    try:
        asUtf8 = unicode(string, 'utf-8')
    except:
        print 'Failure to encode as utf-8: ' + string
        print type(string)
        raise
    return asUtf8


def rowToTable(rowData, keyColumn, allowDupes = False):
    """
    Turns a list of dict's into a dict that's keyed off one common column from the dicts.
    Return: a dict keyed off of keyColumn found in all rowData.  If multiple row's would
    be keyed off the same value, then each item from rowData will be in a list under the same key.
    """
    table = dict()
    for row in rowData:
        if keyColumn not in row:
            raise LookupError('Key column ' + keyColumn + ' not in row data: ' + str(rowData))
        key = toUtf(row[keyColumn])
        if allowDupes == False and row[keyColumn] in table:
            raise StandardError('Duplicate key ' + row[keyColumn] + ' found')

        # turn row dict into a dict with strings in utf
        asDict = {}
        for k,v in row.iteritems():
            if isinstance(v, basestring): v = toUtf(v)
            asDict[toUtf(k)] = v

        # enter dict item into result dict that's keyed off the column given.  If
        # an item already exists under that key, turn the value into a list of dicts.
        if key in table:
            if not isinstance(table[key], list): table[key] = [table[key],]
            table[key].append(asDict)
        else: table[key] = asDict

    return table



row = [
    {
        'id' : 5,
        'fName' : 'timmy'   ,
        'lName' : 'simpson5' ,
        'age' : 3
    },

    {
        'id' : 3,
        'fName' : 'tommy'   ,
        'lName' : 'simpson3' ,
        'age' : 5
    },

    {
        'id' : 4,
        'fName' : 'jimmy'   ,
        'lName' : 'simpson4' ,
        'age' : 13
    },
]

table = rowToTable(row, 'id')
print table

"""
returns:
{
    3: {'lName': 'simpson3', 'age': 5, 'id': 3, 'fName': 'tommy'},
    4: {'lName': 'simpson4', 'age': 13, 'id': 4, 'fName': 'jimmy'},
    5: {'lName': 'simpson5', 'age': 3, 'id': 5, 'fName': 'timmy'}
}


As seen by the output, the rowToTable function is somewhat misnamed. It really takes a table (list of dicts) and
returns those same rows/dicts, but with the specified attribute as a key you can use to reference them.
"""