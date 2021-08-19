from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import logging
from dbutil import db_connect

log = logging.getLogger(__name__)
log.setLevel(logging.NOTSET)

def run_server():
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('upload', '/upload')
        config.include('pyramid_jinja2')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

if __name__ == '__main__':
    log.info("Started")
    db_connect()
    run_server()