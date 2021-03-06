#!/usr/bin/env python
"""
Simple JSON HTTP Server.

https://github.com/mathisonian/simple-testing-server/blob/master/simple-testing-server.py
"""

from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler


class JSONRequestHandler(BaseHTTPRequestHandler):
    """HTTPRequestHander that returns the requested JSON static file."""

    FILE_PREFIX = '.'

    def do_GET(self):
        # Parse the request URL
        parsed_url = urlparse(self.path)
        query_dict = parse_qs(parsed_url.query)
        path = parsed_url.path

        # send response code:
        self.send_response(200)
        # send headers:
        self.send_header("Content-type", "application/json")
        # send a blank line to end headers:
        self.wfile.write("\n")

        try:
            output = open(self.FILE_PREFIX + "/" + path[1:] + ".json", 'r').read()
        except IOError:
            output = '{"error": "Could not find file ' + path[1:] + '.json"}'
        self.wfile.write(query_dict['callback'][0] + '(')
        self.wfile.write(output)
        self.wfile.write(')')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='A simple JSON server.')
    parser.add_argument('-p', '--port', type=int, dest="port", default=8003,
                        help='the port to run the server on; defaults to 8003')
    parser.add_argument('--path', type=str, dest="path", default='.',
                        help='the folder to find the json files')
    args = parser.parse_args()

    JSONRequestHandler.FILE_PREFIX = args.path
    server = HTTPServer(("localhost", args.port), JSONRequestHandler)
    server.serve_forever()
