import matplotlib.pyplot as plt
import cv2
import time
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
KEYSPACE = "mykeyspacex"

def createKeySpace():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE) #新建一个keyspace
    session.set_keyspace(KEYSPACE)
    session.execute(""" CREATE TABLE IF NOT EXISTS mytable ( QueryTime text, QueryImage blob, QueryAnswer text, PRIMARY KEY(QueryTime)) """)
    image_read = open("testImage/1.jpg", "rb").read()
    
    # define which keyspace/database to use for further query
    session.execute('USE %s' % KEYSPACE)

    clothOutput = "shoes"
    strCQL = "INSERT INTO mytable (QueryTime,QueryImage,QueryAnswer) VALUES (?,?,?)"
    pStatement = session.prepare(strCQL)
    session.execute(pStatement,[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), image_read, clothOutput])

def queryKeySpace():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)
    ans = session.execute("""SELECT * FROM mytable""")
    for i in ans:
        print(i[0], i[1])
        # print(type(i[2]))
        open("%s.jpg" % (i[0] + i[1]), "wb").write(i[2])


# createKeySpace()
queryKeySpace();
