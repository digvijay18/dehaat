from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^user/(?P<id>[0-9]+)/$', LedgerView.as_view(), name='ledger'),
]
