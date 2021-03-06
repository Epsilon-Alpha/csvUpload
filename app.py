from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from util.dbutil import db_connect
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def run_server():
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('upload', '/upload')
        config.add_route('get_tables', '/datasets')
        config.add_route('get_headers', '/columns/{table_name}')
        config.add_static_view(name='static', path='static')
        config.include('pyramid_jinja2')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

def main():
    log.debug("Started")
    print("Server started at http://localhost:6543/")
    if not db_connect():
        return
    run_server()

if __name__ == '__main__':
    main()