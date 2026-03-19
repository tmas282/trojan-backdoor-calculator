import requests

def run_client(ip: str, port: int):
    url_stdin = f'http://{ip}:{port}/input'
    resp = requests.get(url_stdin, timeout=60)
    cmd = resp.content
    resp = run(cmd)
    url_stdout = f'http://{ip}:{port}/output?msg={resp}'
    requests.get(url_stdout)
def run(cmd: str) -> str:
    return cmd