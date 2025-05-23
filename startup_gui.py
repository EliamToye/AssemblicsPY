#!/usr/bin/env python3
import subprocess
import sys
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue

option_count = 0
last_option = None
active_option_label = None
script_is_running = False
process = None
log_file = "testlog.txt"
delay_time = 5000
scheduled_task = None
script_queue = queue.Queue()

scripts = {
    "1": "V3test1.py",
    "2": "V2test2.py",
    "3": "test3.py"
}

def enqueue_script(option, serienummer):
    script_queue.put((option, serienummer))
    if not script_is_running:
        run_next_script()

def run_next_script():
    global script_is_running
    if not script_queue.empty():
        option, serienummer = script_queue.get()
        run_script(option, serienummer)
    else:
        script_is_running = False

def run_script(option, serienummer=None):
    global script_is_running, process

    if option not in scripts:
        log_output.insert(tk.END, "X Ongeldige optie, probeer opnieuw.\n")
        return

    script_is_running = True
    input_entry.config(state='disabled')
    log_output.insert(tk.END, f"\n V Start script: {scripts[option]}...\n")
    root.update()

    command = [sys.executable, scripts[option]]
    if serienummer:
        command.append(serienummer)

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True
        )

        def reader_thread():
            for line in process.stdout:
                log_output.insert(tk.END, line)
                log_output.see(tk.END)
            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                log_output.insert(tk.END, f"\n V {scripts[option]} voltooid.\n")
            else:
                log_output.insert(tk.END, f"\n X {scripts[option]} beeindigd met foutcode {process.returncode}.\n")

            log_output.see(tk.END)

            root.after(0, reset_after_script)

        threading.Thread(target=reader_thread, daemon=True).start()

    except Exception as e:
        log_output.insert(tk.END, f" X Fout: {e}\n")
        reset_after_script()

def reset_after_script():
    global script_is_running
    script_is_running = False
    input_entry.config(state='normal')
    input_entry.delete(0, tk.END)
    input_entry.focus()
    run_next_script()

def on_user_input(event=None):
    global scheduled_task
    if scheduled_task:
        root.after_cancel(scheduled_task)
    scheduled_task = root.after(delay_time, process_input)

def process_input():
    global last_option

    if script_is_running:
        return

    user_input = input_entry.get().strip()
    if not user_input:
        return

    input_upper = user_input.upper()

    if "PIM" in input_upper:
        last_option = "2"
        log_output.insert(tk.END, f" V PIM gedetecteerd. Wacht op serienummer...\n")
        active_option_label.config(text="Actieve optie: PIM")
    elif "RISPR" in input_upper:
        last_option = "1"
        log_output.insert(tk.END, f" V RISPR gedetecteerd. Wacht op serienummer...\n")
        active_option_label.config(text="Actieve optie: RISPR")
    elif "RISPE" in input_upper:
        last_option = "3"
        log_output.insert(tk.END, f" V RISPE gedetecteerd. Wacht op serienummer...\n")
        active_option_label.config(text="Actieve optie: RISPE")
    elif last_option and re.match(r"^[A-Za-z0-9\-]+$", user_input):
        log_output.insert(tk.END, f" V Serienummer ingevoerd: {user_input}\n")
        enqueue_script(last_option, serienummer=user_input)
    else:
        log_output.insert(tk.END, " X Ongeldige input. Scan eerst (PIM, RISPR, RISPE).\n")

    log_output.see(tk.END)
    input_entry.delete(0, tk.END)

def open_log_file():
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                content = f.read()
                log_output.insert(tk.END, " V Logbestand:\n")
                log_output.insert(tk.END, content)
                log_output.see(tk.END)
        except Exception as e:
            messagebox.showerror("Fout", f"Kon logbestand niet openen:\n{e}")
    else:
        messagebox.showerror("Fout", f"Het logbestand {log_file} bestaat niet.")

# GUI Setup
root = tk.Tk()
root.title("Script Starter")
root.geometry("600x400")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="Scan module- en serienummer:")
label.pack(pady=5)

input_entry = ttk.Entry(frame)
input_entry.pack(fill=tk.X, pady=5)
input_entry.focus()
input_entry.bind("<KeyRelease>", on_user_input)

open_log_button = ttk.Button(frame, text="Open Logbestand", command=open_log_file)
open_log_button.pack(pady=5)

active_option_label = ttk.Label(frame, text="Actieve optie: Geen", font=("Helvetica", 10, "bold"))
active_option_label.pack(pady=5)

log_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
log_output.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()

