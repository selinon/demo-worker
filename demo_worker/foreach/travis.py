import logging

from selinon import StoragePool

_LOGGER = logging.getLogger(__name__)


def iter_travis_repos(storage_pool: StoragePool, node_args: dict) -> list:
    """Iterate over repos and extend node args with the repo name."""
    try:
        repos = storage_pool.get('travis_active_repos_task')

        new_node_args = []
        for repo in repos:
            new_node_args.append(dict(repo=repo, **node_args))

        return new_node_args
    except Exception as exc:
        _LOGGER.exception(str(exc))
        return []


def iter_travis_builds(storage_pool: StoragePool, node_args: dict) -> list:
    """Iterate over builds found and extend node args with the build information."""
    try:
        builds = storage_pool.get('travis_repo_builds_task')

        new_node_args = []
        for build in builds:
            new_node_args.append(dict(**build, **node_args))

        return new_node_args
    except Exception as exc:
        _LOGGER.exception(str(exc))
        return []