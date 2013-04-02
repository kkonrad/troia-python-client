from client.gal import TroiaClient
from nominalJobsTests.testSettings import *


def check_status(res):
    if res['status'] != "OK" or res['result']['job_storage_status'] != "OK":
        print "FAILURE"

if __name__ == "__main__":
    client = TroiaClient(ADDRESS)
    check_status(client.status())
    client.create(CATEGORIES)
    client.await_completion(client.post_assigned_labels(ASSIGNED_LABELS))
    client.await_completion(client.post_gold_data(GOLD_SAMPLES))
    client.await_completion(client.post_compute())
#    client.await_completion(client.get_predictions_objects())
#    client.await_completion(client.get_prediction_workers_quality())
    client.await_completion(client.get_prediction_zip())
    client.delete()
    check_status(client.status())
