"""
Participant authentication scheme.

Verify participant identity using tokens in URLs that are distributed via email.

For example, the URL below would be sent to participant 12345:

https://econvenor.org/my-tasks/12345/b0f43150492dfeac947b5f27dcbed8e49e66283c

The tokens expire after settings.PARTICIPANT_URL_EXPIRY_DAYS (default 100 days),
while their browser remains "authenticated" as per Django session settings.
"""
import datetime
import functools
import hashlib

from django.conf import settings
from django.core import exceptions


EXPIRY_DAYS = getattr(settings, 'PARTICIPANT_URL_EXPIRY_DAYS', 30)
SESSION_KEY = getattr(settings, 'PARTICIPANT_AUTH_SESSION_KEY', 'participant')


def valid_participant_tokens(participant_id):
    """Generate a current list of tokens for a given participant_id."""
    today = datetime.date.today()
    for days in range(EXPIRY_DAYS):
        yield hashlib.sha1(
            '%d:%s:%s' % (
                participant_id,
                today - datetime.timedelta(days=days),
                settings.SECRET_KEY,
            ),
        ).hexdigest()


def current_participant_token(participant_id):
    """Generate today's token for a given participant."""
    return valid_participant_tokens(participant_id).next()


def token_is_valid(participant_id, token):
    """Validate a token for a given participant_id."""
    return token in valid_participant_tokens(participant_id)


def authenticate(request, participant_id, token):
    """Authenticate a request by participant_id and token."""
    participant_id = int(participant_id)
    if token_is_valid(participant_id, token):
        request.session[SESSION_KEY] = {
            'id': participant_id,
            'when': '%s' % datetime.datetime.now(),
        }
    else:
        # TODO: decide if next line is necessary, perhaps you don't mind if
        # participants follow expired links from emails.
        request.session[SESSION_KEY] = {}
        raise exceptions.PermissionDenied()


def participant_required(view):
    """
    Decorator that forces participant is authenticated.

    Raises PermissionDenied if authentication not valid.
    """
    @functools.wraps(view)
    def _participant_required(request, *args, **kwargs):
        """Decorator inner."""
        if request.session.get(SESSION_KEY, {}).get('id') is None:
            raise exceptions.PermissionDenied()
        return view(request, *args, **kwargs)
    return _participant_required
