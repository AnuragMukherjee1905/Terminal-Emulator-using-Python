import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# ================================
# GLOBALS
# ================================
history = []
history_index = -1
prompt = "$ "


# ================================
# COMMAND EXECUTION
# ================================
def execute_command(command):
    parts = command.strip().split()

    if not parts:
        return ""

    cmd = parts[0].lower()

    try:
        if cmd == "pwd":
            return os.getcwd()

        elif cmd == "ls":
            return "\n".join(os.listdir()) or "(empty)"

        elif cmd == "cd":
            path = " ".join(parts[1:])
            if not path:
                return "Usage: cd <dir>"
            os.chdir(path)
            return ""

        elif cmd == "mkdir":
            name = " ".join(parts[1:])
            if not name:
                return "Usage: mkdir <folder>"
            os.mkdir(name)
            return "Folder created"

        elif cmd == "touch":
            name = " ".join(parts[1:])
            if not name:
                return "Usage: touch <file>"
            open(name, 'w').close()
            return "File created"

        elif cmd == "rm":
            name = " ".join(parts[1:])
            if not name:
                return "Usage: rm <file>"
            os.remove(name)
            return "File deleted"

        elif cmd == "cat":
            name = " ".join(parts[1:])
            if not name:
                return "Usage: cat <file>"
            with open(name, 'r') as f:
                return f.read() or "(empty file)"

        elif cmd == "echo":
            return " ".join(parts[1:])

        elif cmd == "help":
            return "Commands: pwd, ls, cd, mkdir, touch, rm, cat, echo, clear, exit"

        elif cmd == "clear":
            terminal.delete("1.0", tk.END)
            return ""

        elif cmd == "exit":
            root.destroy()

        else:
            return "Command not found"

    except Exception as e:
        return f"Error: {e}"


# ================================
# SHOW PROMPT
# ================================
def show_prompt():
    terminal.insert(tk.END, prompt)
    terminal.mark_set("insert", tk.END)


# ================================
# GET CURRENT INPUT
# ================================
def get_current_command():
    line = terminal.get("insert linestart", "insert")
    return line.replace(prompt, "")


# ================================
# HANDLE ENTER
# ================================
def handle_enter(event):
    global history_index

    command = get_current_command().strip()

    terminal.insert(tk.END, "\n")

    if command:
        history.append(command)
        history_index = len(history)

        output = execute_command(command)

        if output:
            terminal.insert(tk.END, output + "\n")

    show_prompt()
    return "break"


# ================================
# PREVENT EDITING OLD TEXT
# ================================
def prevent_edit(event):
    if terminal.compare("insert", "<", "end-1c linestart"):
        return "break"


# ================================
# HISTORY NAVIGATION
# ================================
def show_previous_command(event):
    global history_index
    if history:
        history_index = max(0, history_index - 1)
        replace_current_line(history[history_index])
    return "break"

def show_next_command(event):
    global history_index
    if history:
        history_index = min(len(history) - 1, history_index + 1)
        replace_current_line(history[history_index])
    return "break"


def replace_current_line(text):
    terminal.delete("insert linestart", "insert")
    terminal.insert("insert", prompt + text)


# ================================
# GUI SETUP
# ================================
root = tk.Tk()
root.configure(bg="black")

root.title("Mini Terminal")
root.geometry("900x500")

terminal = ScrolledText(
    root,
    font=("Consolas", 12),
    bg="black",
    fg="white",
    insertbackground="white"
)
terminal.pack(fill="both", expand=True)

terminal.bind("<Return>", handle_enter)
terminal.bind("<Key>", prevent_edit)
terminal.bind("<Up>", show_previous_command)
terminal.bind("<Down>", show_next_command)

show_prompt()

root.mainloop()