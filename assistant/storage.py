import pickle
import os
from .models import AddressBook, NotesBook

def save_data(book, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
    except Exception as e:
        print(f"⚠️ Помилка при збереженні контактів: {e}")

def load_data(filename="addressbook.pkl"):
    if not os.path.exists(filename):
        return AddressBook()
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data if isinstance(data, AddressBook) else AddressBook()
    except (pickle.UnpicklingError, EOFError, AttributeError):
        print(f"❌ Файл {filename} пошкоджено. Створено нову книгу.")
        return AddressBook()
    except Exception as e:
        print(f"⚠️ Непередбачена помилка завантаження {filename}: {e}")
        return AddressBook()

def save_notes(notes, filename="notes.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(notes, f)
    except Exception as e:
        print(f"⚠️ Помилка при збереженні нотаток: {e}")

def load_notes(filename="notes.pkl"):
    if not os.path.exists(filename):
        return NotesBook()
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data if isinstance(data, NotesBook) else NotesBook()
    except (pickle.UnpicklingError, EOFError, AttributeError):
        print(f"❌ Файл {filename} пошкоджено. Створено новий блокнот.")
        return NotesBook()
    except Exception as e:
        print(f"⚠️ Непередбачена помилка завантаження {filename}: {e}")
        return NotesBook()