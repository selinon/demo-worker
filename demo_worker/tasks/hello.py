from selinon import SelinonTask


class HelloTask(SelinonTask):
    def run(self, node_args):
        """A simple hello world."""
        return {"result": "Hello, {}!".format(node_args.get('name', 'world'))}

