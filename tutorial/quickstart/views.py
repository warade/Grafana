from django.contrib.auth.models import User
from django.http import Http404

from quickstart.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import graphitesend
# from pyformance.meters import counter
# from pyformance.registry import MetricsRegistry

from rest_auth.views import LoginView

# global metricsRegistry
# metricsRegistry = MetricsRegistry()

class UserList(APIView):
	def get(self, request, format=None):
	    users = User.objects.all()
	    serializer = UserSerializer(users, many=True)
	    # counter = metricsRegistry.counter("GET_called")
	    # counter.inc()
	    # g = graphitesend.init(prefix='test', system_name='', graphite_server='ec2-52-26-169-20.us-west-2.compute.amazonaws.com')
	    # g.send('count', counter.get_count())
	    #print(counter("get_calls").get_count())
	    return Response(serializer.data)

	def post(self, request, format=None):
	    serializer = UserSerializer(data=request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data, status=status.HTTP_201_CREATED)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
	    user = self.get_object(pk)
	    user.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail(APIView):
	def get_object(self, pk):
	    try:
	        return User.objects.get(pk=pk)
	    except User.DoesNotExist:
	        raise Http404

	def get(self, request, pk, format=None):
	    user = self.get_object(pk)
	    user = UserSerializer(user)
	    return Response(user.data)

	def put(self, request, pk, format=None):
	    user = self.get_object(pk)
	    serializer = UserSerializer(user, data=request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
	    user = self.get_object(pk)
	    user.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)
