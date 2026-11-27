import pickle
import re
from collections import UserDict
from datetime import date, datetime, timedelta
from functools import wraps


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Contact name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if (
            not isinstance(value, str)
            or len(value) != 10
            or not value.isascii()
            or not value.isdigit()
        ):
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)

class Email(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Invalid email address.")

        super().__init__(value)

class Address(Field):
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        value = value.strip()
        local_part = r"[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
        domain_label = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
        pattern = rf"{local_part}(?:\.{local_part})*@{domain_label}(?:\.{domain_label})+"
        if not re.fullmatch(pattern, value):
            raise ValueError(
                "Invalid email address. Use a format like anna@example.com."
            )
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            if not isinstance(value, str) or not re.fullmatch(
                r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}", value
            ):
                raise ValueError

            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None

        super().__init__(birthday_date)

    def __str__(self):
        return f"{self.value:%d.%m}.{self.value.year:04d}"

class Note:
    def __init__(self, note_id, text):
        self.id = note_id
        self.edit(text)

    def edit(self, text):
        text = text.strip()
        if not text:
            raise ValueError("Note text cannot be empty.")
        self.text = text

    def __str__(self):
        return f"#{self.id} {self.text}"


class NoteBook:
    def __init__(self):
        self.notes = {}
        self.next_id = 1

    def add(self, text):
        note = Note(self.next_id, text)
        self.notes[note.id] = note
        self.next_id += 1
        return note

    def get(self, note_id):
        if not note_id.isascii() or not note_id.isdecimal():
            raise ValueError("Note ID must be a positive whole number.")

        note_id = int(note_id)
        if note_id <= 0:
            raise ValueError("Note ID must be a positive whole number.")

        note = self.notes.get(note_id)
        if note is None:
            raise ValueError(f"Note #{note_id} was not found.")
        return note

    def search(self, query):
        query = query.strip().casefold()
        if not query:
            raise ValueError("Search text cannot be empty.")

        return [
            note for note in self.notes.values()
            if query in note.text.casefold()
        ]

    def delete(self, note_id):
        note = self.get(note_id)
        del self.notes[note.id]
        return note
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def __setstate__(self, state):
        # Contacts saved by the starter bot lack these optional fields.
        self.address = None
        self.email = None
        self.__dict__.update(state)

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def set_address(self, address):
        self.address = Address(address)

    def set_email(self, email):
        self.email = Email(email)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone is not None:
            self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        old_phone = self.find_phone(old_number)
        if old_phone is None:
            raise ValueError(f"Phone number {old_number} was not found.")

        new_phone = Phone(new_number)
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones) or "No phones"
        birthday = str(self.birthday) if self.birthday is not None else "Not set"
        address = str(self.address) if self.address is not None else "Not set"
        email = str(self.email) if self.email is not None else "Not set"
        return (
            f"Contact name: {self.name}, phones: {phones}, address: {address}, "
            f"email: {email}, birthday: {birthday}"
        )


def birthday_in_year(birthday_date, year):
    try:
        return birthday_date.replace(year=year)
    except ValueError:
        # Use February 28 for leap-day birthdays in non-leap years.
        return date(year, 2, 28)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def rename(self, old_name, new_name):
        record = self.find(old_name)
        if record is None:
            raise ValueError(f"Contact '{old_name}' was not found.")

        updated_name = Name(new_name)
        if updated_name.value == old_name:
            return
        if updated_name.value in self.data:
            raise ValueError(f"Contact '{updated_name}' already exists.")

        del self.data[old_name]
        record.name = updated_name
        self.add_record(record)

    def search_contacts(self, query):
        query = query.strip().lower()
        results = []

    if not query:
        return results

    for record in self.data.values():
        name_match = query in record.name.value.lower()
        phone_match = any(query == phone.value for phone in record.phones)
        email_match = record.email is not None and query == record.email.value.lower()

        if name_match or phone_match or email_match:
            results.append(record)

    return results    

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_date = record.birthday.value
            next_birthday = birthday_in_year(birthday_date, today.year)

            if next_birthday < today:
                next_birthday = birthday_in_year(birthday_date, today.year + 1)

            days_until_birthday = (next_birthday - today).days
            if not 0 <= days_until_birthday <= 7:
                continue

            congratulation_date = next_birthday
            if next_birthday.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif next_birthday.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append((congratulation_date, record.name.value))

        upcoming_birthdays.sort()
        return [
            {
                "name": name,
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
            }
            for congratulation_date, name in upcoming_birthdays
        ]


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    @wraps(func)
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as error:
            return str(error)

    return wrapper


def require_args(args, count, usage):
    if len(args) == count and all(args):
        return

    examples = {
        "add-contact": "add-contact Anna Smith, 7045550123",
        "change": "change Anna Smith, 7045550123, 7045550199",
        "set-email": "set-email Anna Smith, anna@example.com",
        "rename-contact": "rename-contact Anna Smith, Anna Brown",
        "add-birthday": "add-birthday Anna Smith, 26.11.1998",
    }

    command = usage.split(maxsplit=1)[0]
    example = examples.get(command)

    if example:
        raise ValueError(
            f"Separate the fields with commas.\nExample: {example}"
        )

    raise ValueError(f"Usage: {usage}")


