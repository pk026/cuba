# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from cuba.cuba_celery import app
from analytics_app.utils import import_models


@app.task
def notify_user(notif_type):
    if notif_type=='first_bill':
        print "send first bill pay notification to user"
        # call notify api
    elif notif_type=='outstanding_bill':
        print "alert user for more than 5 paiments in 5 minutes"
        # call notify api

@app.task
def bill_feedback(user_id):
    Feedback = import_models('Feedback')
    time = datetime.datetime.now() - datetime.timedelta(minutes=15)
    if not Feedback.objects.filter(user_id=user_id, created__gte=time).exists():
        print "we did not get any feedback for user {0}".format(user_id)
        # notify cuba operator