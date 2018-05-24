# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save
from .signals import event_trigger_on_new_event

class AnalyticsAppConfig(AppConfig):
    name = 'analytics_app'

    def ready(self):
        event_class = self.get_model('Event')
        pre_save.connect(
            event_trigger_on_new_event,
            sender=event_class,
            dispatch_uid="analytics_app_app.event_trigger"
        )