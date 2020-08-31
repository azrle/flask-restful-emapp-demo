import sqlite3
from flask import url_for, current_app
from flask_restful import Resource

from emapp.db import get_db
from emapp.event import get_event_by_id
from emapp.errors import (
    ErrAlreadySignup, ErrEventNotFound, ErrSignupMailFailure)
from emapp.notification import Notification
from emapp.auth import auth_simple_token


class Signup(Resource):
    method_decorators = [auth_simple_token]

    def post(self, event_id, email):
        """
        Signup an email for the given event_id.
        """
        try:
            event = get_event_by_id(event_id)
            if not event:
                raise ErrEventNotFound
            db = get_db()
            db.execute(
                "INSERT INTO signup(email, event_id) VALUES(?,?)",
                (email, event_id))
            db.commit()
        except sqlite3.IntegrityError as e:
            if str(e).startswith('FOREIGN KEY'):
                raise ErrEventNotFound
            # UNIQUE constraint of primary key.
            raise ErrAlreadySignup
        try:
            notification = Notification(event=event, signup_email=email)
            notification.send_signup_email()
            notification.send_invitation()
        except Exception as e:
            current_app.logger.error(
                "failed to send signup (%s for %s(id=%d)) notification: %s",
                email, event['name'], event_id, e)
            raise ErrSignupMailFailure
        return {}, 201, {
            'Location': url_for('signup_emails_list', event_id=event_id)}

    def delete(self, event_id, email):
        """
        Remove an email from the given event_id.
        """
        db = get_db()
        db.execute(
            "DELETE FROM signup WHERE email=? AND event_id=?",
            (email, event_id))
        db.commit()
        return {}, 204


class SignupEmailsList(Resource):
    method_decorators = [auth_simple_token]

    def get(self, event_id):
        """
        List all emails signed up to the given event.
        """
        event = get_event_by_id(event_id)
        if not event:
            raise ErrEventNotFound
        db = get_db()
        emails = db.execute(
            ('SELECT event_id, email FROM signup WHERE'
             ' event_id=? ORDER BY email'),
            (event_id,)).fetchall()
        return emails


def register_endpoints(api):
    """Register endpoints with the Flask app."""
    api.add_resource(
        Signup, '/signup/events/<int:event_id>/email/<email>')
    api.add_resource(
        SignupEmailsList, '/signup/events/<int:event_id>',
        endpoint='signup_emails_list')
