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
dbh = c["students"]

assert dbh.connection == c
print "Successfully set up a database handle"

def count_records():
    '''Count mongodb recrods'''
    print 'starting...'
    try:
        total_count = dbh.grades.find({}).count()
        print "There are %d documents in %s collection" % (total_count, dbh)
    except: 'Error: ', sys.exc_info()[0]

def find():
    '''Use the find command'''
    print 'starting find...'
    try:
        results = dbh.grades.find().sort('score', -1)
    except: 
        'Error: ', sys.exc_info()[0]

    for doc in results:
        print doc

def find_selector():
    '''Use find with selector'''
    print 'starting find selector...'
    query = {'type' : 'homework'}
    selector = {'student_id' : 1, '_id': 0, 'score' : 1}
    try:
        results = dbh.grades.find(query, selector).sort('score', -1)
    except: 
        'Error: ', sys.exc_info()[0]

    for doc in results:
        print doc

def find_gt_lt(gt, ls):
    '''gt and lt'''
    print 'starting find selector...'
    query = {'type' : 'homework', 'score' :{'$gt':gt, '$lt':ls}}
    selector = {'student_id' : 1, '_id': 0, 'score' : 1}
    try:
        results = dbh.grades.find(query, selector).sort('score', -1)
    except: 
        'Error: ', sys.exc_info()[0]

    for doc in results:
        print doc

def skip_limit_sort():
    '''Sort, Skip, Limit'''
    query = {}
    #selector = {'student_id' : 1, '_id': 0, 'score' : 1}
    try:
        results = dbh.grades.find(query).sort('student_id', pymongo.ASCENDING).skip(4).limit(10)
    except: 
        'Error: ', sys.exc_info()[0]

    for doc in results:
        print doc

def test():
    '''SORT SKIP LIMIT'''
    query = {'type' : 'homework'}
    selector = {'_id': 1}
    try:
        #results = dbh.grades.find(query).sort('score', pymongo.ASCENDING).sort('student_id', pymongo.ASCENDING).skip(1)
        results = dbh.grades.find(query).skip(2)
        results = results.limit1
        #results = results.sort('score', pymongo.ASCENDING).sort('student_id', pymongo.ASCENDING).skip(2).limit(1)
    except: 
        'Error: ', sys.exc_info()[0]

    for doc in results:
        print doc
            #dbh.grades.remove(doc)

def main():
    #count_records()
    #find()
    #find_selector()
    #find_gt_lt(50, 70)
    #skip_limit_sort()
    test()

if __name__ == "__main__":
    main()


