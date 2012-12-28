import json

import requests


def generate_miss_costs(labels, label):
    d = dict([(x, 1.) for x in labels if x != label])
    d[label] = 0.
    return d


class TroiaClient(object):
    ''' Base class providing wrappers for all REST request
    '''

    def __init__(self, base_url, job_id):
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
        return json.loads(req.content)

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
        arg = 'id=' + self.jid
        if typee is not None:
            arg += '&type=' + typee
        return self._do_raw_request(requests.post, "jobs",
                data=arg)

    def delete(self):
        return self._do_raw_request(requests.delete, "jobs",
                data='id=%s' % (self.jid, ))

    def info(self):
        return self._do_request_get("")

    def load_categories_def_prior(self, categories, prior=1.):
        ''' Loads to Troia server given categories.
        Generates default cost matrix
        for them (1. on error, 0. otherwise)

        :param categories: list of categories ids
        :param prior: default priority
        '''
        categories = [{
                'name':c,
                'prior':prior,
                'misclassification_cost':generate_miss_costs(categories, c)
            } for c in categories]
        return self._do_request_post("categories", {'categories': categories})

    def load_categories(self, categories):
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
            } for category, prior, mc in categories]
        return self._do_request_post("categories", {'categories': categories})


# **** PROGRESS BARRIER
    def load_costs(self, costs, idd=None):
        ''' TODO
        '''
        return self._do_request_post("loadCosts",
            {'id': idd, 'costs': costs})

    def _create_assign_label(self, worker, objectn, category):
        return {
            'workerName': worker,
            'objectName': objectn,
            'categoryName': category
        }

    def load_worker_assigned_label(self, worker, objectn, category, idd=None):
        ''' Adds information that given worker voted on given object with given label
        :param worker: worker id
        :param objectn: object id
        :param category: assigned label
        '''
        data = self._create_assign_label(worker, objectn, category)
        return self._do_request_post("loadWorkerAssignedLabel",
            {'id': idd, 'label': data})

    def load_worker_assigned_labels(self, data, idd=None):
        ''' Adding many votes at once

        :param data: iterable with tuples in form (worker_id, object_id, label)
        :param idd: job ID
        '''
        data = [self._create_assign_label(w, o, c) for w, o, c in data]
        return self._do_request_post("loadWorkerAssignedLabels",
            {'id': idd, 'labels': data})

    def _create_gold_label(self, objectn, category):
        return {"objectName": objectn, "correctCategory": category}

    def load_gold_label(self, objectn, category, idd=None):
        ''' Adds gold sample into job

        :param objectn: id of the gold object
        :param category: true category for this object
        :param idd: job ID
        '''
        data = self._create_gold_label(objectn, category)
        return self._do_request_post("loadGoldLabel", {'id': idd, 'label': data})

    def load_gold_labels(self, data, idd=None):
        ''' Adding many gold samples at once

        :param data: iterable of tuples in form (object_id, label)
        :param idd: job ID
        '''
        data = [self._create_gold_label(on, c) for on, c in data]
        return self._do_request_post("loadGoldLabels",
            {'id': idd, 'labels': data})

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

    def compute_blocking(self, iterations, idd=None):
        ''' Starts computations in blocking mode.
        See Troia server documentation for more informations.

        :param iterations: integer with number of iterations to perform
        :param idd: job ID
        '''
        return self._do_request_get("computeBlocking",
            {'id': idd, 'iterations': iterations})


    def compute_non_blocking(self, iterations, idd=None):
        ''' Starts computations in non-blocking mode.
        See Troia server documentation for more informations.

        :param iterations: integer with number of iterations to perform
        :param idd: job ID
        '''
        return self._do_request_get("computeNotBlocking",
            {'id': idd, 'iterations': iterations})

    def compute(self, iterations, idd=None):
        return self.compute_non_blocking(iterations, idd)

    def is_computed(self, idd=None):
        return self._do_request_get("isComputed", {'id': idd})

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
