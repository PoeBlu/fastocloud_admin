#!/usr/bin/env python3

import logging
import argparse
import gevent
from gevent.pywsgi import WSGIServer

from app import app, servers_manager

PROJECT_NAME = 'fastocloud_iptv_admin'
HOST = '0.0.0.0'
PORT = 8080
LOGS_PATH = PROJECT_NAME + '.log'


def servers_refresh():
    servers_manager.refresh()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=PROJECT_NAME, usage='%(prog)s [options]')
    parser.add_argument('--port', help='port (default: {0})'.format(PORT), default=PORT)
    parser.add_argument('--host', help='host (default: {0})'.format(HOST), default=HOST)
    parser.add_argument('--logs_path', help='logs path (default: {0})'.format(LOGS_PATH), default=LOGS_PATH)

    argv = parser.parse_args()

    logging.basicConfig(filename=argv.logs_path, level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

    http_server = WSGIServer((argv.host, argv.port), app)
    srv_greenlet = gevent.spawn(http_server.serve_forever)
    alarm_greenlet = gevent.spawn(servers_refresh)

    try:
        gevent.joinall([srv_greenlet, alarm_greenlet])
    except KeyboardInterrupt:
        servers_manager.stop()
        http_server.stop()
