from troia_client.client import TroiaClient
from troia_client.testSettings import *
from troia_cont_client.testSettings import *
from troia_cont_client.contClient import TroiaContClient
import threading
from random import randint
import time


def createNominalJob():
        client = TroiaClient(ADDRESS)
        client.create(CATEGORIES)
        jobs.append((client.jid, "NOMINAL"))
        time.sleep(1)
        client.post_assigned_labels(ASSIGNED_LABELS)
        time.sleep(1)
        client.post_evaluation_data(EVALUATION_DATA)
        time.sleep(1)
        client.post_compute(30)


def createContJob():
        contClient = TroiaContClient(ADDRESS)
        contClient.createNewJob()
        jobs.append((contClient.jid, "CONTINUOUS"))
        time.sleep(1)
        contClient.post_assigned_labels(ASSIGNED_LABELS_CONT)
        time.sleep(1)
        contClient.post_gold_data(GOLD_LABELS_CONT)
        time.sleep(1)

if __name__ == '__main__':
    NoThreads = 500
    threads = []
    jobs = []
    for i in range(0, NoThreads):
        jobType = randint(0, 1)
        if jobType:
            t = threading.Thread(target=createNominalJob)
        else:
            t = threading.Thread(target=createContJob)
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
    print len(jobs)
