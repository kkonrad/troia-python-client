from client.gal import TroiaClient
from nominalJobsTests.testSettings import *
from contJobsTests.testSettings import *
from client.galc import TroiaContClient
from threading import Thread
from random import randint


def check_status(client, response):
    response = client.await_completion(response)
    if response['status'] == 'ERROR':
        print client.jid, response['result'], response.get('stacktrace')
        assert False
    return response


def check_assigns(client, expected):
    w = check_status(client, client.get_assigned_labels())
    if len(w['result']) != expected:
        print "WRONG NUMBER OF ASSIGNS %d, expected %d" % (len(w['result']), expected)


def createNominalJob():
    client = TroiaClient(ADDRESS)
    client.create(CATEGORIES)
    jobs.append((client.jid, "NOMINAL"))
    check_status(client, client.post_assigned_labels(ASSIGNED_LABELS))
    check_status(client, client.post_evaluation_objects(EVALUATION_DATA))
    check_status(client, client.post_compute())
    check_assigns(client, len(ASSIGNED_LABELS))


def createContJob():
    client = TroiaContClient(ADDRESS)
    client.create()
    jobs.append((client.jid, "CONTINUOUS"))
    check_status(client, client.post_assigned_labels(ASSIGNED_LABELS_CONT))
    check_status(client, client.post_gold_data(GOLD_LABELS_CONT))
    check_assigns(client, len(ASSIGNED_LABELS_CONT))


if __name__ == '__main__':
    NoThreads = 300
    threads = []
    jobs = []
    for i in range(NoThreads):
        t = Thread(target=createNominalJob if randint(0, 1) else createContJob,)
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
    print len(jobs)
