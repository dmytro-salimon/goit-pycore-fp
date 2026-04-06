import pickle
from .models import AddressBook, NotesBook

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError, EOFError):
        return AddressBook()

def save_notes(notes, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError, EOFError):
        return NotesBook()