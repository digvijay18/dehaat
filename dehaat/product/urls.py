from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', Products.as_view(), name='products'),
    url(r'^(?P<pk>[0-9]+)/$', Product.as_view(), name='product'),
]
