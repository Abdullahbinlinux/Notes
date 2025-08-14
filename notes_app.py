import os

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
    content = input("Enter note content: ")
    with open(name, "w") as f:
        f.write(content)
    print(f"{name} created!") 
def delete_note():
    name = input("Enter the note name to delete (without .txt): ") + ".txt"
    if os.path.exists(name):
        os.remove(name)
        print(f"{name} deleted!")
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

def menu():
    while True:
        print("\n1. Show notes\n2. Add note\n3. Delete note\n4. Search notes\n5. Exit")
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
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
