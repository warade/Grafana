# Grafana

 - Run commands
  Activate Virtual Environment
  ```
  source env/bin/activate
  ```
  Run the project
  ```
  python manage.py runserver
  ```
  Go to the browser
  http://127.0.0.1:8000/rest-auth/login/
  try to login
  
  Check the graph on our ec2 server at
  host:3000
  check stats_counts.count metric in it.
  

Everything is set in models only.
Refer models.py

```
from django.db import models
from django.contrib.auth.signals import user_logged_in

# For grafana these libararies should be installed
import graphitesend
from pyformance.meters import counter

from pyformance.registry import MetricsRegistry

global metricsRegistry
metricsRegistry = MetricsRegistry()


def login_handler(sender, user, request, **kwargs):
    # Core code
    counter = metricsRegistry.counter("GET_called")
    counter.inc()
    g = graphitesend.init(prefix='stats_counts', system_name='', graphite_server='your-aws-compute-server')
    g.send('count', counter.get_count())

user_logged_in.connect(login_handler)
```
Don't forget to choose your graphite_server in quickstart/models.py
