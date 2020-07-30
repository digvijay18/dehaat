# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Product(models.Model):
    product_status = [
        ('active', 'Currently Selling'),
        ('inactive', 'Not Up For Sale')
    ]
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    features = JSONField(null=False)
    price = models.FloatField(null=False)
    units = models.IntegerField(null=False)
    active = models.CharField(max_length=15, choices=product_status, default=product_status[0][0])


'''
## Second Approach on modelling product data

class ProductBasic(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField(max_length=500)
    company = models.CharField(max_length=50) # An example that shows common basic data (or foreign key)


class ProductVariety(models.Model):
    display_choices = [
        ('incr', 'Increasing Lexicographical Order'),
        ('decr', 'Decreasing Lexicographical Order'),
        ('custom', 'Specify Order in Array')
    ]
    basic_info = models.ManyToManyField(
        ProductBasic, through='Product', through_fields=('product_variety', 'product_basic')
    )
    features = JSONField(default={})
    display_setting = models.CharField(choices=display_choices) 
    # Above and below are examples of variety dependent data (apart from just features)
    custom_display_order = ArrayField(models.CharField(null=False), default=[])


## A product is the combination of common data plus varied features data
   For eg:- an earphone with plain color or with printed design may vary in price, stock, etc.
   
class Product(models.Model):
    product_status = [
        ('active', 'Currently Selling'),
        ('inactive', 'Not Up For Sale')
    ]
    product_basic = models.ForeignKey(ProductBasic, on_delete=models.CASCADE)
    product_variety = models.ForeignKey(ProductVariety, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    units = models.IntegerField(default=0)
    active = models.CharField(choices=product_status, default=product_status[0][0])
'''