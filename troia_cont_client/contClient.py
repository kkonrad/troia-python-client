import json
import time
import requests

class TroiaContClient(object):
    ''' Base class providing wrappers for all GALC REST request
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
        return resp

    def _do_request_get(self, path, args=None):
        # args = self._jsonify(args)
        return self._do_raw_request(requests.get,
            "cjobs/%s/%s" % (self.jid, path), params=args)

    def _do_request_post(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(requests.post,
            "cjobs/%s/%s" % (self.jid, path), data=args)

    def _do_request_delete(self, path, args=None):
        args = self._jsonify(args)
        return self._do_raw_request(requests.delete,
            "cjobs/%s/%s" % (self.jid, path), data=args)

    def status(self):
        ''' Sends test request. Should return string with current date

        :return: string with current date
        '''
        return self._do_raw_request(requests.get, "status")
    
    def createNewJob(self):
        w = self._do_raw_request(requests.post, "cjobs")
        if 'New job created with ID: RANDOM_' in w['result']:
            self.jid = w['result'].split(':')[1].strip()
        return w

    def delete(self):
        return self._do_raw_request(requests.delete, "cjobs",
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
        return self._do_raw_request(requests.get, "cjobs/%s" % (self.jid))
                                        
    def get_command_status(self, command_id):
        return self._do_request_get('status/' + command_id)

    def post_gold_data(self, gold_data):
        gold_data = [{
            "objectId": objectId,
            "label": label,
            "zeta": zeta
        } for objectId, label, zeta in gold_data]
        return self._do_request_post("goldData", {'labels': gold_data})

    def get_gold_data(self):
        return self._do_request_get("goldData")
    
    def post_objects(self, data):
        return self._do_request_post("data", {'objects':data})
    
    def get_objects(self, type="all"):
        return self._do_request_get("data", {'type': type})
    
    def get_object_data(self, objectId):
        return self._do_request_get("data/%s" %objectId)
    
    def get_object_assigns(self, objectId):
        return self._do_request_get("data/%s/assignedLabels" %objectId)
    
    def post_assigned_labels(self, assigned_labels):
        assigned_labels = [{
            "worker": worker,
            "object": object,
            "label": label,
        } for worker, object, label in assigned_labels]
        return self._do_request_post("assigns", {"labels": assigned_labels})

    def get_assigned_labels(self):
        return self._do_request_get("assigns")
    
    def get_workers(self):
        return self._do_request_get("workers")
    
    def get_worker_data(self, workerId):
        return self._do_request_get("workers/%s" %workerId)
    
    def get_worker_assigns(self, workerId):
        return self._do_request_get("workers/%s/assigns" %workerId)

    def post_calculate(self):
        return self._do_request_post("calculate")
     
    def get_prediction_objects(self):
        return self._do_request_post("prediction/objects")
    
    def get_prediction_workers(self):
        return self._do_request_post("prediction/workers")


    