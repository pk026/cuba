# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from .tasks import notify_user, bill_feedback
from analytics_app.utils import import_models


def event_trigger_on_new_event(sender, **kwargs):
    instance = kwargs['instance']
    Event = import_models('Event')
    if instance.noun=='bill' and instance.verb=='paid':
        # start timer to check if feedback comes in 15 mins
        bill_feedback.apply_async((instance.user_id,), countdown=900)
        bill_pay_events = Event.objects.filter(
            user_id=instance.user_id, noun='bill', verb='paid'
        )
        # if bill is paid then check if user paid bill ever before?
        if not bill_pay_events.exists():
            notify_user.apply_async(('first_bill',))
        else:
            # check if 5 or more events happened in last 5 minutes
            # we could rather cache all bill paid transactions to avoid queries
            time = datetime.datetime.now() - datetime.timedelta(minutes=5)
            bill_pay_events = bill_pay_events.filter(
                created__gte=time
            ).order_by('-created')[:5]
            if bill_pay_events.count()>=5:
                paid_value = 0
                for bill_event in bill_pay_events:
                    paid_value += bill_event.properties.get('amount', 0)
                    if paid_value>=20000:
                        notify_user.apply_async(('outstanding_bill',))
                        break