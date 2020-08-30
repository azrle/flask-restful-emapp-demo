import os


API_KEY = os.getenv('EMAPP_API_KEY', 'default-test-key')
PREDEFINED_EVENTS = [
    {
        'name': 'foo',
        'location': 'x',
        'start_time': '2020-08-30 18:00:00',  # utc
        'end_time': '2020-08-30 20:00:00',  # utc
    },
    {
        'name': 'bar',
        'location': 'y',
        'start_time': '2020-08-30 19:00:00',  # utc
        'end_time': '2020-09-01 19:00:00',  # utc
    },
]
