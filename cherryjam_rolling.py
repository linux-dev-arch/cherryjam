import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
import os,platform,ctypes
if platform.system() =="Windows":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
file_path=""

# Functions
def on_scroll(*args):
    text_widget.yview(*args)
    line_number_label.yview(*args)

def on_text_scroll(*args):
    scrollbar.set(*args)
    line_number_label.yview_moveto(args[0])

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_label.config(state='normal')
    line_number_label.delete('1.0', 'end')
    line_number_label.insert('1.0', line_numbers)
    line_number_label.config(state='disabled')

def get_line_numbers():
    output = ''
    row, col = text_widget.index("end").split('.')
    for i in range(1, int(row)):
        output += str(i) + '\n'
    return output

def on_content_changed(event=None):
    update_line_numbers()

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CherryScript Files", "*.ci")])
    if file_path:
        with open(file_path, "r") as File:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, File.read())
        update_line_numbers()

def save_file():
    global file_path
    if file_path !="":
        with open(file_path, "w") as File:
            File.write(text_widget.get("1.0", tk.END))
    else:
        save_file_as()

def save_file_as():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".ci", filetypes=[("CherryScript Files", "*.ci")])
    with open(file_path, "w") as File:
        File.write(text_widget.get("1.0", tk.END))

def run_file():
    if platform.system()=="Linux":
        os.system("konsole --hold -e python3 cherryscript_rolling.py "+file_path)
    if platform.system()=="Windows":
        os.system('start cmd /k python.exe cherryscript_rolling.py '+file_path)

# Root window
root = tk.Tk()
root.title("CherryJam")
root.geometry("1280x720")
root.configure(bg="#282a36")  # Dracula background
custom_font = tkFont.Font(family="Arial", size=14)

# Button frame
button_frame = tk.Frame(root, bg="#282a36")
button_frame.pack(side=tk.TOP, anchor="nw", padx=5, pady=5)
button_style = {"bg": "#44475a", "fg": "#f8f8f2", "activebackground": "#6272a4", "activeforeground": "#f8f8f2", "bd":0}

open_button = tk.Button(button_frame, text="Open File", command=open_file, **button_style)
open_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save File", command=save_file, **button_style)
save_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save File As", command=save_file_as, **button_style)
save_button.pack(side=tk.LEFT, padx=5)

run_button = tk.Button(button_frame, text="Run File", command=run_file, **button_style)
run_button.pack(side=tk.LEFT, padx=5)

# Text widget with scrollbar and line numbers
text_frame = tk.Frame(root, bg="#282a36")
text_frame.pack(fill=tk.BOTH, expand=True)

# Line number label
line_number_label = tk.Text(text_frame, width=2, padx=5, takefocus=0, border=0,
                            bg="#1e1f29", fg="#6272a4", state='disabled',
                            font=custom_font)
line_number_label.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(text_frame, bg="#44475a", troughcolor="#282a36")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=on_text_scroll,
                      bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2",
                      selectbackground="#44475a", selectforeground="#f8f8f2")
text_widget.config(font=custom_font,fg="#ff5e5e")
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Connect scrollbar to both widgets
scrollbar.config(command=on_scroll)

# Bind events to update line numbers
text_widget.bind('<KeyRelease>', on_content_changed)

# Initialize line numbers
update_line_numbers()

root.mainloop()
