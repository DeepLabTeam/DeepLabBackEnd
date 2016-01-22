import requests

import socket, os
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import ssl

CERTIFICATE_PATH = os.getcwd() + '/deeplab.crt'
KEY_PATH = os.getcwd() + '/deeplab.key'

class DeepLabRequestHandler(BaseHTTPRequestHandler):
    def handle_head(self):
        try:
            main_page = open('site/index.html', 'r').read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(main_page, 'UTF-8'))
        except IOError:
            self.send_error(404, 'derp')

    def do_GET(self):
        path_split = self.path.split('?')
        path = path_split[0].strip('/')

        # Get attributes from URL path
        attr = {}
        if len(path_split) > 1:
            attr_split = path_split[1].split('&')
            for a in path_split:
                a_split = a.split('=')
                if len(a_split) < 2:
                    continue
                key, value = a_split
                attr[key] = value

        # Check for requested file
        content_type = 'text/html'
        extension = path.split('.')[-1]
        read_mode = 'r'
        if extension == 'css':
            content_type = 'text/css'
            read_mode = 'r'
        elif extension == 'png':
            content_type = 'image/png'
            read_mode = 'rb'
        elif extension == 'jpeg' or extension == 'jpg':
            content_type = 'image/jpeg'
            read_mode = 'rb'
        elif extension == 'mp4':
            content_type = 'video/mp4'
            read_mode = 'rb'

        req_file = None
        try:
            with open('site/'+path, read_mode) as f:
                req_file = f.read()
        except:
            pass

        # Handle the request based on the path
        if req_file != None:
            if content_type.split('/')[0] == 'text':
                content = bytes(req_file, 'UTF-8')
            else:
                content = req_file
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        elif path == "":
            self.handle_head()
        else:
            self.send_error(404, 'derp')

def main():
    httpd = HTTPServer(('0.0.0.0', 443), DeepLabRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=CERTIFICATE_PATH, keyfile=KEY_PATH, server_side=True)
    print("Serving DeepLab server...")
    httpd.serve_forever()

####################################################################################################

if __name__ == '__main__':
    main()
