# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-12 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0009_copountrace'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CopounTrace',
            new_name='CouponTrace',
        ),
    ]