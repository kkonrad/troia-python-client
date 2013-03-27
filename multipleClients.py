from client.gal import TroiaClient
from troia_client.testSettings import *
from troia_cont_client.testSettings import *
from client.galc import TroiaContClient
from threading import Thread
from random import randint


def createNominalJob():
    client = TroiaClient(ADDRESS)
    client.create(CATEGORIES)
    jobs.append((client.jid, "NOMINAL"))
    client.await_completion(client.post_assigned_labels(ASSIGNED_LABELS))
    client.await_completion(client.post_evaluation_objects(EVALUATION_DATA))
    client.await_completion(client.post_compute())


def createContJob():
    client = TroiaContClient(ADDRESS)
    client.create()
    jobs.append((client.jid, "CONTINUOUS"))
    client.await_completion(client.post_assigned_labels(ASSIGNED_LABELS_CONT))
    client.await_completion(client.post_gold_data(GOLD_LABELS_CONT))

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
