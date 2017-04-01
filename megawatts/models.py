# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models


class MegaSite(models.Model):

    class Meta:
        app_label = 'megawatts'

    site_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )


class MegaSiteDetail(models.Model):

    class Meta:
        app_label = 'megawatts'

    date = models.DateField(null=False)
    a_value = models.FloatField(null=False)
    b_value = models.FloatField(null=False)

    site = models.ForeignKey(
        MegaSite,
        blank=False,
        null=False,
        db_index=True
    )