# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q, Sum

from rest_framework import generics, exceptions
from rest_framework.response import Response

from . import models, serializers
from dehaat.settings import CUSTOMER_GROUP, CONFIRMED, DELIVERED, CANCELLED
from order.models import Order as OrderModel
from financialaccount.models import Invoice, Ledger
from .tasks import send_order_acceptance_sms_to_primary_mobile


class Orders(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        """
        If the client is a user, we show only his orders.
        else it's admin/agent and we show all orders.
        """
        user = self.request.user
        if user.groups.first().name == CUSTOMER_GROUP:
            return models.Order.objects.filter(user=self.request.user)
        else:
            return models.Order.objects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Order(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        """
        If we are updating the order, we use the updater serializer.
        """
        if self.request.method == 'PATCH':
            return serializers.OrderUpdateSerializer
        return serializers.OrderSerializer

    def get_queryset(self):
        """
        If the request is update, we don't need to define the actually required query set just yet,
        otherwise we define actually required queryset.
        """
        if self.request.method == 'PATCH':
            return models.Order.objects
        return models.Order.objects.prefetch_related('orderlines', 'orderlines__product')

    def check_object_permissions(self, request, obj):
        """
        We grant resource permission in two cases:
        1. Client method is GET and owns the object.
        2. Or client is not a customer (i.e, admin/agent)
        Thus, to deny the request, both the condition must fail together.
        """
        if not ((request.method == 'GET' and request.user == obj.user)\
               or (request.user.groups.first().name != CUSTOMER_GROUP)):
            raise exceptions.PermissionDenied()

    def perform_update(self, serializer):
        """
        This runs on order confirmation and cancellation. It accepts two target states-
        1. confirmed (coming from accepted)
        2. cancelled (coming from confirmed)
        """
        serializer.save()
        order = serializer.instance
        customer = order.user

        # Nothing to do
        if order.status == DELIVERED:
            return

        # Get last standing balance
        last_ledger = customer.ledgers.latest('transaction_date')

        # Get total from just-locked orderlines.
        total = order.orderlines.all().aggregate(total=Sum('sub_total'))

        if order.status == CONFIRMED:
            # Get new balance, create invoice and ledger entries. Send confirmation SMS.
            bal = last_ledger.post_balance - total['total']
            Invoice.objects.create(customer=customer, order=order, agent=self.request.user, amount=total['total'])
            Ledger.objects.create(customer=customer, order=order, amount=-total['total'], post_balance=bal)
            send_order_acceptance_sms_to_primary_mobile.delay(total['total'], order.id, customer.username)

        if order.status == CANCELLED:
            # Get new balance and create reverse ledger entry.
            bal = last_ledger.post_balance + total['total']
            Ledger.objects.create(customer=customer, order=order, amount=total['total'], post_balance=bal)


class PurchaseHistory(generics.ListAPIView):
    """
    Purchase History endpoint is separate from others because this is low-priority data that can
    get heavy over time and don't want others to get slowed down. Client should call this separately
    to show purchase history data. This technique is used to show high priority data first and low
    priority data can take a few extra seconds separately. Only confirmed/delivered order purchases
    are allowed.
    """
    serializer_class = serializers.OrderSerializer

    def get(self, request, *args, **kwargs):
        orders = OrderModel.objects.filter(Q(status=CONFIRMED) | Q(status=DELIVERED), user=request.user)
        purchases = orders.prefetch_related('orderlines__product')
        data = serializers.OrderSerializer(purchases, many=True).data
        response = []
        for order in data:
            response.extend(order['orderlines'])
        return Response(response)
