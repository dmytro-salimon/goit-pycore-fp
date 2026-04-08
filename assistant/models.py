import re
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Номер телефону має складатися рівно з 10 цифр.")
        super().__init__(value)

class Email(Field):
    def __init__(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Некоректний формат email.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте DD.MM.YYYY.")
            
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Address(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Старий номер телефону не знайдено.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones) if self.phones else "відсутні"
        email = f" | Email: {self.email}" if self.email else ""
        bday = f" | День народження: {self.birthday}" if self.birthday else ""
        addr = f" | Адреса: {self.address}" if self.address else ""
        return f"👤 {self.name.value:<15} | Тел: {phones:<15}{email}{bday}{addr}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days):
        upcoming = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                days_until = (bday_this_year - today).days
                if 0 <= days_until <= days:
                    upcoming.append({"name": record.name.value, "date": bday_this_year.strftime("%d.%m.%Y")})
        return upcoming

    def search(self, query):
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
                continue
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break
        return results

class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        tags_str = f" [Теги: {', '.join(self.tags)}]" if self.tags else ""
        return f"📜 {self.text}{tags_str}"

class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        self.note_id = 1

    def add_note(self, text, tags=None):
        while self.note_id in self.data:
            self.note_id += 1
        self.data[self.note_id] = Note(text, tags)
        return self.note_id

    def find_notes_by_text(self, keyword):
        return {id: n for id, n in self.data.items() if keyword.lower() in n.text.lower()}

    def find_notes_by_tag(self, tag):
        return {id: n for id, n in self.data.items() if tag.lower() in [t.lower() for t in n.tags]}

    def delete_note(self, note_id):
        if int(note_id) in self.data:
            del self.data[int(note_id)]
        else:
            raise KeyError("Нотатку з таким ID не знайдено.")

    def edit_note(self, note_id, new_text):
        if int(note_id) in self.data:
            self.data[int(note_id)].text = new_text
        else:
            raise KeyError("Нотатку з таким ID не знайдено.")