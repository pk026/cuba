# cuba
There is a continuous stream of user activity events generated from multiple users as they use our mobile Cube app.
Objective is to implement a server to ingest these events. 
The server will expose a http end-point to which the events would be posted.
Also the server will contain an admin interface to specify business rules, that alert the operator 
(an engineer in the Cube Ops team) or trigger an action (like sending an alert sms to the end user),
when certain criteria is met.
# project design
1. We have two tables event and feedback
2. We have two apis /api/v1/event/ and /api/v1/feedback/
3. User keep posting data on these apis.
4. For now I haven't implemented any athentication and we are relying on client who knows his user id
5. We may implement token based authentication, so client can post data with his token in header of http
6. With token post api we do not need to rely on user and we would his user is using token.
7. We are using pre_save signal of django to trigger the notifications.
8. Every time we save something in event table we check if it is bill payment.
	if yes (no database query in this part)
		a. we fire bill_feedback_timer which checks database feedback table after 15 minutes
		   if any feedback from this user in last 15 minutes. (one database query existance of row?)
			notify cuba operator that this user have not submitted any feedback after bill payment.	
		b. we check if this is first bill mayment of this user
			if yes (one database query)
				invoke a non-blocking celery task which will notify user for his first ever bill mayment.
			else we check if user have 5 or more bill payments transactions in last 5 minutes (one database query may be we can cache bill mayment transaction for 5 minutes to get rid of this query)
				if yes
					add the paid amount if it is 20000 or more
						invoke a non-blocking celery task which notify user for the outstanding bill payment

# stacks used
django, djangorestframework, celery, postgresql, redis

# pre-requisite: install postgresql and redis on machine

# project setup
1. git clone https://github.com/pk026/cuba.git
2. create a virtualenv using: virtualenv venv (install virtualenv on your machine if not already installed)
3. activate environment using: source venv/bin/activate
4. upgrade pip using: pip install --upgrade pip
5. install requirements using: pip install -r requirements.txt
6. make database setting proper: create a database with name:cuba, user:pramod, password: postgres
7. install redis and run it on machine
or you can create database with your own set of parameters and update them into settings.py: DATABASES
7. create database schema using: python manage.py migrate
8. create a superuser: python manage.py createsuperuser

we are ready run project and do testing.
1. run django developement server on terminal: python manage.py runserver
2. start a celery worker in the same environment: celery -A cuba worker --app=cuba.cuba_celery:app --loglevel=info
3. run redis-server  in other terminal in not running redis in deamon mode.

# testing the functionality
post on localhost:8000/api/v1/event/ using postmant or some other client

{
	"user": 1,
	"ts": "1234567890",
	"latlong": "76.865, 98.975",
	"noun": "bill",
	"verb": "paid",
	"time": 5,
	"properties": {"amount": 3000, "type": "electricity"}
}

For demo purpose I just have printed
1. push notification on very first bill pay event for the user: "send first bill pay notification to user"
2. Alert user if 5 or more bill pay events of total value >= 20000 happen within 5 minutes time window: "alert user for more than 5 paiments in 5 minutes"
3. Alert cube operator if bill paid, but did not give feedback within 15 minutes of the bill pay event: "we did not get any feedback for user {0}"

keep posting and looking at the celery workers screen you will find above messages printed.

also you can post feedback on localhost:8000/api/v1/feedback/
data: {
	"user": 1,
	"rating": 4,
	"comment": "test"
}
