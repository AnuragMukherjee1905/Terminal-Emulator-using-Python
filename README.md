# Mini Terminal Emulator

A GUI-based terminal emulator built using Python and Tkinter that replicates core shell functionality such as command execution, directory navigation, file management, command history, and asynchronous processing using threading and queues.

This project was developed as a learning-focused implementation of:

* GUI programming
* event-driven architecture
* multi-threading
* command parsing
* filesystem interaction
* scalable command registration systems

# Features

* Interactive terminal-style GUI
* Custom command execution system
* Dynamic command registration using decorators
* Directory navigation support
* File and folder management
* Persistent command history
* Arrow key history navigation
* Threaded command execution
* Thread-safe queue communication
* Protected terminal editing
* Scrollable terminal interface
* Custom application icon
* Real-time prompt rendering

# Tech Stack

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Core programming language      |
| Tkinter    | GUI framework                  |
| Threading  | Non-blocking command execution |
| Queue      | Thread-safe communication      |
| JSON       | Persistent command history     |
| OOP        | Project architecture           |

# Project Structure

```text id="5dujlwm"
project/
│
├── main.py
├── logo.png
├── README.md
└── .gitignore
```

# Supported Commands

| Command        | Description                       |
| -------------- | --------------------------------- |
| `pwd`          | Display current working directory |
| `ls`           | List files and folders            |
| `cd <folder>`  | Change current directory          |
| `mkdir <name>` | Create new folder                 |
| `touch <file>` | Create empty file                 |
| `cat <file>`   | Display file contents             |
| `clear`        | Clear terminal screen             |
| `help`         | Display available commands        |
| `exit`         | Close the application             |

# System Architecture

```text id="cjlwm4"
User Input
    ↓
Tkinter Event Binding
    ↓
Command Extraction
    ↓
Worker Thread Execution
    ↓
Queue-Based Communication
    ↓
Main GUI Thread
    ↓
Terminal Output Rendering
```

# Core Concepts Implemented

## Object-Oriented Programming

The application is structured using modular classes such as:

* `CommandRegistry`
* `TerminalEngine`

This improves:

* scalability
* maintainability
* code organization

## Decorator-Based Command Registration

Commands are dynamically registered using Python decorators.

Example:

```python id="jlwm67"
@registry.register("pwd")
def cmd_pwd(args):
    return os.getcwd()
```

This avoids large `if-elif` chains and enables scalable command addition.

## Multi-Threading

Commands execute in separate worker threads to prevent GUI freezing.

```python id="jlwm68"
threading.Thread(
    target=run_command,
    args=(command,),
    daemon=True
).start()
```

This ensures the interface remains responsive during command execution.

## Thread-Safe Queue Communication

The project uses a queue for safe communication between:

* worker threads
* main GUI thread

```python id="jlwm69"
output_queue.put(output)
```

This follows a producer-consumer architecture commonly used in real-world software systems.

## Persistent Command History

Command history is stored using JSON.

```python id="jlwm70"
json.dump(self.history, f, indent=2)
```

History remains available even after restarting the application.

# GUI Features

* Dark terminal-inspired interface
* Scrollable output window
* Dynamic prompt generation
* Keyboard event handling
* Protected terminal region
* Custom window icon
* Responsive resizing behavior

# Keyboard Shortcuts

| Key            | Action           |
| -------------- | ---------------- |
| `Enter`        | Execute command  |
| `↑ Up Arrow`   | Previous command |
| `↓ Down Arrow` | Next command     |

# Installation & Usage

## Clone Repository

```bash id="jlwm71"
git clone <your-repository-link>
```

## Navigate Into Project Folder

```bash id="jlwm72"
cd <project-folder>
```

## Run Application

```bash id="jlwm73"
python main.py
```

# Key Learning Outcomes

This project strengthened understanding of:

* GUI application development
* event-driven programming
* threading and concurrency
* asynchronous communication
* decorators
* filesystem operations
* command parsing
* Tkinter event handling
* scalable software architecture

# Why This Project Matters

This project demonstrates practical understanding of:

* backend + frontend integration
* responsive GUI design
* concurrency handling
* modular architecture
* real-world software design patterns

Compared to basic console applications, this project introduces significantly more advanced programming concepts and architectural thinking.

# License

This project was created for educational and learning purposes.
