import logging

_LOGGER = logging.getLevelName(__name__)


def iter_travis_repos(storage_pool, node_args: dict) -> list:
    """Iterate over repos and extend node args with the repo name."""
    try:
        repos = storage_pool.get('travis_active_repos')

        new_node_args = []
        for repo in repos:
            new_node_args.append(dict(repo=repo, **node_args))

        return new_node_args
    except Exception as exc:
        _LOGGER.exception(str(exc))
        return []
