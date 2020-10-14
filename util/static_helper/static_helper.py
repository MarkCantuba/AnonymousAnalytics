# https://stackoverflow.com/questions/12193803/invoke-python-simplehttpserver-from-command-line-with-no-cache-option
# Adapted from https://github.com/python/cpython/blob/3.9/Lib/http/server.py#L1262
# LICENSE: https://github.com/python/cpython/blob/master/LICENSE


import http.server
import argparse
import contextlib
from functools import partial


parser = argparse.ArgumentParser()
parser.add_argument('--bind', '-b', metavar='ADDRESS', default='localhost',
                    help='Specify alternate bind address [default: localhost]')
parser.add_argument('--directory', '-d', default='../../static',
                    help='Specify alternative directory [default: <project_root>/static]')
parser.add_argument('port', action='store', default=80, type=int, nargs='?',
                    help='Specify alternate port [default: 80]')
args = parser.parse_args()


class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")


class DualStackServer(http.server.ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(
                socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


http.server.test(
    HandlerClass=partial(NoCacheHTTPRequestHandler, directory=args.directory),
    ServerClass=DualStackServer,
    port=args.port,
    bind=args.bind,
)
