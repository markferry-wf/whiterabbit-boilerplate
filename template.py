__author__ = 'Richie Foreman <richie.foreman@gmail.com>'

import os
import settings
from json import dumps as json_dumps
from hashlib import sha1
from jinja2 import Environment, FunctionLoader, FileSystemLoader
import datetime
import google.appengine.api.memcache as memcache

def jinja2_template_loader(templatename):
    '''
    Jinja2 Template caching powered by Memcache.  Updating the current_version_id will invalidate this cache.

    :param templatename:
    :return:
    '''
    key = "jinja:%s:%s" % (templatename,os.environ.get("CURRENT_VERSION_ID"))
    template = memcache.get(key)
    if template is None:
        template = file(templatename).read()
        memcache.set(key,template)
    return template

loader = FunctionLoader(jinja2_template_loader)

if os.environ['SERVER_SOFTWARE'].startswith("Dev"):
    loader = FileSystemLoader(os.path.dirname(__file__))

jinja_environment = Environment(loader=loader,extensions=["jinja2.ext.do"])


def register_filter(func):
    '''
    Quick decorator to add a template filter method. Can also be referenced from controllers as @app.template.register_filter()
    :param func:
    :return:
    '''
    jinja_environment.filters[func.__name__] = func
    return func

@register_filter
def datetimeformat(value, format=None):
    '''
    Format a datetime object

    :param value:
    :param format:
    :return:
    '''

    if format is None:
        format = settings.DATE_FORMAT

    try:
        return value.strftime(format)
    except:
        return ""

@register_filter
def sha1(value,salt=""):
    '''
    Jinja Filter to create a (potentially salted) sha1 hash

    :param value:
    :param salt:
    :return:
    '''
    return sha1(salt+value).hexdigest()

@register_filter
def json_encode(value):
    '''
    Special JSON encoder that has some simple handling of Datetime objects.

    :param value:
    :return:
    '''

    def _handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%m/%d/%Y')
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
    return json_dumps(value,default=_handler)

@register_filter
def format_currency(value):
    '''
    Format a number as currency
    :param value:
    :return:
    '''
    try:
        return "%.2f" % float(value)
    except:
        return "%.2f" % float(0)