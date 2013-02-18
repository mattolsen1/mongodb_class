import sys

from pymongo import Connection
from pymongo.errors import ConnectionFailure
import pymongo

""" Connect to MongoDB """
try:
    c = Connection(host="localhost", port=27017, safe=True)
    print "Connected successfully"
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
# Get a Database handle to a database named "mydb"
dbh = c["blog"]

assert dbh.connection == c
print "Successfully set up a database handle"

def test():
    cursor = dbh.posts.find().sort('date',pymongo.DESCENDING).limit(10)
    for i in cursor:
        print i

test()