import json
import time

import requests


def generate_miss_costs(labels, label):
    d = dict([(x, 1.) for x in labels if x != label])
    d[label] = 0.
    return d


class TroiaClient(object):
    ''' Base class providing wrappers for all REST request
    '''

    def __init__(self, base_url, job_id=''):
        '''
        Initializes new client

        :param base_url: address at which Troia server is running
        :param job_id: job ID for which we will be making calls
        '''
        self.url = base_url
        self.jid = job_id
        if not self.url.endswith('/'):
            self.url += '/'

    def _jsonify(self, args=None):
        if isinstance(args, dict):
            new_args = {}
            for k, v in args.iteritems():
                new_args[k] = json.dumps(v)
            return new_args
        return args

    def _do_raw_request(self, method, path, **kwargs):
        req = method(self.url + path, **kwargs)
        resp = json.loads(req.content)
        if not 200 <= req.status_code < 300:
            raise Exception(req.status_code, resp)
        return resp

    def _do_request_get(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(requests.get,
            "jobs/%s/%s" % (self.jid, path), params=args)

    def _do_request_post(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(requests.post,
            "jobs/%s/%s" % (self.jid, path), data=args)

    def _do_request_delete(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(requests.delete,
            "jobs/%s/%s" % (self.jid, path), data=args)

    def ping(self):
        ''' Sends test request. Should return string with current date

        :return: string with current date
        '''
        return self._do_raw_request(requests.get, "status/ping")

    def pingDB(self):
        return self._do_raw_request(requests.get, "status/pingDB")

    def create(self, typee=None):
        arg = ''
        if self.jid:
            arg += 'id=' + self.jid
        if typee is not None:
            arg += '&type=' + typee
        w = self._do_raw_request(requests.post, "jobs",
                data=arg)
        if not self.jid:
            self.jid = w['result'].split(' ')[-1]
        return w

    def delete(self):
        return self._do_raw_request(requests.delete, "jobs",
                data='id=%s' % (self.jid, ))

    def info(self):
        return self._do_request_get("")

    def get_status(self, stat_id):
        return self._do_request_get("status/" + stat_id)

    def await_completion(self, request_response, timeout=0.5):
        if request_response['status'] == 'ERROR':
            raise Exception(request_response['message'])
        status_id = request_response['redirect']
        resp = self.get_status(status_id)
        while resp['status'] == 'NOT_READY':
            time.sleep(timeout)
            resp = self.get_status(status_id)
        return resp

    def post_categories_def_prior_cost(self, categories, prior=1.):
        ''' Loads to Troia server given categories.
        Generates default cost matrix
        for them (1. on error, 0. otherwise)

        :param categories: list of categories ids
        :param prior: default priority
        '''
        categories = [{
                'name': c,
                'prior': prior,
                'misclassification_cost': generate_miss_costs(categories, c)
            } for c in categories]
        return self._do_request_post("categories", {'categories': categories})

    def post_categories_def_prior(self, categories, prior=1.):
        ''' Load categories to Troia server with their cost matrices.
        Costs should be iterable with iterables in form:

        ..

            (name, prior, dict-misclassification_cost { class_ : cost })

        Only default priority is used
        '''
        categories = [{
                'name': category,
                'prior': prior,
                'misclassification_cost': mc
            } for category, mc in categories]
        return self._do_request_post("categories", {'categories': categories})

    def get_categories(self):
        return self._do_request_get("categories")

    def post_gold_data(self, gold_data):
        gold_data = [{
            "correctCategory": label,
            "objectName": obj_id,
        } for obj_id, label in gold_data]
        return self._do_request_post("goldData", {'labels': gold_data})

    def get_gold_data(self):
        return self._do_request_get("goldData")

    def post_assigned_labels(self, assigned_labels):
        assigned_labels = [{
            "workerName": worker,
            "objectName": object_id,
            "categoryName": category,
        } for worker, object_id, category in assigned_labels]
        return self._do_request_post("assignedLabels",
                {"labels": assigned_labels})

    def get_assigned_labels(self):
        return self._do_request_get("assignedLabels")

    def post_compute(self, iterations):
        return self._do_request_post("compute", {'iterations': iterations})

    def get_predictions_for_objects(self):
        return self._do_request_get("prediction/data")

# **** PROGRESS BARRIER
    def load_costs(self, costs, idd=None):
        ''' TODO
        '''
        return self._do_request_post("loadCosts",
            {'id': idd, 'costs': costs})

    def majority_vote(self, objectName, idd=None):
        ''' Returns label? for given object using majority votes rule

        :param objectName: id of object that we want know label
        :param idd: job ID
        '''
        return self._do_request_get("majorityVote",
            {'id': idd, 'objectName': objectName})

    def majority_votes(self, idd=None):
        ''' Returns labels for all objects using
        *majority voting algorithm*.

        :param idd: job ID
        '''
        return json.loads(self._do_request_get("majorityVotes", {'id': idd}))

    def print_worker_summary(self, verbose, idd=None):
        ''' Returns printable workers summary

        :param verbose: definies how much verbose return should be
        :param idd: job ID
        '''
        return self._do_request_get("printWorkerSummary",
            {'id': idd, 'verbose': verbose})

    def print_objects_probs(self, entropy, idd=None):
        return self._do_request_get("printObjectsProbs",
            {'id': idd, 'entropy': entropy})

    def object_probs(self, obj, idd=None):
        ''' Returns given object probability distribution over labels

        :param obj: object id which probability distribution we want
        :param idd: ID of the job which class priorities we want
        '''
        return json.loads(
                self._do_request_get("objectProbs", {'id': idd, 'object': obj}))

    def print_priors(self, idd=None):
        ''' Returns print friendly class priorities in given job

        :param idd: ID of the job which class priorities we want
        '''
        return self._do_request_get("printPriors", {'id': idd})

    def class_priors(self, idd=None):
        ''' Returns class priorities in gvien job

        :param idd: ID of the job which class priorities we want
        '''
        return self._do_request_get("classPriors", {'id': idd})

    def get_dawid_skene(self, idd=None):
        ''' Returns quite big dictionary. See Troia server documentation for more info.

        :param idd: ID of the job which results we want
        '''
        return json.loads(self._do_request_get("getDawidSkene", {'id': idd}))
