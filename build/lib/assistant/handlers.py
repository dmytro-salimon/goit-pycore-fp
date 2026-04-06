from .models import Record, AddressBook, NotesBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}" if str(e) else "Error: Invalid input."
        except KeyError as e:
            return f"Error: {e}" if str(e).strip("'") else "Error: Item not found."
        except IndexError:
            return "Error: Incomplete command arguments."
        except Exception as e:
            return f"Error: {e}"
    return inner

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *rest = args
    record = book.find(name)
    message = "Contact updated successfully."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added successfully."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact phone updated successfully."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    return f"{name}'s phones: {', '.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added successfully."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    if not record.birthday:
        return f"No birthday set for {name}."
    return f"{name}'s birthday is {record.birthday}"

@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."
    return "Upcoming birthdays:\n" + "\n".join([f"🎉 {item['name']}: {item['date']}" for item in upcoming])

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "No contacts saved yet."
    return "Address Book:\n" + "\n".join([str(record) for record in book.data.values()])

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    if name not in book.data:
        raise KeyError("Contact not found.")
    book.delete(name)
    return "Contact deleted successfully."

@input_error
def search_contacts(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    query = args[0]
    results = book.search(query)
    if not results:
        return "No contacts found matching the query."
    return "Search results:\n" + "\n".join([str(record) for record in results])

@input_error
def add_note(args, notes: NotesBook):
    if len(args) < 1:
        raise ValueError("Give me note text.")
    
    text_parts = []
    tags = []
    for arg in args:
        if arg.startswith("#"):
            tags.append(arg[1:])
        else:
            text_parts.append(arg)
    
    text = " ".join(text_parts)
    notes.add_note(text, tags)
    return "Note added successfully."

@input_error
def show_all_notes(args, notes: NotesBook):
    if not notes.data:
        return "No notes saved yet."
    return "Notes Book:\n" + "\n".join([f"ID: {note_id} | {str(note)}" for note_id, note in notes.data.items()])

@input_error
def search_notes(args, notes: NotesBook):
    if len(args) < 1:
        raise IndexError
    query = args[0]
    results = notes.find_notes_by_text(query)
    if not results:
        return "No notes found matching the query."
    return "Search results:\n" + "\n".join([str(note) for note in results])
    
@input_error
def search_by_tag(args, notes: NotesBook):
    if len(args) < 1:
        raise IndexError
    tag = args[0].lstrip("#")
    results = notes.find_notes_by_tag(tag)
    if not results:
        return "No notes found with this tag."
    return "Search results:\n" + "\n".join([str(note) for note in results])

@input_error
def delete_note(args, notes: NotesBook):
    if len(args) < 1:
        raise IndexError
    note_id = args[0]
    notes.delete_note(note_id)
    return "Note deleted successfully."

@input_error
def edit_note(args, notes: NotesBook):
    if len(args) < 2:
        raise ValueError("Give me note ID and new text.")
    note_id = args[0]
    new_text = " ".join(args[1:])
    notes.edit_note(note_id, new_text)
    return "Note updated successfully."