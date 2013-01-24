import sys

from client import TroiaClient


COST_MATRIX = [
    ('porn', {
        'porn':     0.2,
        'notporn':  0.8,
    }),
    ('notporn', {
        'notporn':  0.3,
        'porn':     0.7,
    }),
]

GOLD_SAMPLES = [
    ('http://sunnyfun.com', 'notporn'),
    ('http://sex-mission.com', 'porn'),
]

EVALUATION_DATA = [
    ('http://sunnyfun.com', 'notporn'),
    ('http://sex-mission.com', 'porn'),
    ('http://google.com', 'porn'),
    ('http://youporn.com', 'notporn'),
    ('http://yahoo.com', 'notporn')
]

WORKERS_LABELS = [
    ('worker1', 'http://sunnyfun.com', 'porn'),
    ('worker1', 'http://sex-mission.com', 'porn'),
    ('worker1', 'http://google.com', 'porn'),
    ('worker1', 'http://youporn.com', 'porn'),
    ('worker1', 'http://yahoo.com', 'porn'),
    ('worker2', 'http://sunnyfun.com', 'notporn'),
    ('worker2', 'http://sex-mission.com', 'porn'),
    ('worker2', 'http://google.com', 'notporn'),
    ('worker2', 'http://youporn.com', 'porn'),
    ('worker2', 'http://yahoo.com', 'porn'),
    ('worker3', 'http://sunnyfun.com', 'notporn'),
    ('worker3', 'http://sex-mission.com', 'porn'),
    ('worker3', 'http://google.com', 'notporn'),
    ('worker3', 'http://youporn.com', 'porn'),
    ('worker3', 'http://yahoo.com', 'notporn'),
    ('worker4', 'http://sunnyfun.com', 'notporn'),
    ('worker4', 'http://sex-mission.com', 'porn'),
    ('worker4', 'http://google.com', 'notporn'),
    ('worker4', 'http://youporn.com', 'porn'),
    ('worker4', 'http://yahoo.com', 'notporn'),
    ('worker5', 'http://sunnyfun.com', 'porn'),
    ('worker5', 'http://sex-mission.com', 'notporn'),
    ('worker5', 'http://google.com', 'porn'),
    ('worker5', 'http://youporn.com', 'notporn'),
    ('worker5', 'http://yahoo.com', 'porn'),
]



OBJECTS = ['http://sunnyfun.com', 'http://sex-mission.com', 'http://google.com', 'http://youporn.com', 'http://yahoo.com']

ALGORITHMS = ["DS", "MV"]
LABEL_CHOOSING = ["MaxLikelihood", "MinCost"]
COST_ALGORITHM = ["ExpectedCost", "MinCost", "MaxLikelihood"]

def test_all(tc, gold_labels, cost_matrix, labels, eval_data):

    print "STATUS:", tc.status()
    try:
        tc.delete()
    except:
        pass
    print "CREATE:", tc.create(cost_matrix)
    # print "POST_CATEGORIES:", tc.await_completion(
    #         tc.post_categories_def_prior(cost_matrix))
    print "GET COST MATRIX", tc.await_completion(
            tc.get_cost_matrix())
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
    
    for cost_alg in COST_ALGORITHM:
        print "WORKER_ESTM_QUALITY ({}):".format(cost_alg), tc.await_completion(tc.get_prediction_workers_quality(cost_alg))
    
    print "POST_EVALUATION_DATA:", tc.await_completion(tc.post_evaluation_data(eval_data))
    print "GET_EVALUATION_DATA:", tc.await_completion(tc.get_evaluation_data())
    
    for alg in ALGORITHMS:
        for label_choosing in LABEL_CHOOSING + ['Soft']:
            print "DATA_EV_COST ({}, {}):".format(alg, label_choosing), tc.await_completion(tc.get_evaluation_data_cost(alg, label_choosing))
            
    for alg in ALGORITHMS:
        for label_choosing in LABEL_CHOOSING + ["SOFT"]:
            print "DATA_EV_QUALITY ({}, {}):".format(alg, label_choosing), tc.await_completion(tc.get_evaluation_data_quality(alg, label_choosing))
    
    for cost_alg in COST_ALGORITHM:
        print "WORKER_EVAL_QUALITY ({}):".format(cost_alg), tc.await_completion(tc.get_evaluation_workers_quality(cost_alg))

    print "WORKERS_SCORE", tc.await_completion(tc.get_evaluation_workers_score())

if __name__ == "__main__":
    jid = ''
    if len(sys.argv) > 1:
        jid = sys.argv[1]
    tc = TroiaClient('http://localhost:8080/troia-server-0.8/', "ww")
    test_all(tc, GOLD_SAMPLES, COST_MATRIX, WORKERS_LABELS, EVALUATION_DATA)
