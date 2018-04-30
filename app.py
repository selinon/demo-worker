#!/usr/bin/env python3

import sys

from celery.bin.celery import main as celery_main

# Act like we would invoke celery directly.
sys.argv = [
    '/usr/bin/celery',
    'worker',
    '--app=entrypoint',
    '-l', 'INFO',
    '--concurrency=1',
    '-Qfoo',
    '-P', 'solo',
    '--prefetch-multiplier=128',
    '-Ofair',
    '--without-gossip',
    '--without-mingle',
    '--without-heartbeat',
    '--no-color',
]

celery_main()
