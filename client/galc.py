import requests
from client import AbstractTroiaClient


class TroiaContClient(AbstractTroiaClient):
    ''' Base class providing wrappers for all GALC REST request
    '''

    job_type = "cjobs"

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
            "name": object_id,
            "goldLabel": {"value": float(label), "zeta": float(zeta)},
        } for object_id, label, zeta in objects]

    def _construct_evaluation_data(self, objects):
        return [{
            "name": object_id,
            "evaluationLabel": {"value": float(label), "zeta": float(zeta)},
        } for object_id, label, zeta in objects]

    def _construct_assigned_labels(self, labels):
        return [{
            "worker": worker,
            "object": object_id,
            "label": {"value": float(label)},
        } for worker, object_id, label in labels]
