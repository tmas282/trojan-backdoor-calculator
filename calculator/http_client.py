import requests

def run_client(ip: str, port: int):
    url_stdin = f'http://{ip}:{port}/input'
    resp = requests.get(url_stdin, timeout=10)
    url_stdout = f'http://{ip}:{port}/output?msg={resp.content.decode("utf-8")}'
    requests.get(url_stdout)
