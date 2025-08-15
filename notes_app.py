import subprocess
import os
def push_to_git(message="Update notes"):
    try:
        # Step 1: Pull remote changes first (merge)
        subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories", "--no-rebase"], check=True)
        
        # Step 2: Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Step 3: Commit changes
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        # Step 4: Push to remote
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("Changes pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("Git operation failed. Make sure your repo is set up and you are connected to the internet.")


def show_notes():
    files = [f for f in os.listdir() if f.endswith(".txt")]
    if not files:
        print("No notes found.")
        return
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            tag = lines[0].strip() if lines else "No tag"
            content = "".join(lines[1:]) if len(lines) > 1 else ""
            print(f"\nNote: {file}\nTag: {tag}\nContent:\n{content}")

def show_notes():
    files = os.listdir()
    notes = [f for f in files if f.endswith(".txt")]
    if notes:
        print("Your notes:")
        for note in notes:
            print("-", note)
    else:
        print("No notes found.")

def add_note():
    name = input("Enter note name: ") + ".txt"
    tag = input("Enter a tag for this note (e.g., Work, Personal): ")
    content = input("Enter note content: ")
    with open(name, "w") as f:
        f.write(f"Tag: {tag}\n{content}")
    print(f"{name} created with tag '{tag}'!")
    push_to_git(f"Added note {name}")

def delete_note():
    name = input("Enter the note name to delete (without .txt): ") + ".txt"
    if os.path.exists(name):
        os.remove(name)
        print(f"{name} deleted!")
        push_to_git(f"Deleted note {name}")
    else:
        print("Note not found.")
def search_notes():
    keyword = input("Enter keyword to search: ").lower()
    files = [f for f in os.listdir() if f.endswith(".txt")]
    found = False
    for file in files:
        with open(file, "r") as f:
            content = f.read().lower()
            if keyword in content:
                print(f"Keyword found in: {file}")
                found = True
    if not found:
        print("No notes contain that keyword.")
def edit_note():
    name = input("Enter the note name to edit (without .txt): ") + ".txt"
    if os.path.exists(name):
        with open(name, "r") as f:
            content = f.read()
        print(f"Current content:\n{content}\n")
        new_content = input("Enter new content: ")
        with open(name, "w") as f:
            f.write(new_content)
        print(f"{name} updated!")
        push_to_git(f"Edited note {name}")
    else:
        print("Note not found.")

def search_by_tag():
    tag_to_search = input("Enter the tag to search for: ")
    files = [f for f in os.listdir() if f.endswith(".txt")]
    found = False
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            tag = lines[0].replace("Tag: ", "").strip() if lines else ""
            if tag.lower() == tag_to_search.lower():
                content = "".join(lines[1:]) if len(lines) > 1 else ""
                print(f"\nNote: {file}\nTag: {tag}\nContent:\n{content}")
                found = True
    if not found:
        print(f"No notes found with tag '{tag_to_search}'.")


def menu():
    while True:
        print("\n1. Show notes\n2. Add note\n3. Delete note\n4. Search notes\n5. Edit note\n6. Search by tag\n7. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            show_notes()
        elif choice == "2":
            add_note()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            search_notes()
        elif choice == "5":
            edit_note()
        elif choice == "6":
            search_by_tag()
        elif choice == "7":
            break
        else:
            print("Invalid option.")
if __name__ == "__main__":
    menu()

