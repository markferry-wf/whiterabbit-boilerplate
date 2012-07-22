#!/usr/bin/env python

import webapp2
import os
from webapp2_extras import sessions
from google.appengine.api import users as ga_users
_webapp = webapp2
import settings
import template
import logging
from models import User
import json

class WSGIApplication(_webapp.WSGIApplication):
    def __init__(self, *args, **kwargs):
        kwargs["config"] = settings.webapp2_config
        kwargs["debug"] = settings.APP_DEBUG
        
        super(WSGIApplication, self).__init__(*args, **kwargs)

    def route(self, template, *args, **kwargs):
        '''
        Decorator: Register a class a url handler
        :param template:
        :param args:
        :param kwargs:
        :return:
        '''
        def wrapper(func):
            self.router.add(webapp2.Route(template,handler=func, *args, **kwargs))
            return func

        return wrapper

class BaseHandler(_webapp.RequestHandler):
    def dispatch(self):

        self.user = User()

        '''
         Method dispatcher for wrapping method calls within the context of 'self'

         Any variables created here are given to the method handlers as 'self'
        :return:
        '''
        self.session_store = sessions.get_store(request=self.request)
        try:
            # call method handler
            results = _webapp.RequestHandler.dispatch(self)
            if results is True:
                self.response.set_status(200)
            elif results is False:
                self.response.set_status(501)
            elif results is dict or results is list:
                # nah -- it's another type, it's JSON
                self.response.content_type = "application/json"
                self.response.out.write(json.dumps(results))
            elif results is None:
                self.response.set_status(200)
                logging.info("null response from handler")
            else:
                self.response.out.write(results)

        finally:
            # store session
            self.session_store.save_sessions(self.response)
    
    @_webapp.cached_property
    def session(self):
        '''
        This method enables the self.session dictionary for referencing current session data.

        :return:
        '''
        return self.session_store.get_session(backend=settings.SESSION_BACKEND)

    @_webapp.cached_property
    def jinja(self):
        return template.jinja_environment

    def flash(self,message,type="warning"):
        '''
        Add a quick flash alert message to the template.
        :param message:
        :param type:
        :return:
        '''
        self.session.add_flash(value=message,level=type)
    
    def handle_exception(self, exception, debug):
        '''
        Simple exception handler to draw a 'pretty page'

        :param exception:
        :param debug:
        :return:
        '''

        # We are handling an HTTPException.
        if hasattr(exception,"status"):
            if str(exception.status).startswith("403"):
                self.response.set_status(403)
                return self.renderTemplate("templates/_denied.html",uri=self.request.uri)

        # default handler
        # log the exception
        import traceback
        self.response.set_status(500)
        logging.exception(exception)
        return self.renderTemplate("templates/_exception.html", exception=traceback.format_exc())

    def renderTemplate(self, t,  *args, **kwargs):
        '''
        Render a Jinja Template, taking template variables as **kwargs

        :param t:
        :param kwargs:
        :return:
        '''

        # inject some template variables
        kwargs.update({
           "url": self.request.url,
           "path": self.request.path,
           "settings": settings,
           "_flash": self.session.get_flashes(),
           "user": ga_users.get_current_user(),
           "is_admin": ga_users.is_current_user_admin(),
           "os_environ": os.environ
        })

        return self.jinja.get_template(t).render(**kwargs)

wsgi = WSGIApplication()