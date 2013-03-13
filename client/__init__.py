import json
import time
import requests
from abc import ABCMeta, abstractmethod


class AbstractTroiaClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _construct_gold_data(self, objects):
        pass

    @abstractmethod
    def _construct_assigned_labels(self, labels):
        pass

    @abstractmethod
    def _construct_evaluation_data(self, objects):
        pass

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
        return resp

    def _do_request_get(self, path, args=None):
        # args = self._jsonify(args)
        return self._do_raw_request(
            requests.get,
            "%s/%s/%s" % (self.job_type, self.jid, path), params=args)

    def _do_request_post(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(
            requests.post,
            "%s/%s/%s" % (self.job_type, self.jid, path), data=args)

    def _do_request_post_json(self, path, json):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return self._do_raw_request(
            requests.post,
            "%s/%s/%s" % (self.job_type, self.jid, path), data=json, headers=headers)

    def _do_request_delete(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(
            requests.delete,
            "%s/%s/%s" % (self.job_type, self.jid, path), data=args)

    def status(self):
        ''' Sends test request. Should return string with current date

        :return: string with current date
        '''
        return self._do_raw_request(requests.get, "status")

    def delete(self):
        return self._do_raw_request(
            requests.delete,
            self.job_type,
            data='id=%s' % (self.jid))

    def get_status(self, redirect_url):
        return self._do_raw_request(requests.get, redirect_url)

    def await_completion(self, request_response, timeout=0.5):
        if request_response['status'] == 'ERROR':
            raise Exception(request_response)
        redirect_url = request_response['redirect']
        resp = self.get_status(redirect_url)
        while resp['status'] == 'NOT_READY':
            time.sleep(timeout)
            resp = self.get_status(redirect_url)
        return resp

    def get_job_status(self):
        return self._do_request_get("")

    def get_command_status(self, command_id):
        return self._do_request_get('status/' + command_id)

    def post_gold_data(self, objects):
        return self._do_request_post_json(
            "goldObjects",
            json.dumps({"objects": self._construct_gold_data(objects)}))

    def get_gold_data(self):
        return self._do_request_get("goldObjects")

    def get_gold_object(self, objectId):
        return self._do_request_get("goldObjects/%s" % objectId)

    def post_evaluation_objects(self, objects):
        return self._do_request_post_json(
            "evaluationObjects",
            json.dumps({"objects": self._construct_evaluation_data(objects)}))

    def get_evaluation_objects(self):
        return self._do_request_get("evaluationObjects")

    def get_evaluation_object(self, objectId):
        return self._do_request_get("evaluationObjects/%s" % objectId)

    def post_objects(self, objects):
        return self._do_request_post_json(
            "objects",
            json.dumps({"objects": [{"name": obj} for obj in objects]}))

    def get_objects(self, type="all"):
        return self._do_request_get("objects", )

    def get_object(self, objectId):
        return self._do_request_get("objects/%s/info" % objectId)

    def get_object_assigns(self, objectId):
        return self._do_request_get("objects/%s/assigns" % objectId)

    def post_assigned_labels(self, labels):
        return self._do_request_post_json(
            "assigns",
            json.dumps({'assigns': self._construct_assigned_labels(labels)}))

    def get_assigned_labels(self):
        return self._do_request_get("assigns")

    def get_workers(self):
        return self._do_request_get("workers")

    def get_worker_info(self, workerId):
        return self._do_request_get("workers/%s/info" % workerId)

    def get_worker_assigns(self, workerId):
        return self._do_request_get("workers/%s/assigns" % workerId)

    def post_compute(self):
        return self._do_request_post("compute")

    def get_prediction_zip(self):
        return self._do_request_get("prediction/zip")
