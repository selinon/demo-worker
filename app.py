#!/usr/bin/env python3

import os
import sys
import logging

from celery.bin.celery import main as celery_main
from selinon import Config

from demo_worker import get_config_files

_LOGGER = logging.getLogger(__name__)

Config.set_config_yaml(*get_config_files())

SELINON_DISPATCHER = bool(int(os.getenv('SELINON_DISPATCHER', '0')))
INCLUDE_QUEUES = Config.dispatcher_queues if SELINON_DISPATCHER else Config.task_queues

_LOGGER.info("Worker will listen on %r", INCLUDE_QUEUES)

# Act like we would invoke celery directly from command line.
sys.argv = [
    '/usr/bin/celery',
    'worker',
    '--app=entrypoint',
    '-l', 'INFO',
    '--concurrency=1',
    '-Q', ','.join(INCLUDE_QUEUES),
    '-P', 'solo',
    '--prefetch-multiplier=128',
    '-Ofair',
    '--without-gossip',
    '--without-mingle',
    '--without-heartbeat',
    '--no-color',
]

celery_main()
