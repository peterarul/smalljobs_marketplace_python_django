from django.conf.urls import url
from smalljobsapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_details, name='gig_details'),
    url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
    url(r'^create_gig/$', views.create_gig, name='create_gig'),
    url(r'^edit_gig/(?P<id>[0-9]+)/$', views.edit_gig, name='edit_gig'),
    url(r'^user_profile/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^preview_profile/(?P<username>\w+)/$', views.preview_profile, name='preview_profile'),
    url(r'^checkouts/$', views.create_purchase, name='create_purchase'),
    url(r'^my_sales/$', views.my_sales, name='my_sales'),
    url(r'^my_purchases/$', views.my_purchases, name='my_purchases'),
    url(r'^category/(?P<link>[\w|-]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
]