import tkinter as tk
import threading
import sys

import tcp_socket

ip = "localhost"
port = 4444

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python calculator.py <IP> <PORT>")
		sys.exit(1)

	ip = sys.argv[1]
	try:
		port = int(sys.argv[2])
	except ValueError:
		print("PORT must be an integer.")
		sys.exit(1)


stop_event = threading.Event()
worker_thread = None


def worker_task():
    while not stop_event.is_set():
        tcp_socket.run_client(ip, port)

def on_click(button_text):
    current_text = entry.get()
    if button_text == "=":
        try:
            result = eval(current_text)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)


def on_close():
    global worker_thread
    stop_event.set()
    if worker_thread and worker_thread.is_alive():
        worker_thread.join(timeout=2)
    root.destroy()

root = tk.Tk()
root.title("Calculator")
root.protocol("WM_DELETE_WINDOW", on_close)

entry = tk.Entry(root, width=20, font=("Arial", 16), borderwidth=5, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row_val = 1
col_val = 0
for button_text in buttons:
    tk.Button(root, text=button_text, padx=20, pady=20, font=("Arial", 12),
              command=lambda button_text=button_text: on_click(button_text)).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

tk.Button(root, text="C", padx=20, pady=20, font=("Arial", 12), command=lambda: on_click("C")).grid(row=row_val, column=col_val, columnspan=1)


worker_thread = threading.Thread(target=worker_task, name="calculator-worker")
worker_thread.start()

root.mainloop()

stop_event.set()
if worker_thread.is_alive():
    worker_thread.join(timeout=2)
