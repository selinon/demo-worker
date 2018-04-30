#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
from celery import Celery
from selinon import Config


def init(with_result_backend=False):
    """ Init Celery and Selinon

    :param with_result_backend: true if the application should connect to the result backend
    :return: Celery application instance
    """
    conf = {
        # TODO: get this from env variables
        'broker_url': os.environ.get('BROKER_URL', 'amqp://rabbitmq:5672'),
    }

    if with_result_backend:
        conf['result_backend'] = os.environ.get('RESULT_BACKEND_URL', 'redis://redis:6379/0')

    app = Celery('app')
    app.config_from_object(conf)


    # Set Selinon configuration
    Config.set_config_yaml(os.path.join(_BASE_NAME, 'nodes.yaml'), flow_definition_files)
    # Prepare Celery
    Config.set_celery_app(app)


# Entrypoint for Celery worker
app = init(with_result_backend=True)
