from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.events import subscriber
from pyramid.events import BeforeRender

# def add_global(event):
#     event['project'] = 'Gemstone II'
#     event['page_title'] = "Gemstone II"

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings, root_factory='.resources.Root') as config:
        config.include('.models')
        config.include('pyramid_mako')
        config.include('.routes')
        config.include('.security')
        config.include('pyramid_mailer')
        config.set_default_csrf_options(require_csrf=True)
        config.scan()
    return config.make_wsgi_app()
