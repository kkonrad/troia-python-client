#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from client import AbstractTroiaClient


def generate_miss_costs(labels, label):
    d = dict([(x, 1.) for x in labels if x != label])
    d[label] = 0.
    return d


def prepare_categories_def_prior_cost(categories):
    ''' Generates default cost matrix
    for them (1. on error, 0. otherwise)

    :param categories: list of categories ids
    :param prior: default priority
    '''
    return [{
            'name': c,
            'prior': 1. / len(categories),
            'misclassificationCost': generate_miss_costs(categories, c)
        } for c in categories]


def prepare_categories_def_prior(categories):
    ''' Costs should be iterable with iterables in form:
    ..

        (name, prior, dict-misclassification_cost { class_ : cost })

    Only default priority is used
    '''
    return [{
            'name': category,
            'misclassificationCost': mc
        } for category, mc in categories]


class TroiaClient(AbstractTroiaClient):
    ''' Base class providing wrappers for all REST request
    '''
    job_type = "jobs"

    def _construct_gold_data(self, objects):
        return [{
            "name": object_id,
            "goldLabel": label,
        } for object_id, label in objects]

    def _construct_assigned_labels(self, labels):
        return [{
            "worker": worker,
            "object": object_id,
            "label": label,
        } for worker, object_id, label in labels]

    def create(self, categories=None, typee=None):
        arg = ''
        if categories is not None:
            arg += 'categories=' + json.dumps(categories)
        if self.jid:
            arg += '&id=' + str(self.jid)
        if typee is not None:
            arg += '&type=' + typee
        w = self._do_raw_request(requests.post, "jobs", data=arg)
        if not self.jid:
            self.jid = w['result'].split(' ')[-1]
        return w

    def get_categories(self):
        return self._do_request_get("categories")

    # def get_object_prediction(self, object_id):
    #     return self._do_request_get("objects/%s/prediction" % object_id)

    # def get_objects_prediction(self):
    #     return self._do_request_get("objects/prediction")

    # def get_worker_prediction(self, worker_id):
    #     return self._do_request_get("workers/%s/quality/estimated" % worker_id)

    # def get_workers_prediction(self):
    #     return self._do_request_get("workers/quality/estimated")

    def get_objects_prediction(self, algorithm="DS", labelChoosing="MaxLikelihood"):
        return self._do_request_get("objects/prediction", {
            'algorithm': algorithm,
            'labelChoosing': labelChoosing})

    def get_object_prediction(self, object_id, algorithm="DS", labelChoosing="MaxLikelihood"):
        return self._do_request_get("objects/%s/prediction" % object_id, {
            'algorithm': algorithm,
            'labelChoosing': labelChoosing})

    def get_estimated_objects_cost(self, algorithm="DS", cost_algorithm="ExpectedCost"):
        return self._do_request_get("objects/cost/estimated", {
            'algorithm': algorithm,
            'costAlgorithm': cost_algorithm})

    def get_estimated_objects_quality(self, algorithm="DS", cost_algorithm="ExpectedCost"):
        return self._do_request_get("objects/quality/estimated", {
            'algorithm': algorithm,
            'costAlgorithm': cost_algorithm})

    def get_evaluated_objects_cost(self, algorithm, labelChoosing):
        return self._do_request_get("objects/cost/evaluated", {
            'algorithm': algorithm,
            'labelChoosing': labelChoosing})

    def get_evaluated_objects_quality(self, algorithm, labelChoosing):
        return self._do_request_get("objects/quality/evaluated", {
            'algorithm': algorithm,
            'labelChoosing': labelChoosing})

    # def get_cost_matrix(self):
    #     return self._do_request_get("costs")

    # def post_cost_matrix(self, costMatrix):
    #     return self._do_request_post("costs",  {"costs": costMatrix})

    def get_probability_distribution(self, datum, typ=None):
        data = {"type": typ} if typ else None
        return self._do_request_get("objects/{}/categoryProbability".format(datum), data)

    def get_prediction_workers_quality(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("workers/quality/estimated", {
            'costAlgorithm': cost_algorithm})

    def get_evaluation_workers_quality(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("workers/quality/evaluated", {
            'costAlgorithm': cost_algorithm})
