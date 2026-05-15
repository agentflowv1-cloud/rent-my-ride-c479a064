import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path).path
        if url_path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

port = int(os.environ.get('PORT', 8080))
httpd = HTTPServer(('', port), RequestHandler)
print(f'Server running on port {port}...')
httpd.serve_forever()