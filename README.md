# Event Manager (demo)

Simple demo of a tool that manage events signups by using Flask-RESTful.

API let users signup an email for an event.
Also let the signup can be removed as well.

Note that an user can sign up only one event at the same time.
The user is identified by the email.

## Setup
```
python3 -m venv venv
. venv/bin/activate

pip3 install -r requirements.txt
cp instance/config{_sample,}.py
```

## Start
* Run local mail server

This is optional if you're using external mail services.

```
. venv/bin/activate
python3 -m aiosmtpd -n -l 127.0.0.1:1025
```

* Test
```
python3 -m pytest -v
```

* Run API server
```
. venv/bin/activate
export FLASK_APP=emapp
export FLASK_ENV=production
export EMAPP_API_KEY=$(uuidgen) # any secret string

# rest all data with predefined events
flask init-events
# run
flask run
```


## APIs
* `Event` object:
    * `id`: event id
    * `name`: event name
    * `start_time`: event start time in UTC
    * `end_time`: event end time in UTC
* `GET /events`
  * List all predefined events.
  * Parameters: None
  * Response
    200: Array of `Event` objects.
  * Errors
    500: Internal error
  * Example
    ```
    # curl -sH "X-SIMPLE-AUTH: $EMAPP_API_KEY" http://127.0.0.1:5000/api/events | jq .
    [
    {
        "id": 2,
        "name": "bar",
        "start_time": "2020-08-30T19:00:00",
        "end_time": "2020-09-01T19:00:00",
        "location": "y"
    },
    {
        "id": 1,
        "name": "foo",
        "start_time": "2020-08-30T18:00:00",
        "end_time": "2020-08-30T20:00:00",
        "location": "x"
    }
    ]
    ```
* `POST /signup/events/<event_id>/email/<email>`
  * Sign up an email for an event.
  * Parameters
    `event_id`: event id of the event to signup
    `email`: email address that will be used to sign up (no validation)
  * Response
    201: Empty result with `Location` header set.
  * Errors
    401: API key is not matched
    404: The event is not found
    409: The email has already signed up for an event
    500: Internal error (including notification failure)
  * Example
    ```
    # curl -sH "X-SIMPLE-AUTH: $EMAPP_API_KEY" -XPOST 'http://127.0.0.1:5000/api/signup/events/1/email/dummy@example.com'
    {}
    ```
* `DELETE /signup/events/<event_id>/email/<email>`
  * Remove an email for an event.
  * Parameters:
    `event_id`: target event id
    `email`: email address will be removed from the event signups
  * Response
    204: Empty result.
  * Errors
    401: API key is not matched
    500: Internal error
  * Example
    ```
    # curl -sH "X-SIMPLE-AUTH: $EMAPP_API_KEY" -XDELETE 'http://127.0.0.1:5000/api/signup/events/1/email/dummy@example.com'
    {}
    ```
* `GET /signup/events/<event_id>`
  * List all signup emails for an event.
  * Parameters:
    `event_id`: target event id
  * Response
    200: Array of event signups (`event_id` and `email`)
  * Errors
    401: API key is not matched
    404: The event is not found
    500: Internal error
  * Example
    ```
    # curl -sH "X-SIMPLE-AUTH: $EMAPP_API_KEY" http://127.0.0.1:5000/api/signup/events/1 | jq .
    [
    {
        "event_id": 1,
        "email": "bar@example.com"
    },
    {
        "event_id": 1,
        "email": "foo@example.com"
    }
    ]
    ```

## Client CLI
```
. venv/bin/activate
export EMAPP_API_KEY=$(uuidgen) # should be same as the above api key

./restful-cli.py --help

# ./restful-cli.py list-events
# ./restful-cli.py signup --event-id=1 --email foo@example.com
# ./restful-cli.py list-signup --event-id=1
# ./restful-cli.py remove-signup --event-id=1 --email foo@example.com
```

## Code reading guide
* `emapp/__init__.py` intialize API server
* `emapp/event.py` defines and registers API endpoint behaviors for event itself.
* `emapp/signup.py` defines and registers API endpoint behaviors for signups.
* Others are helpers.

## None-Goals
* Availability
* Reliablity
  * notification can be missing
  * data can be lost
* Perforamnce
  * mail is sent synchronously (not using queue, etc)
* No pagination
* Simple enough and neither ORM nor SQL builder is used
* Simple enough and not using OpenAPI for code/docs generation
* No API versioning
* No input validation
* Security (API keys, etc.)
* Privacy (including logging)
* Signup is current using `POST` and server does not guarantee idempotent

