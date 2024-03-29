# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-27 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updation_date', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_invoices', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('post_balance', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_ledgers', to='order.Order')),
            ],
        ),
    ]
