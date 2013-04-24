import sys

from client.gal import TroiaClient
from testSettings import *

LABEL_CHOOSING = ["MaxLikelihood", "MinCost"]
COST_ALGORITHM = ["ExpectedCost", "MinCost", "MaxLikelihood"]


def _test_all(tc, gold_labels, categories, priors, cost_matrix, labels, eval_data):

    print "STATUS:", tc.status()
    try:
        print "DELETE", tc.delete()
    except:
        pass
    print "CREATE:", tc.create(categories, costMatrix=cost_matrix, algorithm="BDS")
    print "GET COST MATRIX", tc.await_completion(
            tc.get_cost_matrix())
    print "GET_CATEGORIES:", tc.await_completion(tc.get_categories())
    print "POST_GOLDS:", tc.await_completion(tc.post_gold_data(gold_labels))
    print "GET_GOLDS:", tc.await_completion(tc.get_gold_data())
    print "POST_ASSIGNS:", tc.await_completion(tc.post_assigned_labels(labels))
    print "GET_ASSIGNS:", tc.await_completion(tc.get_assigned_labels())
    print 'GET_DATA:', tc.await_completion(tc.get_objects())
    print 'GET_WORKERS', tc.await_completion(tc.get_workers())
    print "COMPUTATION:", tc.await_completion(tc.post_compute())

    for label_choosing in LABEL_CHOOSING:
        print "DATA_PREDICTIONS", label_choosing, tc.await_completion(tc.get_objects_prediction(label_choosing))

    for cost_alg in COST_ALGORITHM:
        print "DATA_COST", cost_alg, tc.await_completion(tc.get_estimated_objects_cost(cost_alg))

    for cost_alg in COST_ALGORITHM:
        print "DATA_ESTM_QUALITY", cost_alg, tc.await_completion(tc.get_estimated_objects_quality(cost_alg))

    for d in OBJECTS:
        print "PROB. DIST.", d, tc.await_completion(tc.get_probability_distribution(d))

    for cost_alg in COST_ALGORITHM:
        print "WORKER_ESTM_QUALITY", cost_alg, tc.await_completion(tc.get_estimated_workers_quality(cost_alg))

    print "POST_EVALUATION_DATA:", tc.await_completion(tc.post_evaluation_objects(eval_data))
    print "GET_EVALUATION_DATA:", tc.await_completion(tc.get_evaluation_objects())

    for label_choosing in LABEL_CHOOSING + ['Soft']:
        print "DATA_EV_COST", label_choosing, tc.await_completion(tc.get_evaluated_objects_cost(label_choosing))

    for label_choosing in LABEL_CHOOSING + ["SOFT"]:
        print "DATA_EV_QUALITY", label_choosing, tc.await_completion(tc.get_evaluated_objects_quality(label_choosing))

    for cost_alg in COST_ALGORITHM:
        print "WORKER_EVAL_QUALITY", cost_alg, tc.await_completion(tc.get_evaluated_workers_quality(cost_alg))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        jid = sys.argv[1]
    tc = TroiaClient('http://localhost:8080/troia-server-1.1/')
    _test_all(tc, GOLD_SAMPLES, CATEGORIES, CATEGORY_PRIORS, COST_MATRIX, ASSIGNED_LABELS, EVALUATION_DATA)
