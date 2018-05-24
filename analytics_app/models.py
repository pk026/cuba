# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    user = models.ForeignKey(User)
    ts = models.CharField(max_length=16)
    latlong = models.CharField(max_length=16, null=True, blank=True)
    noun = models.CharField(max_length=16, null=True, blank=True)
    verb = models.CharField(max_length=16, null=True, blank=True)
    time = models.CharField(max_length=8, null=True, blank=True)
    properties = JSONField(default={})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Feedback(models.Model):
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    comment = models.CharField(max_length=64, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)