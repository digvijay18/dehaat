# -*- coding: utf-8 -*-

from dehaat.settings import ALL_GROUP_NAMES
from django.db import migrations
from django.contrib.auth.models import Group


def create_groups(apps, schema_editor):
    groups = []
    for group_name in ALL_GROUP_NAMES:
        groups.append(Group(name=group_name))
    Group.objects.bulk_create(groups)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0001_initial'),
        ('financialaccount', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
