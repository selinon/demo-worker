import json

from selinon.storages.s3 import S3


class TravisLogsStorage(S3):
    def store(self, node_args, flow_name, task_name, task_id, result):
        object_key = 'travis/logs/{org}/{repo}/1/{build}.json'.format(
            org=node_args['organization'],
            repo=node_args['repo'],
            build=node_args['build']
        )
        result = json.dumps(result).encode()
        self._s3.Object(self._bucket_name, object_key).put(Body=result)
        return object_key

    def retrieve(self, flow_name, task_name, task_id):  # noqa
        # TODO: implement
        raise NotImplementedError
