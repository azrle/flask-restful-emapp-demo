from flask_restful import Resource
from flask import current_app
from flask.cli import with_appcontext
import click

from emapp.db import get_db


class EventList(Resource):
    def get(self):
        """
        List all events.
        """
        db = get_db()
        events = db.execute(
            'SELECT id, name, start_time, end_time, location'
            ' FROM event ORDER BY id DESC'
        ).fetchall()
        return events


def get_event_by_id(event_id):
    """
    Get a single event by its id.
    Return None if it's not found.
    """
    db = get_db()
    return db.execute((
        'SELECT id, name, start_time, end_time, location '
        'FROM event WHERE id=?'),
        (event_id,)).fetchone()


def init_events():
    """Reset database and insert predefined data."""
    db = get_db()

    from emapp.db import init_db
    init_db()
    for event in current_app.config['PREDEFINED_EVENTS']:
        db.execute(('INSERT INTO event '
                    '(name, location, start_time, end_time)'
                    'VALUES (?,?,?,?)'),
                   (event['name'], event['location'],
                    event['start_time'], event['end_time']))
    db.commit()


@click.command('init-events')
@with_appcontext
def init_events_command():
    """Clear existing data and create new tables."""
    init_events()
    click.echo('Initialized the predefined events.')


def register_cli_commands(app):
    """Register cli command with the Flask app."""
    app.cli.add_command(init_events_command)


def register_endpoints(api):
    """Register endpoints with the Flask app."""
    api.add_resource(EventList, '/events')
