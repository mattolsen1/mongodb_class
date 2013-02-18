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
dbh = c["school"]

assert dbh.connection == c
print "Successfully set up a database handle"

def test():
    total = dbh.students.count()
    print 'Total Items: {0}'.format(total)
    check = dbh.students.find({'_id':100}).sort('', pymongo.ASCENDING)
    for item in check:
        for score in item['scores']:
            print score['score']

def sort():
    check = dbh.students.find()
    for doc in check:
        print doc

def find_selector():
    '''Use find with selector'''
    print 'starting find selector...'
    selector = {'_id': 1, 'scores' : 1}
    try:
        #myresults = dbh.students.aggregate( [ {"$match": {"scores.type" : "homework" }},{ "$unwind": "$scores"},{"$group": { '_id':'$_id', 'minitem': {'$min': "$scores.score" } } } ] )
        myresults = dbh.students.aggregate( [ 

            { "$unwind": "$scores"},
            {"$match": {"scores.type" : "homework" }},
            {"$group": { '_id':'$_id', 'minitem': {'$min': "$scores.score" } } } ] )
    except: 
        'Error: ', sys.exc_info()[0]

    for result in myresults['result']:
        dbh.students.update( { '_id': result['_id'] }, { '$pull': { 'scores': { 'score': result['minitem'] } } } )
    #for result in myresults['result']:
        #print result
 


def main():

    #test()
    #sort()
    find_selector()
if __name__ == "__main__":
    main()


