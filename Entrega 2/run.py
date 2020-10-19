#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import smtplib, ssl
import json
import time
import sys

port = 1025 # For SSL
smtp_server = "localhost"

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=HTTPStatus.OK.value):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def validate(self, data):
        """ Valida datos de la request POST para el envio de mail

        Parameters:
            data(dict): Diccionario con el remitete "from", contraseña "password"
                destinatario "to" y el mensaje "message" del mail a enviar

        Returns:
            str: En caso de que falte algun campo
            None: Datos completos
        """

        # iterate over required fields: from, to, message
        for field in ['from', 'password', 'to', 'message']:
            if not data.get(field):
                return f'Field `{field}` is required'

        return None

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length))

        # handle request validation
        message = self.validate(data)

        if message:
            self._set_headers(code=HTTPStatus.BAD_REQUEST.value)
            self.wfile.write(json.dumps({ 'success': False, 'message': message }).encode('utf-8'))
            return

        print(f'Connecting with {smtp_server}:{port}')

        # create ssl context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(data['from'], data['password'])
            server.sendmail(data['from'], data['to'], data['message'])

        print(f'Mail sent')

        self._set_headers()
        self.wfile.write(json.dumps({ 'success': True }).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    global smtp_server
    global port

    if len(sys.argv) > 1:
        smtp_server = sys.argv[1]

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Serving at %s:%d' % server_address)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
