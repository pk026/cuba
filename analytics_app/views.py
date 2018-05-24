# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from analytics_app.models import Event, Feedback
from analytics_app.serializers import EventSerializer, FeedbackSerializer


class FeedbackViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class EventViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
