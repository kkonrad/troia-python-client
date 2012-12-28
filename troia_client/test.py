import sys

from client import TroiaClient


if __name__ == '__main__':

    if len(sys.argv) > 1:
        address = sys.argv[1]
    else:
        address = 'http://localhost:8080/troia-server-0.0.1'
    tc = TroiaClient(address, "TEST_JOB_")
    print "PING:", tc.ping()
    print "PINGDB:", tc.pingDB()
    print "CREATE:", tc.create("batch")
    print "INFO:", tc.info()
