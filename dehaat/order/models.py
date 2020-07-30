# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from product.models import Product

from dehaat.settings import ACCEPTED, CONFIRMED, DELIVERED, CANCELLED


class Order(models.Model):
    order_status = [
        (ACCEPTED, 'Accepted'),
        (CONFIRMED, 'Confirmed'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=order_status, default=order_status[0][0])


class OrderLine(models.Model):
    orderline_options = [
        ('accepted', 'Accepted'),
        ('confirmed', 'confirmed')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_history')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderlines')
    units = models.IntegerField()
    confirmed_price = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    locked = models.CharField(max_length=15, choices=orderline_options, default=orderline_options[0][0])
