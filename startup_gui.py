import subprocess
import sys
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Onthoud hoeveel opties
option_count = 0
# Onthoud laatste gekozen script
last_option = None  
# Label voor actieve optie
active_option_label = None
# Flag om te zien of een script bezig is
script_is_running = False

scripts = {
    "1": "test1.py",
    "2": "test2.py",
    "help": "testhelp.py",
    "log": "log.py"
}

log_file = "test_log.txt"
delay_time = 5000  # 5 seconden

# Houd de geplande taak bij
scheduled_task = None

def run_script(option, serienummer=None, repeat=1):
    global option_count, script_is_running

    script_is_running = True
    input_entry.config(state='disabled')
    root.update()

    for _ in range(repeat):
        option_count += 1

        log_output.delete('1.0', tk.END)
        log_output.insert(tk.END, f"📢 Uitvoering gestart...\n")

        if option in scripts:
            try:
                log_output.insert(tk.END, f"🚀 Script {scripts[option]} wordt uitgevoerd...\n")

                command = [sys.executable, scripts[option]]
                if serienummer:
                    command.append(serienummer)

                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )

                for line in process.stdout:
                    log_output.insert(tk.END, line)
                    log_output.see(tk.END)
                    log_output.update_idletasks()

                process.wait()

                if process.returncode == 0:
                    log_output.insert(tk.END, f"✅ {scripts[option]} voltooid.\n\n")
                else:
                    log_output.insert(tk.END, f"⚠️ {scripts[option]} beëindigd met foutcode {process.returncode}.\n\n")

            except Exception as e:
                log_output.insert(tk.END, f"⚠️ Onverwachte fout: {e}\n")
        else:
            log_output.insert(tk.END, "❌ Ongeldige optie, probeer opnieuw.\n")
            break

    script_is_running = False
    input_entry.config(state='normal')

    # Na 5 seconden input wissen als extra veiligheid
    root.after(500, lambda: input_entry.delete(0, tk.END))

    input_entry.focus()

def on_user_input(event=None):
    global scheduled_task

    if script_is_running:
        return  # Geen invoer verwerken als een script bezig is

    if scheduled_task:
        root.after_cancel(scheduled_task)

    scheduled_task = root.after(delay_time, process_input)

def process_input():
    global last_option

    if script_is_running:
        return  # Beveiliging, extra controle

    user_input = input_entry.get().strip()

    if not user_input:
        return

    if user_input.lower() == "exit":
        root.quit()
        return

    input_upper = user_input.upper()

    if input_upper in ["PIM", "RIS"]:
        last_option = "1" if input_upper == "PIM" else "2"
        log_output.delete('1.0', tk.END)
        log_output.insert(tk.END, f"✅ Optie '{input_upper}' gekozen. Wacht op serienummer...\n")
        log_output.see(tk.END)
        active_option_label.config(text=f"Actieve optie: {input_upper}")

    elif last_option and re.match(r"^[A-Za-z0-9\-]+$", user_input):
        log_output.insert(tk.END, f"📦 Serienummer ingevoerd: {user_input}\n")
        run_script(last_option, serienummer=user_input)

    else:
        log_output.insert(tk.END, "❌ Ongeldige input. Typ eerst PIM of RIS.\n")

    input_entry.delete(0, tk.END)

def clear_log():
    log_output.delete('1.0', tk.END)

def open_log_file():
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                content = f.read()
                log_output.insert(tk.END, "📂 Inhoud van logbestand:\n")
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

label = ttk.Label(frame, text="Voer in (PIM of RIS) & dan serienummer :")
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