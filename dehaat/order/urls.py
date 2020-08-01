from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', Orders.as_view(), name='orders'),
    url(r'^(?P<pk>[0-9]+)/$', Order.as_view(), name='order'),
    url(r'^history/$', PurchaseHistory.as_view(), name='purchase-history')
]
