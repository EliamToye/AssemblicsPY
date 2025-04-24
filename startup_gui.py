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

def run_script(option, serienummer=None, repeat=1):
    global option_count

    for _ in range(repeat):
        option_count += 1

        if option_count % 1 == 0:
            log_output.insert(tk.END, f"📢 Terminal gewist na {option_count} keuzes.\n")
            log_output.delete('1.0', tk.END)

        if option in scripts:
            try:
                log_output.insert(tk.END, f"🚀 Script {scripts[option]} wordt uitgevoerd met serienummer '{serienummer}'...\n")
                log_output.see(tk.END)
                log_output.update_idletasks()

                args = [sys.executable, scripts[option]]
                if serienummer:
                    args.append(serienummer)

                process = subprocess.Popen(
                    args,
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

def on_user_input(event=None):
    global scheduled_task

    # Annuleer de geplande taak als er een nieuwe toets wordt ingedrukt
    if scheduled_task:
        root.after_cancel(scheduled_task)

    # Start de geplande taak na de vertraging
    scheduled_task = root.after(delay_time, process_input)

def process_input():
    global last_option

    user_input = input_entry.get().strip()

    if not user_input:
        return

    if user_input.lower() == "exit":
        root.quit()
        return

    input_upper = user_input.upper()

    # Eerste keuze: PIM of RIS
    if input_upper in ["PIM", "RIS"]:
        last_option = "1" if input_upper == "PIM" else "2"

        # Clear log en toon geselecteerde optie
        log_output.delete('1.0', tk.END)
        log_output.insert(tk.END, f"✅ Optie '{input_upper}' gekozen. Wacht op serienummer...\n")
        log_output.see(tk.END)

        # Update label
        active_option_label.config(text=f"Actieve optie: {input_upper}")
    
    # Tweede input: Serienummer
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
                log_output.insert(tk.END, "?? Inhoud van logbestand:\n")
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

# Bind de <KeyRelease> event aan de on_user_input functie
input_entry.bind("<KeyRelease>", on_user_input)

# Knoppen
open_log_button = ttk.Button(frame, text="Open Logbestand", command=open_log_file)
open_log_button.pack(pady=5)

# Label om actieve optie te tonen
active_option_label = ttk.Label(frame, text="Actieve optie: Geen", font=("Helvetica", 10, "bold"))
active_option_label.pack(pady=5)

log_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
log_output.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()