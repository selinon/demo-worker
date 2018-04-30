#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
from celery import Celery
from selinon import Config

from demo_app import get_config_files


BROKER_URL = os.environ['BROKER_URL']


def init(with_result_backend=False):
    """Init Celery and Selinon.

    :param with_result_backend: true if the application should connect to the result backend
    :return: Celery application instance
    """
    conf = {
        'broker_url': BROKER_URL
    }

    if with_result_backend:
        conf['result_backend'] = os.environ['RESULT_BACKEND_URL']

    app = Celery('app')
    app.config_from_object(conf)

    # Set Selinon configuration.
    Config.set_config_yaml(*get_config_files())
    # Prepare Celery
    Config.set_celery_app(app)

    return app


# Entrypoint for Celery worker
app = init(with_result_backend=True)
