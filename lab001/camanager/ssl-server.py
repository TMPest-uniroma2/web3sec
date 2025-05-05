import http.server
import ssl
from email.utils import formatdate

# Basic HTTP handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        response_body = b"Hello over HTTPS with a cert chain!\r\n\r\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Server", "PythonHTTPS/1.0")
        self.send_header("Date", formatdate(timeval=None, localtime=False, usegmt=True))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(response_body)

# Server address
server_address = ('0.0.0.0', 4443)

# Create HTTP server instance
httpd = http.server.HTTPServer(server_address, MyHandler)

# Modern TLS context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile='./certs/www.tmpest.local/fullchain.pem',  # This should include server cert + intermediate(s)
    keyfile='./certs/www.tmpest.local/privkey.pem'
)

# Wrap the server socket using the modern SSLContext
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving on https://{server_address[0]}:{server_address[1]}")
httpd.serve_forever()
