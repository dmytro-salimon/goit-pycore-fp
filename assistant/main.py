from .storage import load_data, save_data, load_notes, save_notes
from . import handlers

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = load_data()
    notes = load_notes()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue
            
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            save_notes(notes)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(handlers.add_contact(args, book))
            save_data(book)
        elif command == "change":
            print(handlers.change_contact(args, book))
            save_data(book)
        elif command == "phone":
            print(handlers.show_phone(args, book))
        elif command == "all":
            print(handlers.show_all(args, book))
        elif command == "add-birthday":
            print(handlers.add_birthday(args, book))
            save_data(book)
        elif command == "show-birthday":
            print(handlers.show_birthday(args, book))
        elif command == "birthdays":
            print(handlers.birthdays(args, book))
        elif command == "delete":
            print(handlers.delete_contact(args, book))
            save_data(book)
        elif command == "search":
            print(handlers.search_contacts(args, book))
        elif command == "add-note":
            print(handlers.add_note(args, notes))
            save_notes(notes)
        elif command == "notes":
            print(handlers.show_all_notes(args, notes))
        elif command == "search-note":
            print(handlers.search_notes(args, notes))
        elif command == "search-tag":
            print(handlers.search_by_tag(args, notes))
        elif command == "edit-note":
            print(handlers.edit_note(args, notes))
            save_notes(notes)
        elif command == "delete-note":
            print(handlers.delete_note(args, notes))
            save_notes(notes)
        else:
            print("Error: Invalid command.")

if __name__ == "__main__":
    main()