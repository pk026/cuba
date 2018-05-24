# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from analytics_app.models import Event, Feedback


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Feedback
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Event
        fields = '__all__'