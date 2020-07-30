# -*- coding: utf-8 -*-

from django.db import migrations
from django.contrib.auth.models import Group, Permission

from dehaat.settings import ALL_GROUP_NAMES, ALL_PERMISSIONS


def link_permissions(apps, schema_editor):
    for g_name, p_names in ALL_PERMISSIONS.items():
        group = Group.objects.filter(name=g_name).first()
        if not group:
            continue
        permissions = Permission.objects.filter(codename__in=p_names)
        group.permissions.set(permissions)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('useraccount', '0001_create_groups')
    ]

    operations = [
        migrations.RunPython(link_permissions)
    ]