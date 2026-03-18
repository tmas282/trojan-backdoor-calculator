import socket
import base64
from charset_normalizer import detect

HOST = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Got Client: ', addr)
        while True:
            while(True):
                cmd = input("> ")
                if cmd == "":
                    print("Can't be empty.")
                    continue
                break
            b_cmd = base64.encodebytes(cmd.encode("ascii"))
            conn.send(b_cmd)

            data = conn.recv(1024)
            std_all = base64.decodebytes(data)
            encDetector = detect(std_all)
            print(std_all.decode(encDetector["encoding"]).encode("utf-8").decode("utf-8"))
