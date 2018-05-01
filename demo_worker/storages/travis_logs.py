import json

from selinon.storages.s3 import S3


class TravisLogsStorage(S3):
    def store(self, node_args, flow_name, task_name, task_id, result):
        # TODO: make this more generic and move generic parts to Selinon's S3 directly
        org, repo = node_args['repo'].split('/', maxsplit=1)
        object_key = 'travis/logs/{org}/{repo}/{build}.json'.format(org=org, repo=repo, build=node_args['build'])
        result = json.dumps(result).encode()
        self._s3.Object(self._bucket_name, object_key).put(Body=result)
        return object_key

    def retrieve(self, flow_name, task_name, task_id):  # noqa
        # TODO: implement
        raise NotImplementedError
