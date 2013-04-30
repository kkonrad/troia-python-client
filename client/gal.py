#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from client import AbstractTroiaClient


def generate_miss_costs(labels, label):
    d = dict([(x, 1.) for x in labels if x != label])
    d[label] = 0.
    return d


class TroiaClient(AbstractTroiaClient):
    ''' Base class providing wrappers for all REST request
    '''
    job_type = "jobs"

    def _construct_gold_data(self, objects):
        return [{
            "name": object_id,
            "goldLabel": label,
        } for object_id, label in objects]

    def _construct_evaluation_data(self, objects):
        return [{
            "name": object_id,
            "evaluationLabel": label,
        } for object_id, label in objects]

    def _construct_assigned_labels(self, labels):
        return [{
            "worker": worker,
            "object": object_id,
            "label": label,
        } for worker, object_id, label in labels]

    def create(self, categories, **kwargs):
        data = {}
        data.update(kwargs)
        data['categories'] = categories
        if 'algorithm' not in data:
            data['algorithm'] = "BDS"
        return super(TroiaClient, self).create(**data)

    def get_categories(self):
        return self._do_request_get("categories")

    def get_objects_prediction(self, labelChoosing="MaxLikelihood"):
        return self._do_request_get("objects/prediction", {
           'labelChoosing': labelChoosing})

    def get_object_prediction(self, object_id, labelChoosing="MaxLikelihood"):
        return self._do_request_get("objects/%s/prediction" % object_id, {
            'labelChoosing': labelChoosing})

    def get_estimated_objects_cost(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("objects/cost/estimated", {
            'costAlgorithm': cost_algorithm})

    def get_estimated_objects_quality(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("objects/quality/estimated", {
            'costAlgorithm': cost_algorithm})

    def get_evaluated_objects_cost(self, labelChoosing):
        return self._do_request_get("objects/cost/evaluated", {
            'labelChoosing': labelChoosing})

    def get_evaluated_objects_quality(self, labelChoosing):
        return self._do_request_get("objects/quality/evaluated", {
            'labelChoosing': labelChoosing})

    def get_cost_matrix(self):
        return self._do_request_get("costs")

    def get_probability_distribution(self, datum):
        return self._do_request_get("objects/{}/categoryProbability".format(datum))

    def get_estimated_workers_quality(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("workers/quality/estimated", {
            'costAlgorithm': cost_algorithm})

    def get_evaluated_workers_quality(self, cost_algorithm="ExpectedCost"):
        return self._do_request_get("workers/quality/evaluated", {
            'costAlgorithm': cost_algorithm})

    def get_workers_confusion_matrix(self):
        return self._do_request_get("workers/quality/matrix")
    
    def get_workers_quality_summary(self):
        return self._do_request_get("workers/quality/summary")
    
    def get_objects_quality_summary(self):
        return self._do_request_get("objects/quality/summary")
