import os
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.events import subscriber
from pyramid.events import BeforeRender

# def add_global(event):
#     event['project'] = 'Gemstone II'
#     event['page_title'] = "Gemstone II"

def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    return dict((key, os.path.expandvars(value)) for
                key, value in settings.items())

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # settings = expandvars_dict(settings)
    if os.environ.get('DATABASE_URL', ''):
        settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    with Configurator(settings=settings, root_factory='.resources.Root') as config:
        config.include('.models')
        config.include('pyramid_mako')
        config.include('.routes')
        config.include('.security')
        config.include('pyramid_mailer')
        config.set_default_csrf_options(require_csrf=True)
        config.scan()
    return config.make_wsgi_app()
