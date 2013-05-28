import logging
import requests
import csv
import sys
import nose

from nominalJobsTests.testSettings import *
from client.galc import TroiaContClient
from client.gal import TroiaClient

JOB_STORAGES = ["MEMORY_FULL", "MEMORY_KV", "DB_FULL", "DB_KV_MEMCACHE_JSON", "DB_KV_MEMCACHE_SIMPLE", "DB_KV_JSON", "DB_KV_SIMPLE"] 


def main(args):
    for js in JOB_STORAGES:
        print "JS:", js
        requests.post("{}/config".format(ADDRESS), data={'JOBS_STORAGE': js})
        requests.post("{}/config/resetDB".format(ADDRESS))
        noseargs = ['testStorages', '--with-xunit', '--xunit-file=%s_Results.xml' %js]
        nose.run(argv=noseargs)

if __name__ == '__main__':
    main(sys.argv[1:])
