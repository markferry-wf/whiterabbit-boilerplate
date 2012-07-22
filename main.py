#!/usr/bin/env python

import settings
import app
from decorators import *


@app.wsgi.route("/")
class IndexHandler(app.BaseHandler):
    def get(self):
        return self.renderTemplate("/templates/index.html")