import settings
def webapp_add_wsgi_middleware(app):
    if settings.RUN_APP_STATS:
        from google.appengine.ext.appstats import recording
        app = recording.appstats_wsgi_middleware(app)
    return app