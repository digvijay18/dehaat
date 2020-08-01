from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', Account.as_view(), name='account'),
    url(r'^customer/$', LoginMobileNumber.as_view(), name='login-mobile'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
]
