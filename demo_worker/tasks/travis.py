"""Interact with Travis CI API."""

import os
import typing
from urllib.parse import quote_plus as url_quote

from selinon import SelinonTask
import requests


_TRAVIS_API_URL = 'https://api.travis-ci.org'
_TRAVIS_CI_TOKEN = os.getenv('TRAVIS_CI_TOKEN')


def _travis_get(url: str, **params) -> requests.models.Response:
    """Issue HTTP GET method on the given URL to Travis CI. Check for HTTP status."""
    if _TRAVIS_CI_TOKEN is None:
        raise ValueError("Travis CI token was not provided")

    response = requests.get(url, params=params, headers={
        'Travis-API-Version': '3',
        'Authorization': f'token {_TRAVIS_CI_TOKEN}'
    })
    response.raise_for_status()
    return response


def _paginated_response(url: str, iter_key: str, params: dict=None) -> typing.Generator:
    """Iterate over a paginated response, yield entries under iter_key key."""
    params = params or {}
    offset = 0
    while True:
        response = _travis_get(url, offset=offset, **params)
        yield from response.json()[iter_key]

        if response.json()['@pagination']['is_last']:
            break

        offset += 1

        #break  # TODO


class TravisActiveRepos(SelinonTask):
    """List active repos available for the given organization."""

    def run(self, node_args: dict) -> list:
        organization = node_args['organization']
        url = _TRAVIS_API_URL + f'/owner/{organization}/repos'

        repos = []
        for repo in _paginated_response(url, 'repositories', params={'active': 'true'}):
            repos.append(repo['slug'])

        return repos


class TravisRepoBuilds(SelinonTask):
    """Get builds available for the given repo (org/repo slug)."""

    def run(self, node_args: dict) -> list:
        builds = []
        repo = url_quote(node_args['repo'])
        url = _TRAVIS_API_URL + f'/repo/{repo}/builds'

        for build in _paginated_response(url, 'builds'):
            if 'finished_at' in build and build['finished_at']:
                # Track only the finished ones.
                # TODO: is this check correct?
                jobs = []
                for job in build['jobs']:
                    jobs.append(job['id'])

                builds.append({
                    'build': build['id'],
                    'jobs': jobs
                })

        return builds


class TravisLogTxt(SelinonTask):
    """Download the given log in a text form."""

    def run(self, node_args: dict) -> list:
        result = []

        for job_id in node_args['jobs']:
            url = _TRAVIS_API_URL + f'/job/{job_id}/log.txt'
            response = _travis_get(url)
            result.append({
                'organization': node_args.get('organization'),
                'repo': node_args.get('repo'),
                'build': node_args.get('build'),
                'job': job_id,
                'log': response.text
            })

        return result
