"""All jinga filters will be found here."""
from app import app


def datetimeformat(value, format='%d/%m/%Y'):
    """Filter to convert str to datetime."""
    if isinstance(value, str) is True:
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat

from partials.requests import *
