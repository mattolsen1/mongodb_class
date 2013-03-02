# create our directories
mkdir -p /data/shard{0,1}/rs{0,1,2}
mkdir -p /data/config/config-{a,b,c}

# start a replica set and tell it that it will be a shard
mongod --replSet s0 --logpath s0-r0.log --dbpath /data/shard0/rs0 --port 37017 --fork --shardsvr --smallfiles --oplogSize=50
mongod --replSet s0 --logpath s0-r1.log --dbpath /data/shard0/rs1 --port 37018 --fork --shardsvr --smallfiles --oplogSize=50
mongod --replSet s0 --logpath s0-r2.log --dbpath /data/shard0/rs2 --port 37019 --fork --shardsvr --smallfiles --oplogSize=50

# connect to one server and initiate the set
mongo --port 37017 << 'EOF'
config = {
    _id: "s0",
    members: [
        {_id: 0, host: "localhost:37017"},
        {_id: 1, host: "localhost:37018"},
        {_id: 2, host: "localhost:37019"}
    ]
}

rs.initiate(config)
EOF

# start a replica set and tell it that it will be a shard
mongod --replSet s1 --logpath s1-r0.log --dbpath /data/shard1/rs0 --port 47017 --fork --shardsvr --smallfiles --oplogSize=50
mongod --replSet s1 --logpath s1-r1.log --dbpath /data/shard1/rs1 --port 47018 --fork --shardsvr --smallfiles --oplogSize=50
mongod --replSet s1 --logpath s1-r2.log --dbpath /data/shard1/rs2 --port 47019 --fork --shardsvr --smallfiles --oplogSize=50

# connect to one server and initiate the set
mongo --port 47017 << 'EOF'
config = {
    _id: "s1",
    members: [
        {_id: 0, host: "localhost:47017"},
        {_id: 1, host: "localhost:47018"},
        {_id: 2, host: "localhost:47019"}
    ]
}

rs.initiate(config)
EOF

# now start 3 config servers
mongod --logpath config-a.log --dbpath /data/config/config-a --port 57017 --fork --configsvr
mongod --logpath config-b.log --dbpath /data/config/config-b --port 57018 --fork --configsvr
mongod --logpath config-c.log --dbpath /data/config/config-c --port 57019 --fork --configsvr

# add shards and enable sharding on the test db
mongo << 'EOF'
db.adminCommand({addshard: "s0/localhost:37017"})
db.adminCommand({addshard: "s1/localhost:47017"})
db.adminCommand({enableSharding: "test"})
db.adminCommand({shardCollection: "test.grades", key: {student_id: 1}})
EOF