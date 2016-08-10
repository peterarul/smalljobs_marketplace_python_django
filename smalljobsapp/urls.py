from django.conf.urls import url
from smalljobsapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_details,name='gig_details'),
]
