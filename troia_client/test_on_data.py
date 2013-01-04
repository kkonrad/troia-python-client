import sys

from client import TroiaClient


COST_MATRIX = [
    ('porn', {
        'porn':     0.,
        'notporn':  1.,
    }),
    ('notporn', {
        'notporn':  0.,
        'porn':     1.,
    }),
]

GOLD_SAMPLES = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
]

EVALUATION_DATA = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
    ('url3', 'porn'),
    ('url4', 'notporn'),
    ('url5', 'notporn')
]

WORKERS_LABELS = [
    ('worker1', 'url1', 'porn'),
    ('worker1', 'url2', 'porn'),
    ('worker1', 'url3', 'porn'),
    ('worker1', 'url4', 'porn'),
    ('worker1', 'url5', 'porn'),
    ('worker2', 'url1', 'notporn'),
    ('worker2', 'url2', 'porn'),
    ('worker2', 'url3', 'notporn'),
    ('worker2', 'url4', 'porn'),
    ('worker2', 'url5', 'porn'),
    ('worker3', 'url1', 'notporn'),
    ('worker3', 'url2', 'porn'),
    ('worker3', 'url3', 'notporn'),
    ('worker3', 'url4', 'porn'),
    ('worker3', 'url5', 'notporn'),
    ('worker4', 'url1', 'notporn'),
    ('worker4', 'url2', 'porn'),
    ('worker4', 'url3', 'notporn'),
    ('worker4', 'url4', 'porn'),
    ('worker4', 'url5', 'notporn'),
    ('worker5', 'url1', 'porn'),
    ('worker5', 'url2', 'notporn'),
    ('worker5', 'url3', 'porn'),
    ('worker5', 'url4', 'notporn'),
    ('worker5', 'url5', 'porn'),
]



OBJECTS = ['url1', 'url2', 'url3', 'url4', 'url5']

ALGORITHMS = ["DS", "MV"]
LABEL_CHOOSING = ["MaxLikelihood", "MinCost"]
COST_ALGORITHM = ["ExpectedCost", "MinCost"]

def test_all(tc, gold_labels, cost_matrix, labels, eval_data):

    print "PING:", tc.ping()
    try:
        tc.delete()
    except:
        pass
    print "CREATE:", tc.create(cost_matrix)
    # print "POST_CATEGORIES:", tc.await_completion(
    #         tc.post_categories_def_prior(cost_matrix))
    print "GET_CATEGORIES:", tc.await_completion(
            tc.get_categories())
    print "POST_GOLDS:", tc.await_completion(
            tc.post_gold_data(gold_labels))
    print "GET_GOLDS:", tc.await_completion(
            tc.get_gold_data())
    print "POST_ASSIGNS:", tc.await_completion(
            tc.post_assigned_labels(labels))
    print "GET_ASSIGNS:", tc.await_completion(
            tc.get_assigned_labels())
    print 'GET_COST_MATRIX:', tc.await_completion(tc.get_cost_matrix())

    print "COMPUTATION:", tc.await_completion(
            tc.post_compute(50))

    for alg in ALGORITHMS:
        for label_choosing in LABEL_CHOOSING:
            print "DATA_PREDICTIONS ({}, {}):".format(alg, label_choosing), tc.await_completion(tc.get_predictions_objects(alg, label_choosing))

    for alg in ALGORITHMS:
        for cost_alg in COST_ALGORITHM:
            print "DATA_COST ({}, {})".format(alg, cost_alg), tc.await_completion(tc.get_prediction_data_cost(alg, cost_alg))

    for alg in ALGORITHMS:
        for cost_alg in COST_ALGORITHM:
            print "DATA_ESTM_QUALITY ({}, {}):".format(alg, cost_alg), tc.await_completion(tc.get_prediction_data_quality(alg, cost_alg))

    for alg in ALGORITHMS:
        for d in OBJECTS:
            print "PROB. DIST. ({}) for {}:".format(alg, d), tc.await_completion(tc.get_probability_distribution(d, alg))
    
    print "POST_EVALUATION_DATA:", tc.await_completion(tc.post_evaluation_data(eval_data))
    print "GET_EVALUATION_DATA:", tc.await_completion(tc.get_evaluation_data())
    
    for alg in ALGORITHMS:
        for label_choosing in LABEL_CHOOSING:
            print "DATA_EV_COST ({}, {}):".format(alg, label_choosing), tc.await_completion(tc.get_evaluation_data_cost(alg, label_choosing))

#    print "DATA_EV_QUALITY:", tc.await_completion(
#            tc.get_evaluation_data_quality())


if __name__ == "__main__":
    jid = ''
    if len(sys.argv) > 1:
        jid = sys.argv[1]
    tc = TroiaClient('http://localhost:8080/troia_server2/rest', jid)
    test_all(tc, GOLD_SAMPLES, COST_MATRIX, WORKERS_LABELS, EVALUATION_DATA)
