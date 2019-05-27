from django.db import models
from django.contrib.auth.signals import user_logged_in

# For grafana
import graphitesend
from pyformance.meters import counter
from pyformance.registry import MetricsRegistry
#from pystatsd import Client

# For grafana
global metricsRegistry
metricsRegistry = MetricsRegistry()


def login_handler(sender, user, request, **kwargs):
    counter = metricsRegistry.counter("GET_called")
    counter.inc()
    g = graphitesend.init(prefix='stats_counts', system_name='', graphite_server='your-aws-compute-server')
    g.send('count', counter.get_count())

user_logged_in.connect(login_handler)
