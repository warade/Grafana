
# Step 1 For Graphite and Grafana
Tried installing graphite using following link 
https://www.vultr.com/docs/how-to-install-and-configure-graphite-on-ubuntu-16-04
But it didn't work

For Grafana installation
https://grafana.com/docs/installation/debian/
Worked!

Extra notes if nnginx was running on port 80 I had to kill it using
```
ps -eaf | grep nginx
sudo kill -9 1764
```
See if any process still running
```
sudo netstat -tulpn | grep :80
```
Used docker instead:
Used the following link
https://graphite.readthedocs.io/en/latest/install.html#docker
Ran the following code:
```
docker run -d\
 --name graphite\
 --restart=always\
 -p 80:80\
 -p 2003-2004:2003-2004\
 -p 2023-2024:2023-2024\
 -p 8125:8125/udp\
 -p 8126:8126\
 graphiteapp/graphite-statsd
 ```
 Used following handy commands:
 To delete the docker created
 ```
 docker system prune
 ```
 It ran after some time, maybe docker takes time to start.
 
 # Step 2
 Graphite is up running.
 You can see a memUsage file.
 Graphite does read the data, we have to feed it.
 ```
 echo "test.count 4 `date +%s`" | nc -q0 127.0.0.1 2003
 ```
Metric messages need to contain a metric name, a value, and a timestamp. We can do this in our terminal. Let's create a value that will match our test storage schema that we created. We will also match one of the definitions that will add up the values when it aggregates. We'll use the date command to make our timestamp.

# Step 3
if we want relational database to use.
We change the ini file of grafana
which is at
```
/etc/grafana/grafana.ini
```
First, keep in mind that Graphite-web supports Python versions 2.6 to 2.7 and Django versions 1.4 and above.

# Step 4
We want to send the metric to the graphite server, use graphitesend
```
import graphitesend
g = graphitesend.init(prefix='test', system_name='', graphite_server='127.0.0.1')
g.send('count', 10)
```

# Installation of Graphite on aws
1. Install docker
```
sudo apt install docker.io
```
2. Run docker command
```
docker run -d\
 --name graphite\
 --restart=always\
 -p 80:80\
 -p 2003-2004:2003-2004\
 -p 2023-2024:2023-2024\
 -p 8125:8125/udp\
 -p 8126:8126\
 graphiteapp/graphite-statsd
 ```
 It may happen that someone using a port
 To check the port
 ```
 sudo netstat -tulpn | grep :2004
 ps -eaf | grep 31123
 ```
 Try to make sure no one is running on the ports mentioned in docker command
 
3. Run for Graphite
```
your_ec2_host:80
```
Done!

# Installation of Grafana
1. You have to open the port 3000 for EC2 instance.
```
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
curl https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana
```

2. Run the grafana
```
sudo service grafana-server start
```

# Installation of statsd on django application
1. When you have build a django application, we need statsd which listens continously to port 8125
   Hence we have to install statsd which is integrated with django
```
pip install statsd
```
2. In the django app view do the following:
```
from django.shortcuts import render
from statsd.defaults.django import statsd
from django.http import HttpResponse

def someview(request):
	statsd.incr('test.count')
	return HttpResponse('Hello, World!')
```
3. You can find the graph on grafana, path -> stats_count.test.count

NOTE: Above statsd setup worked in localhost
The setup was
- Django project
 - view.py
 ```
 from django.shortcuts import render
 from statsd.defaults.django import statsd
 from django.http import HttpResponse

 def someview(request):
 	 statsd.incr('test.count')
	 return HttpResponse('Hello, World!')
 ```
But didn't worked in AWS
The setup was
- Django proect
 - settings.py
  ```
  STATSD_HOST = 'your_ec2_host'
  STATSD_PORT = 8125
  ```
 - views.py
 same as above

4. What worked then?
Installed pyformance, and feeded the counter data to carbon at 2003 using graphitesend
- Install pyformance
```
pip install pyformance
```
- view.py
```
from django.shortcuts import render
from statsd.defaults.django import statsd
from django.http import HttpResponse
import graphitesend
from pyformance import counter, count_calls

@count_calls
def someview(request):
	#statsd.incr('success.count')
	g = graphitesend.init(prefix='test', system_name='', graphite_server='your_ec2_host')
	g.send('count', counter("someview_calls").get_count())
	return HttpResponse('Hello, World!')
```

Above had issues when the function is def(self, request) and it is in class based view,
As class based views are used in API frameworks, we have to do following method for counter.
Used below view.py
```
import graphitesend
from pyformance.meters import counter
from pyformance.registry import MetricsRegistry

global metricsRegistry
metricsRegistry = MetricsRegistry()

class UserList(APIView):
	def get(self, request, format=None):
	    users = User.objects.all()
	    serializer = UserSerializer(users, many=True)
	    counter = metricsRegistry.counter("GET_called")
	    counter.inc()
	    g = graphitesend.init(prefix='test', system_name='', graphite_server='your_ec2_host')
	    g.send('count', counter.get_count())
	    #print(counter("get_calls").get_count())
	    return Response(serializer.data)
```
Reference: http://techtraits.com/programming/monitoring/python/2013/02/17/Monitoring-python-servers-with-pyformance-and-graphite.html

- nothing was in settings.py as we are not setting statsd.
 	

(Side note -> django_statsd is a middleware that uses python-statsd to log query and view durations to statsd.)
( Blog for statsd - https://codeascraft.com/2011/02/15/measure-anything-measure-everything/ )
( Blog for Login Django code https://medium.freecodecamp.org/user-authentication-in-django-bae3a387f77d )

# links used
https://www.vultr.com/docs/how-to-install-and-configure-graphite-on-ubuntu-16-04
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-graphite-on-an-ubuntu-14-04-server
https://www.digitalocean.com/community/tutorials/an-introduction-to-tracking-statistics-with-graphite-statsd-and-collectd
https://grafana.com/docs/installation/configuration/
https://matt.aimonetti.net/posts/2013/06/26/practical-guide-to-graphite-monitoring/
https://play.grafana.org/d/000000012/grafana-play-home?orgId=1
https://django-statsd.readthedocs.io/en/latest/
https://pyformance.readthedocs.io/en/latest/usage.html
https://github.com/statsd/statsd
https://www.agiliq.com/blog/2014/12/building-a-restful-api-with-django-rest-framework/
