import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext

# -------------------------------
# Git helper function
# -------------------------------
def push_to_git(message="Update notes"):
    try:
        subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories", "--no-rebase"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("Git operation failed. Make sure your repo is set up and you are connected to the internet.")

# -------------------------------
# Note functions
# -------------------------------
def create_note():
    name = simpledialog.askstring("Add Note", "Enter note name:") + ".txt"
    tag = simpledialog.askstring("Add Note", "Enter a tag for this note:")
    content = ""
    with open(name, "w") as f:
        f.write(f"Tag: {tag}\n{content}")
    messagebox.showinfo("Success", f"{name} created with tag '{tag}'!")
    push_to_git(f"Added note {name}")

def open_note_editor():
    name = filedialog.askopenfilename(title="Select note", filetypes=[("Text Files", "*.txt")])
    if not name:
        return
    editor_window = tk.Toplevel()
    editor_window.title(f"Editing {os.path.basename(name)}")
    editor_window.geometry("500x400")

    text_area = scrolledtext.ScrolledText(editor_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill='both')

    # Load current content
    with open(name, "r") as f:
        text_area.insert(tk.END, f.read())

    def save_changes():
        with open(name, "w") as f:
            f.write(text_area.get("1.0", tk.END).rstrip())
        messagebox.showinfo("Saved", f"{os.path.basename(name)} saved!")
        push_to_git(f"Edited note {os.path.basename(name)}")

    tk.Button(editor_window, text="Save", command=save_changes).pack(pady=5)

def delete_note():
    name = filedialog.askopenfilename(title="Select note to delete", filetypes=[("Text Files", "*.txt")])
    if not name:
        return
    if messagebox.askyesno("Delete", f"Are you sure you want to delete {os.path.basename(name)}?"):
        os.remove(name)
        messagebox.showinfo("Deleted", f"{os.path.basename(name)} deleted!")
        push_to_git(f"Deleted note {os.path.basename(name)}")

def search_notes():
    tag = simpledialog.askstring("Search Notes", "Enter tag to search for:")
    results = []
    for file in os.listdir():
        if file.endswith(".txt"):
            with open(file, "r") as f:
                first_line = f.readline().strip()
                if f"Tag: {tag}" in first_line:
                    results.append(file)
    if results:
        messagebox.showinfo("Search Results", "\n".join(results))
    else:
        messagebox.showinfo("Search Results", "No notes found with that tag.")

# -------------------------------
# GUI function
# -------------------------------
def launch_gui():
    root = tk.Tk()
    root.title("Notes App")
    root.geometry("400x400")

    tk.Label(root, text="Welcome to Notes App", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Create New Note", width=25, command=create_note).pack(pady=5)
    tk.Button(root, text="Open & Edit Note", width=25, command=open_note_editor).pack(pady=5)
    tk.Button(root, text="Delete Note", width=25, command=delete_note).pack(pady=5)
    tk.Button(root, text="Search Notes by Tag", width=25, command=search_notes).pack(pady=5)
    tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

# -------------------------------
# Launch GUI
# -------------------------------
if __name__ == "__main__":
    launch_gui()

