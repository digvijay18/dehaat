# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import models, serializers
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from apio.api_permissions import IsAdminOrReadOnly


class Products(generics.ListCreateAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return models.Product.objects.filter(active='active')


class Product(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return models.Product.objects
