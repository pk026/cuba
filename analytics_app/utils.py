# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime


def import_models(model):
    analytics_app_app_models = __import__(
        'analytics_app.models', fromlist=[model]
    )
    model = getattr(analytics_app_app_models, model)
    return model