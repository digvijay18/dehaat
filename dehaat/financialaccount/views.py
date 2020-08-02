# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .ledger import LedgerList
from .models import Ledger
from .serializers import LedgerSerializer


class LedgerView(generics.ListCreateAPIView, LedgerList):
    """
    A view to get all ledger entries of a user or to create a new entry for a user.
    The LedgerList can provide custom methods (in this case, a very particular queryset)
    and abstracts away the code so that the view itself can focus on flow rather than code.
    """
    permission_classes = [IsAdminUser]
    serializer_class = LedgerSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return self.query_set_all()
        return Ledger.objects
