from django.conf.urls import include, url
from django.contrib import admin
from quickstart import views
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view()),
	url(r'rest-auth/', include('rest_auth.urls')),
	#url(r'rest-auth/registration/', include('rest_auth.registration.urls')),
]