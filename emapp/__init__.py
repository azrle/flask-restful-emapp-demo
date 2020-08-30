import os

from flask import Flask
from flask_restful import Api

from emapp.encoder import ApiResponseJSONEncoder


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # flask_restful json encoder config.
        RESTFUL_JSON={
            'indent': None,
            'separators': (',', ':'),
            'cls': ApiResponseJSONEncoder},
        # a default API key that should be overridden by instance config.
        API_KEY='default-test-key',
        # store the database in the instance folder.
        DATABASE=os.path.join(app.instance_path, 'emdb.sqlite'),
        # define events will be inserted into database on initilazation.
        # the format should be as following:
        # {
        #   'name': 'str',
        #   'location': 'str',
        #   'start_time': '2006-01-02 03:04:05',
        #   'end_time': '2006-01-02 03:04:05',
        # }
        # Note that we trust the data and do not validate it.
        PREDEFINED_EVENTS=[],
        # Notification default configs.
        NOTIFICATION={
            'smtp_server': {
                'host': '127.0.0.1',
                'port': 1025,
            },
            'invitation_email_from': 'emapp@example.com',
            'signup_email_from': 'emapp@example.com',
            'signup_email_to': 'emapp@example.com',
        },
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in.
        app.config.update(test_config)

    # ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from emapp import db
    # close database session when a request is finished.
    app.teardown_appcontext(db.close_db)
    # register db init cli commands.
    db.register_cli_commands(app)

    from emapp import event, signup
    # register event cli commands.
    event.register_cli_commands(app)
    # register API endpoints.
    api = Api(app, catch_all_404s=True, prefix='/api')
    event.register_endpoints(api)
    signup.register_endpoints(api)

    return app
