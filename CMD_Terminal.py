import os
import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import queue

# ================================
# COMMAND REGISTRY
# ================================
class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator

    def execute(self, cmd, args):
        if cmd in self.commands:
            return self.commands[cmd](args)
        return f"Command not found: {cmd}"


registry = CommandRegistry()

# ================================
# BACKEND ENGINE
# ================================
class TerminalEngine:
    def __init__(self):
        self.history_file = "history.json"
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def execute(self, command):
        parts = command.strip().split()
        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        self.history.append(command)
        self.save_history()

        return registry.execute(cmd, args)


engine = TerminalEngine()

# ================================
# COMMANDS
# ================================
@registry.register("pwd")
def cmd_pwd(args):
    return os.getcwd()

@registry.register("ls")
def cmd_ls(args):
    try:
        return "\n".join(os.listdir())
    except Exception as e:
        return f"Error: {e}"

@registry.register("cd")
def cmd_cd(args):
    if not args:
        return "Usage: cd <directory>"
    try:
        os.chdir(args[0])
        return ""
    except Exception as e:
        return f"Error: {e}"

@registry.register("mkdir")
def cmd_mkdir(args):
    if not args:
        return "Usage: mkdir <folder>"
    try:
        os.mkdir(args[0])
        return "Folder created"
    except Exception as e:
        return f"Error: {e}"

@registry.register("touch")
def cmd_touch(args):
    if not args:
        return "Usage: touch <file>"
    try:
        open(args[0], "a").close()
        return "File created"
    except Exception as e:
        return f"Error: {e}"

@registry.register("cat")
def cmd_cat(args):
    if not args:
        return "Usage: cat <file>"
    try:
        with open(args[0], "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@registry.register("clear")
def cmd_clear(args):
    return "__CLEAR__"

@registry.register("exit")
def cmd_exit(args):
    return "__EXIT__"

@registry.register("help")
def cmd_help(args):
    return """Available commands:
pwd, ls, cd, mkdir, touch, cat
clear, exit, help"""

# ================================
# GUI
# ================================
root = tk.Tk()
root.title("Mini Terminal")
root.geometry("1000x600")

icon = tk.PhotoImage(file="logo.png")
root.iconphoto(True, icon)

terminal = ScrolledText(
    root,
    font=("Consolas", 11),
    bg="#0D0D0D",
    fg="#E0E0E0",
    insertbackground="white"
)
terminal.pack(fill="both", expand=True)

history_index = len(engine.history)

# ================================
# THREAD-SAFE QUEUE
# ================================
output_queue = queue.Queue()

# ================================
# PROMPT
# ================================
def show_prompt():
    terminal.insert(tk.END, f"\n{os.getcwd()} $ ")
    terminal.mark_set("insert", tk.END)

# ================================
# WORKER THREAD
# ================================
def run_command(command):
    output = engine.execute(command)
    output_queue.put(output)

# ================================
# QUEUE PROCESSOR (MAIN THREAD)
# ================================
def process_queue():
    try:
        while True:
            output = output_queue.get_nowait()

            if output == "__CLEAR__":
                terminal.delete("1.0", tk.END)

            elif output == "__EXIT__":
                root.destroy()
                return

            elif output:
                terminal.insert(tk.END, output + "\n")

            show_prompt()

    except queue.Empty:
        pass

    root.after(100, process_queue)

# ================================
# INPUT HANDLING
# ================================
def handle_enter(event):
    input_line = terminal.get("insert linestart", "end-1c")
    command = input_line.split("$")[-1].strip()

    terminal.insert(tk.END, "\n")

    threading.Thread(target=run_command, args=(command,), daemon=True).start()

    return "break"

# ================================
# HISTORY NAVIGATION
# ================================
def navigate_history(direction):
    global history_index

    if not engine.history:
        return

    if direction == "up":
        history_index = max(0, history_index - 1)
    else:
        history_index = min(len(engine.history) - 1, history_index + 1)

    replace_line(engine.history[history_index])

def replace_line(text):
    terminal.delete("insert linestart", "insert")
    terminal.insert("insert", f"{os.getcwd()} $ {text}")

# ================================
# PROTECT PROMPT
# ================================
def protect_text(event):
    if terminal.compare("insert", "<", "end-1c linestart"):
        return "break"

# ================================
# BINDINGS
# ================================
terminal.bind("<Return>", handle_enter)
terminal.bind("<Key>", protect_text)
terminal.bind("<Up>", lambda e: [navigate_history("up"), "break"][1])
terminal.bind("<Down>", lambda e: [navigate_history("down"), "break"][1])

# ================================
# START
# ================================
terminal.insert(tk.END, "Mini Terminal\nType 'help'\n")
show_prompt()

process_queue()  # IMPORTANT: start queue loop

root.mainloop()
