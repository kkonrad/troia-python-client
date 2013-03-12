import requests
from client import AbstractTroiaClient


class TroiaContClient(AbstractTroiaClient):
    ''' Base class providing wrappers for all GALC REST request
    '''

    job_type = "cjobs"

    def create(self):
        post_data = "id=" + str(self.jid) if self.jid else None
        w = self._do_raw_request(requests.post, "cjobs", data=post_data)
        if 'New job created with ID: RANDOM_' in w['result']:
            self.jid = w['result'].split(':')[1].strip()
        return w

    def get_object_prediction(self, object_id):
        return self._do_request_get("objects/%s/prediction" % object_id)

    def get_objects_prediction(self):
        return self._do_request_get("objects/prediction")

    def get_worker_prediction(self, worker_id):
        return self._do_request_get("workers/%s/quality/estimated" % worker_id)

    def get_workers_prediction(self):
        return self._do_request_get("workers/quality/estimated")

    def _construct_gold_data(self, objects):
        return [{
            "object": object_id,
            "label": {"value": float(label), "zeta": float(zeta)},
        } for object_id, label, zeta in objects]

    def _construct_assigned_labels(self, labels):
        return [{
            "worker": worker,
            "object": object_id,
            "label": {"value": float(label)},
        } for worker, object_id, label in labels]
