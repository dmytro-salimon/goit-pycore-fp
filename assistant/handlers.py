from .models import Record, AddressBook, NotesBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"❌ Помилка вводу: {e}"
        except KeyError as e:
            # Виносимо обробку тексту помилки за межі f-рядка
            item_name = str(e).strip("'")
            return f"❓ Не знайдено: {item_name}"
        except IndexError:
            return "⚠️ Недостатньо аргументів для команди. Використовуйте 'help' для довідки."
        except Exception as e:
            return f"🔥 Сталася непередбачена помилка: {e}"
    return inner

@input_error
def show_help():
    commands = {
        "hello": "привітання з ботом",
        "add <ім'я> <телефон>": "додати новий контакт або телефон",
        "change <ім'я> <старий_тел> <новий_тел>": "змінити існуючий номер",
        "phone <ім'я>": "показати номери телефону",
        "all": "показати всі контакти",
        "add-birthday <ім'я> <DD.MM.YYYY>": "додати день народження",
        "show-birthday <ім'я>": "показати день народження",
        "birthdays <днів>": "іменинники на найближчі дні",
        "delete <ім'я>": "видалити контакт",
        "search <запит>": "пошук контактів за іменем або телефоном",
        "add-note <текст> [#теги]": "створити нотатку",
        "notes": "показати всі нотатки",
        "search-note <текст>": "пошук нотаток за змістом",
        "search-tag <тег>": "пошук за тегами",
        "edit-note <ID> <новий_текст>": "редагувати текст нотатки",
        "delete-note <ID>": "видалити нотатку",
        "close / exit": "завершити роботу"
    }
    help_text = "\n📋 Доступні команди:\n"
    for cmd, desc in commands.items():
        help_text += f"  🔹 {cmd:<35} - {desc}\n"
    return help_text

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та номер телефону.")
    name, phone, *rest = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        res = "✅ Контакт створено."
    else:
        res = "✅ Номер додано до існуючого контакту."
    record.add_phone(phone)
    return res

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Вкажіть ім'я, старий та новий номери.")
    name, old_p, new_p = args[:3]
    record = book.find(name)
    if not record:
        raise KeyError(f"Контакт '{name}' не знайдено.")
    record.edit_phone(old_p, new_p)
    return f"✅ Номер для {name} оновлено."

@input_error
def show_phone(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(name)
    phones = ", ".join(p.value for p in record.phones)
    return f"📞 Телефони {name}: {phones}"

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та дату (DD.MM.YYYY).")
    name, bday = args[:2]
    record = book.find(name)
    if not record:
        raise KeyError(name)
    record.add_birthday(bday)
    return f"🎂 День народження для {name} додано."

@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(name)
    if not record.birthday:
        return f"No birthday set for {name}."
    return f"{name}'s birthday is {record.birthday}"

@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"📭 У найближчі {days} днів іменинників немає."
    res = f"🎉 Іменинники (наступні {days} днів):\n"
    rows = [f"  🎈 {i['name']}: {i['date']}" for i in upcoming]
    return res + "\n".join(rows)

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "📭 Книга контактів порожня."
    res = "📇 Список контактів:\n"
    rows = [str(r) for r in book.data.values()]
    return res + "\n".join(rows)

@input_error
def delete_contact(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0]
    if name not in book.data:
        raise KeyError(name)
    book.delete(name)
    return f"🗑️ Контакт '{name}' видалено."

@input_error
def search_contacts(args, book: AddressBook):
    if not args:
        raise IndexError
    query = args[0]
    results = book.search(query)
    if not results:
        return f"🔍 За запитом '{query}' нічого не знайдено."
    res = "🔎 Результати пошуку:\n"
    rows = [str(r) for r in results]
    return res + "\n".join(rows)

@input_error
def add_note(args, notes: NotesBook):
    if not args:
        raise ValueError("Введіть текст нотатки.")
    tags = [a[1:] for a in args if a.startswith("#")]
    text = " ".join([a for a in args if not a.startswith("#")])
    note_id = notes.add_note(text, tags)
    return f"✅ Нотатку додано (ID: {note_id})."

@input_error
def show_all_notes(args, notes: NotesBook):
    if not notes.data:
        return "📭 Список нотаток порожній."
    res = "🗒️ Ваші нотатки:\n"
    rows = [f"  [{n_id}] {str(note)}" for n_id, note in notes.data.items()]
    return res + "\n".join(rows)

@input_error
def search_notes(args, notes: NotesBook):
    if not args:
        raise IndexError
    query = args[0]
    results = notes.find_notes_by_text(query)
    if not results:
        return "🔍 Нотаток не знайдено."
    res = "🔎 Знайдені нотатки:\n"
    rows = [f"  [{n_id}] {str(note)}" for n_id, note in results.items()]
    return res + "\n".join(rows)

@input_error
def search_by_tag(args, notes: NotesBook):
    if not args:
        raise IndexError
    tag = args[0].lstrip("#")
    results = notes.find_notes_by_tag(tag)
    if not results:
        return f"🔍 Нотаток з тегом #{tag} не знайдено."
    res = f"🔎 Нотатки з тегом #{tag}:\n"
    rows = [f"  [{n_id}] {str(note)}" for n_id, note in results.items()]
    return res + "\n".join(rows)

@input_error
def delete_note(args, notes: NotesBook):
    if not args:
        raise IndexError
    notes.delete_note(args[0])
    return f"🗑️ Нотатку {args[0]} видалено."

@input_error
def edit_note(args, notes: NotesBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ID нотатки та новий текст.")
    note_id, *text = args
    notes.edit_note(note_id, " ".join(text))
    return f"✅ Нотатку {note_id} оновлено."