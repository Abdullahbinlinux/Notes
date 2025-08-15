import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# -------------------------------
# Notes directory
# -------------------------------
notes_dir = os.path.expanduser("~/notes")
os.makedirs(notes_dir, exist_ok=True)

# -------------------------------
# Git helper
# -------------------------------
def push_to_git(message="Update notes"):
    try:
        subprocess.run(
            ["git", "pull", "origin", "main", "--allow-unrelated-histories", "--no-rebase"],
            check=True,
        )
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("Git operation failed. Check your repo or internet.")

# -------------------------------
# Note functions
# -------------------------------
def create_note():
    name = simpledialog.askstring("New Note", "Enter note name:")
    if not name:
        return
    filename = f"{name}.txt"
    tag = simpledialog.askstring("New Note", "Enter a tag for this note:") or ""
    with open(os.path.join(notes_dir, filename), "w", encoding="utf-8") as f:
        f.write(f"[{tag}]\n")
    messagebox.showinfo("Success", f"{filename} created with tag '{tag}'!")
    refresh_note_list()
    load_note(filename)
    push_to_git(f"Added note {filename}")

def delete_note():
    filename = note_listbox.get(tk.ACTIVE) if note_listbox.curselection() else None
    if not filename:
        return
    path = os.path.join(notes_dir, filename)
    if messagebox.askyesno("Delete", f"Delete {filename}?"):
        os.remove(path)
        messagebox.showinfo("Deleted", f"{filename} deleted!")
        push_to_git(f"Deleted note {filename}")
        refresh_note_list()
        clear_editor()

def search_notes():
    tag = simpledialog.askstring("Search Notes", "Enter tag to search for:")
    if not tag:
        return
    results = []
    for file in os.listdir(notes_dir):
        if file.endswith(".txt"):
            with open(os.path.join(notes_dir, file), "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if f"[{tag}]" == first_line:
                    results.append(file)
    if results:
        messagebox.showinfo("Search Results", "\n".join(results))
    else:
        messagebox.showinfo("Search Results", "No notes found with that tag.")

# -------------------------------
# GUI functions
# -------------------------------
def refresh_note_list():
    note_listbox.delete(0, tk.END)
    for file in sorted(os.listdir(notes_dir)):
        if file.endswith(".txt"):
            note_listbox.insert(tk.END, file)

def load_note(filename):
    path = os.path.join(notes_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    tag = ""
    content_lines = lines
    if lines and lines[0].startswith("[") and "]" in lines[0]:
        tag = lines[0].strip("[]\n")
        content_lines = lines[1:]

    tag_entry.delete(0, tk.END)
    tag_entry.insert(0, tag)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "".join(content_lines))

def save_note():
    filename = note_listbox.get(tk.ACTIVE) if note_listbox.curselection() else None
    if not filename:
        messagebox.showwarning("No Note Selected", "Please select a note from the list")
        return
    path = os.path.join(notes_dir, filename)
    new_tag = tag_entry.get().strip()
    new_content = text_area.get("1.0", tk.END).rstrip()
    with open(path, "w", encoding="utf-8") as f:
        if new_tag:
            f.write(f"[{new_tag}]\n")
        f.write(new_content)
    messagebox.showinfo("Saved", f"{filename} saved!")
    push_to_git(f"Edited note {filename}")
    refresh_note_list()

def clear_editor():
    tag_entry.delete(0, tk.END)
    text_area.delete("1.0", tk.END)

def on_note_select(event):
    if note_listbox.curselection():
        filename = note_listbox.get(tk.ACTIVE)
        load_note(filename)

# -------------------------------
# Main window
# -------------------------------
root = tk.Tk()
root.title("Vibrant Notes App")
root.geometry("900x600")
root.configure(bg="#1e1e2f")

# -------------------------------
# Frames
# -------------------------------
left_frame = tk.Frame(root, bg="#292b3e", width=250)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, bg="#1e1e2f")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# -------------------------------
# Sidebar Listbox
# -------------------------------
note_listbox = tk.Listbox(left_frame, font=("Segoe UI", 12), bg="#292b3e", fg="#ffffff",
                          selectbackground="#ff7f50", selectforeground="#000000")
note_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
note_listbox.bind("<<ListboxSelect>>", on_note_select)

refresh_note_list()

# -------------------------------
# Sidebar Buttons
# -------------------------------
btn_params = {"font": ("Segoe UI", 11), "bg": "#ff7f50", "fg": "#ffffff", "activebackground": "#ff9b7f"}

tk.Button(left_frame, text="Create New Note", command=create_note, **btn_params).pack(fill=tk.X, padx=10, pady=5)
tk.Button(left_frame, text="Delete Note", command=delete_note, **btn_params).pack(fill=tk.X, padx=10, pady=5)
tk.Button(left_frame, text="Search Notes", command=search_notes, **btn_params).pack(fill=tk.X, padx=10, pady=5)
tk.Button(left_frame, text="Exit", command=root.destroy, **btn_params).pack(fill=tk.X, padx=10, pady=5)

# -------------------------------
# Editor area
# -------------------------------
editor_label = tk.Label(right_frame, text="Note Editor", font=("Segoe UI", 16), bg="#1e1e2f", fg="#ffffff")
editor_label.pack(pady=10)

tag_frame = tk.Frame(right_frame, bg="#1e1e2f")
tag_frame.pack(fill=tk.X, padx=10)
tk.Label(tag_frame, text="Tag:", font=("Segoe UI", 12), bg="#1e1e2f", fg="#ffffff").pack(side=tk.LEFT)
tag_entry = tk.Entry(tag_frame, font=("Segoe UI", 12))
tag_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Consolas", 12), bg="#2e2e3e", fg="#ffffff")
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Button(right_frame, text="Save Note", font=("Segoe UI", 12), bg="#ff7f50", fg="#ffffff", command=save_note)\
    .pack(pady=5, padx=10, anchor="e")

# -------------------------------
# Launch
# -------------------------------
root.mainloop()
