import gevent.monkey
gevent.monkey.patch_all()

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
import random
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://root@localhost/test',
                       pool_size=2, max_overflow=100, pool_recycle=2)
Session = scoped_session(sessionmaker(bind=engine))

stop = False

def worker():
    global stop
    try:
        while True:
            Session.execute("SELECT 1+1")
            gevent.sleep(random.random())
            Session.remove()
            #sys.stderr.write('.')
    finally:
        stop = True


def main():
    for i in range(100):
        gevent.spawn(worker)

    gevent.sleep(3)

    result = list(engine.execute("show processlist"))
    engine.execute("kill %d" % result[-2][0])

    while not stop:
        gevent.sleep(1)
    gevent.sleep(1)


main()
