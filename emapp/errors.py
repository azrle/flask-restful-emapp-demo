from flask_restful import HTTPException


class ErrAlreadySignup(HTTPException):
    code = 409
    description = 'The email is already signed up to an event.'


class ErrEventNotFound(HTTPException):
    code = 404
    description = 'The event is not found.'


class ErrSignupMailFailure(HTTPException):
    code = 500
    description = ('The email is signed up for the event'
                   ' but failed to send the signup notification.')