def get_record(book, name):
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' was not found.")
    return record

@input_error
def add_user(args, book):
    require_args(args, 1, "add-user [name]")
    name = Name(args[0]).value

    if book.find(name) is not None:
        raise ValueError(f"Contact '{name}' already exists.")

    book.add_record(Record(name))
    return "Contact added."

@input_error
def add_contact(args, book):
    require_args(args, 2, "add-contact [name], [phone]")
    name, phone = args
    name = Name(name).value
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    require_args(args, 3, "change [name], [old phone], [new phone]")
    name, old_phone, new_phone = args
    get_record(book, name).edit_phone(old_phone, new_phone)
    return "Phone number updated."


@input_error
def set_address(args, book):
    require_args(args, 2, "set-address [name], [address]")
    name, address = args
    get_record(book, name).set_address(address)
    return "Address saved."


@input_error
def set_email(args, book):
    require_args(args, 2, "set-email [name], [email]")
    name, email = args
    get_record(book, name).set_email(email)
    return "Email saved."


@input_error
def rename_contact(args, book):
    require_args(args, 2, "rename-contact [old name], [new name]")
    old_name, new_name = args
    book.rename(old_name, new_name)
    return "Contact renamed."


@input_error
def delete_contact(args, book):
    require_args(args, 1, "delete-contact [name]")
    name = args[0]
    get_record(book, name)
    book.delete(name)
    return "Contact deleted."


@input_error
def show_phone(args, book):
    require_args(args, 1, "phone [name]")
    name = args[0]
    record = get_record(book, name)
    phones = "; ".join(phone.value for phone in record.phones)
    return phones or f"No phone numbers for {name}."


@input_error
def show_all(args, book):
    require_args(args, 0, "all")
    return "\n".join(str(record) for record in book.data.values()) or "No contacts."


@input_error
def add_birthday(args, book):
    require_args(args, 2, "add-birthday [name], [DD.MM.YYYY]")
    name, birthday = args
    get_record(book, name).add_birthday(birthday)
    return "Birthday saved."


@input_error
def show_birthday(args, book):
    require_args(args, 1, "show-birthday [name]")
    name = args[0]
    record = get_record(book, name)

    if record.birthday is None:
        return f"No birthday saved for {name}."

    return f"{record.name}: {record.birthday}"


@input_error
def birthdays(args, book):
    require_args(args, 0, "birthdays")
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['congratulation_date']} — {item['name']}"
        for item in upcoming
    )

@input_error
def add_note(args, notebook):
    require_args(args, 1, "add-note [text]")
    note = notebook.add(args[0])
    return f"Note #{note.id} added."


@input_error
def search_note(args, notebook):
    require_args(args, 1, "search-note [text]")
    matches = notebook.search(args[0])
    return "\n".join(str(note) for note in matches) or "No matching notes."


@input_error
def edit_note(args, notebook):
    require_args(args, 2, "edit-note [id], [new text]")
    note_id, text = args
    note = notebook.get(note_id)
    note.edit(text)
    return f"Note #{note.id} updated."


@input_error
def delete_note(args, notebook):
    require_args(args, 1, "delete-note [id]")
    note = notebook.delete(args[0])
    return f"Note #{note.id} deleted."


def remove_note_quotes(text):
    if len(text) >= 2 and text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def parse_input(user_input):
    parts = user_input.split(maxsplit=1)
    if not parts:
        return "", []

    command = parts[0].lower()
    text = parts[1].strip() if len(parts) == 2 else ""

    if command == "set-address":
        name, comma, address = text.partition(",")
        if not comma or not name.strip() or not address.strip():
            raise ValueError(
                "Separate the name and address with a comma. "
                "Example: set-address Anna Smith, 100 Main St"
            )
        return command, [name.strip(), address.strip()]
    
    if command == "edit-note" and text:
        args = re.split(r"\s*,\s*|\s+", text, maxsplit=1)
        if len(args) == 2:
            args[1] = remove_note_quotes(args[1])
        return command, args

    if command in ("add-note", "search-note") and text:
        return command, [remove_note_quotes(text)]

    if not text:
        return command, []

    comma_commands = {
        "add-contact": 1,
        "change": 2,
        "set-email": 1,
        "rename-contact": 1,
        "add-birthday": 1,
    }

    if command in comma_commands:
        args = [
            part.strip()
            for part in text.split(",", maxsplit=comma_commands[command])
        ]
        return command, args

    return command, [text]


def main():
    book = load_data()
    notebook = NoteBook()
    print("Welcome to the assistant bot!")

    while True:
        try:
            command, args = parse_input(input("Enter a command: "))
        except ValueError as error:
            print(error)
            continue

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add-user":
            print(add_user(args, book))    
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "set-address":
            print(set_address(args, book))
        elif command == "set-email":
            print(set_email(args, book))
        elif command == "rename-contact":
            print(rename_contact(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-note":
            print(add_note(args, notebook))
        elif command == "search-note":
            print(search_note(args, notebook))
        elif command == "edit-note":
            print(edit_note(args, notebook))
        elif command == "delete-note":
            print(delete_note(args, notebook))
        elif command:
            print("Invalid command.")


if __name__ == "__main__":
    main()
