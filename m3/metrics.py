#coding: utf-8

import json
import hashlib
import logging
import time
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out

from m3.actions import ControllerCache

try:
    import pystatsd
except ImportError as ie:
    raise ImportError('Metrics collection is enabled, but we failed to '
                      'import "pystatsd": {0}'.format(unicode(ie)))

prefix = getattr(settings, 'METRICS_PREFIX', None)
host = getattr(settings, 'METRICS_HOST', 'localhost')
port = getattr(settings, 'METRICS_PORT', 8125)
endpoint_url = getattr(settings, 'METRICS_CONTEXTS_URL',
                       'http://localhost:1942/register')

statsd_client = pystatsd.Client(host, port, prefix=prefix)


def gauge_user_count():
    statsd_client.gauge('users.count', User.objects.count())


def gauge_active_users():
    statsd_client.gauge('users.active', Session.objects.count())


def logged_out(**kwargs):
    statsd_client.decr('users.active')


def logged_in(**kwargs):
    statsd_client.incr('users.active')


def user_deleted(**kwargs):
    statsd_client.decr('users.count')


def user_created(**kwargs):
    if not kwargs['instance'].id:
        statsd_client.incr('users.count')


def capture_users_metrics(statsd_client):
    gauge_user_count()
    gauge_active_users()

    if not getattr(User, '__metrics_registered', False):
        post_delete.connect(sender=User, receiver=user_deleted)
        post_save.connect(sender=User, receiver=user_created)

        user_logged_in.connect(receiver=logged_in)
        user_logged_out.connect(receiver=logged_out)

        User.__metrics_registered = True


def send_controllers_contexts():
    def get_hash(s):
        h = hashlib.md5()
        h.update(s)
        return h.hexdigest()

    assert prefix, 'Identity prefix (METRICS_PREFIX) should be specified!'

    ControllerCache.populate()
    controllers = {}    
    
    controller_urls = sorted([c.url for c in ControllerCache._controllers])
    for url in controller_urls:
        controllers[get_hash(url)] = dict(url=url)

    all_urls = [url for c in ControllerCache._controllers for url in c._url_patterns.keys()]
    urls = dict([(get_hash(u), u) for u in all_urls])

    parts = prefix.split('.')
    identity = dict(zip(['version', 'region', 'client', 'product'], parts))
    instance_id = [part for part in parts if part.startswith('instance_')]

    if instance_id:
        identity['instance'] = instance_id[0][9:]

    packet = {
        'timestamp': int(time.time()),
        'info': {
            'controller': controllers,
            'url': urls
        },
        'identity': identity
    }

    try:
        req = urllib2.Request(endpoint_url,
                              data=json.dumps(packet),
                              headers={'Content-Type': 'application/json'})
        urllib2.urlopen(req)
        logging.info('Successfully sent context information.')
    except urllib2.URLError as ue:
        logging.error("Can't send contexts to {0}: {1}".format(endpoint_url, ue))
