from restapi import create_app
from asgiref.wsgi import WsgiToAsgi


def create_application():
    wsgi_app = create_app()
    application = WsgiToAsgi(wsgi_app)
    return application
