# -*- coding: utf-8 -*-

"""
views.py

:Created: 3/19/14
:Author: timic
"""

import logging
logger = logging.getLogger(__name__)

from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from config import Settings, track_config


@track_config
def api_list(request):
    """

    TODO: придумать как отдавать доку по сервисам
    """
    raise Http404("Not implemented yet")


@track_config
def handle_api_call(request, service):
    conf = Settings()
    return conf.ApiHandler(request, service)


def api_handler(request, service):
    service_handler = Settings.get_service_handler(service)
    if service_handler:
        logger.debug("Hitting service %s" % service)
        return csrf_exempt(service_handler)(request)
    else:
        msg = "Service %s not found" % service
        logger.info(msg)
        raise Http404(msg)
