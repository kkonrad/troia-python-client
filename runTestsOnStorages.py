import requests
import sys
import nose

from nominalJobsTests.testSettings import ADDRESS

JOB_STORAGES = ["MEMORY_FULL", "MEMORY_KV", "DB_FULL", "DB_KV_MEMCACHE_SIMPLE", "DB_KV_SIMPLE"] 
TRIALS = 5

def post_request(url, data={}):
    for _ in xrange(TRIALS):
        response = requests.post(url, data=data)
        if response.ok:
            break
        else:
            print "{}: {}".format(response.reason, response.content)
    if not response.ok:
        assert False, "Failed changing backend"

def main(args):
    for js in JOB_STORAGES:
        print "Working on backend: " + js
        post_request("{}/config".format(ADDRESS), {'JOBS_STORAGE': js})
        post_request("{}/config/resetDB".format(ADDRESS))
        noseargs = ['testStorages', '-v', '--ignore-files=.*testConfig.*', '--with-xunit', '--xunit-file=%s_Results.xml' %js]
        nose.run(argv=noseargs)

if __name__ == '__main__':
    main(sys.argv[1:])
