# -*- coding: utf-8 -*-

from django.db import migrations
from django.contrib.auth.models import Group, User

from dehaat.settings import ADMIN_GROUP, ADMIN_USERNAME, ADMIN_PASSWORD


def add_default_admin(apps, schema_editor):
    group = Group.objects.filter(name=ADMIN_GROUP).first()
    user = User.objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, email='')
    user.groups.add(group)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('useraccount', '0002_link_permissions')
    ]

    operations = [
        migrations.RunPython(add_default_admin)
    ]