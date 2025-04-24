import subprocess
import sys
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

option_count = 0

scripts = {
    "1": "test1.py",
    "2": "test2.py",
    "help": "testhelp.py",
    "log": "log.py"
}

log_file = "test_log.txt"  # Pad naar het logbestand
delay_time = 5000  # 5 seconden in milliseconden

# Houd de geplande taak bij
scheduled_task = None

def run_script(option, repeat=1):
    global option_count

    for _ in range(repeat):
        option_count += 1

        if option_count % 1 == 0:
            log_output.insert(tk.END, f"?? Terminal gewist na {option_count} keuzes.\n")
            log_output.delete('1.0', tk.END)

        if option in scripts:
            try:
                log_output.insert(tk.END, f"?? Script {scripts[option]} wordt uitgevoerd...\n")
                log_output.see(tk.END)
                log_output.update_idletasks()  # forceer update

                process = subprocess.Popen(
                    [sys.executable, scripts[option]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )

                # Lees output regel per regel en toon onmiddellijk
                for line in process.stdout:
                    log_output.insert(tk.END, line)
                    log_output.see(tk.END)  # scroll automatisch naar onder
                    log_output.update_idletasks()  # forceer update

                process.wait()

                if process.returncode == 0:
                    log_output.insert(tk.END, f"? {scripts[option]} voltooid.\n\n")
                else:
                    log_output.insert(tk.END, f"?? {scripts[option]} beëindigd met foutcode {process.returncode}.\n\n")

            except Exception as e:
                log_output.insert(tk.END, f"?? Onverwachte fout: {e}\n")
        else:
            log_output.insert(tk.END, "? Ongeldige optie, probeer opnieuw.\n")
            break

def on_user_input(event=None):
    global scheduled_task

    # Annuleer de geplande taak als er een nieuwe toets wordt ingedrukt
    if scheduled_task:
        root.after_cancel(scheduled_task)

    # Start de geplande taak na de vertraging
    scheduled_task = root.after(delay_time, process_input)

def process_input():
    user_input = input_entry.get().strip().lower()
    if not user_input:
        return  # Als het invoerveld leeg is, gebeurt er verder niets

    if user_input == "exit":
        root.quit()
        return

    match = re.match(r"([a-zA-Z0-9]+)\*(\d+)", user_input)
    if match:
        option, repeat = match.groups()
        run_script(option, int(repeat))
    else:
        run_script(user_input)

    # Maak het invoerveld leeg na het uitvoeren van het script
    input_entry.delete(0, tk.END)

def clear_log():
    log_output.delete('1.0', tk.END)

def open_log_file():
    if os.path.exists(log_file):
        # Open het logbestand in de standaard teksteditor
        os.system(f'start {log_file}')  # Voor Windows
    else:
        messagebox.showerror("Fout", f"Het logbestand {log_file} bestaat niet.")

# GUI Setup
root = tk.Tk()
root.title("Script Starter")
root.geometry("600x400")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="Voer een optie in (1 of 2):")
label.pack(pady=5)

input_entry = ttk.Entry(frame)
input_entry.pack(fill=tk.X, pady=5)
input_entry.focus()

# Bind de <KeyRelease> event aan de on_user_input functie
input_entry.bind("<KeyRelease>", on_user_input)

# Knoppen
open_log_button = ttk.Button(frame, text="Open Logbestand", command=open_log_file)
open_log_button.pack(pady=5)

log_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
log_output.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()