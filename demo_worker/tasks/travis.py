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


def _travis_response(url: str, iter_key: str, params: dict=None, pagination: bool=True) -> typing.Generator:
    """Iterate over a paginated response, yield entries under iter_key key."""
    params = params or {}
    offset = 0
    while True:
        response = _travis_get(url, offset=offset, **params)
        yield from response.json()[iter_key]

        if not pagination or response.json()['@pagination']['is_last']:
            break

        offset += 1


class TravisActiveRepos(SelinonTask):
    """List active repos available for the given organization."""

    def run(self, node_args: dict) -> list:
        organization = node_args['organization']
        url = _TRAVIS_API_URL + f'/owner/{organization}/repos'

        repos = []
        for repo in _travis_response(url, 'repositories', params={'active': 'true'}):
            repos.append(repo['slug'].split('/', maxsplit=1)[1])

        return repos


class TravisRepoBuildsCount(SelinonTask):
    """Retrieve number of builds for the given repo so build ids can be gathered in parallel."""

    def run(self, node_args: dict) -> dict:
        repo = url_quote("{}/{}".format(node_args['organization'], node_args['repo']))
        url = _TRAVIS_API_URL + f'/repo/{repo}/builds'
        response = _travis_get(url, params={'limit': 1})
        return {'count': response.json()['@pagination']['count']}


class TravisRepoBuilds(SelinonTask):
    """Get builds available for the given repo (org/repo slug)."""

    def run(self, node_args: dict) -> list:
        builds = []
        repo = url_quote("{}/{}".format(node_args['organization'], node_args['repo']))
        url = _TRAVIS_API_URL + f'/repo/{repo}/builds'

        response = _travis_get(url, offset=node_args['offset']).json()
        for build in response['builds']:
            if 'finished_at' not in build or not build['finished_at']:
                # Keep track of finished builds.
                continue

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
                'organization': node_args['organization'],
                'repo': node_args['repo'],
                'build': node_args['build'],
                'job': job_id,
                'log': response.text
            })

        return result
