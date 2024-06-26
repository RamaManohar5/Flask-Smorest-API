from restapi import create_app
from asgiref.wsgi import WsgiToAsgi

wsgi_app = create_app()
application = WsgiToAsgi(wsgi_app)