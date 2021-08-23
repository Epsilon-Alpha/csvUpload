from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import logging
from util.dbutil import db_connect

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def run_server():
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('upload', '/upload')
        config.add_route('get_tables', '/tables')
        config.add_route('get_headers', '/columns/{table}')
        config.add_static_view(name='static', path='static')
        config.include('pyramid_jinja2')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

if __name__ == '__main__':
    log.debug("Started")
    print("Server started at http://localhost:6543/")
    db_connect()
    run_server()