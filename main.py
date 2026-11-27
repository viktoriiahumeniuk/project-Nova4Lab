import pickle
import re
from pathlib import Path
from collections import UserDict
from datetime import date, datetime, timedelta
from difflib import get_close_matches
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


def normalize_note_tag(tag):
    tag = tag.strip().casefold()
    if not tag or any(char.isspace() for char in tag):
        raise ValueError("A tag must be a single word.")
    return tag


class Note:
    def __init__(self, note_id, text):
        self.id = note_id
        self.pinned = False
        self.tags = set()
        self.edit(text)

    def edit(self, text):
        text = text.strip()
        if not text:
            raise ValueError("Note text cannot be empty.")
        self.text = text

    def add_tag(self, tag):
        self.tags.add(normalize_note_tag(tag))

    def __setstate__(self, state):
        # Notes saved before tags were introduced have no "tags" field.
        self.__dict__.update(state)
        self.__dict__.setdefault("tags", set())

    def __str__(self):
        marker = "[Pinned] " if self.pinned else ""
        tags = ", ".join(sorted(self.tags))
        suffix = f" [Tags: {tags}]" if tags else ""
        return f"{marker}#{self.id} {self.text}{suffix}"


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

    def list_notes(self):
        return sorted(self.notes.values(), key=lambda note: not note.pinned)

    def search(self, query):
        query = query.strip().casefold()
        if not query:
            raise ValueError("Search text cannot be empty.")
        return [
            note for note in self.list_notes()
            if query in note.text.casefold()
        ]

    def search_by_tag(self, tag):
        tag = normalize_note_tag(tag)
        return [note for note in self.list_notes() if tag in note.tags]

    def sort_by_tags(self):
        return sorted(
            self.notes.values(),
            key=lambda note: (not note.tags, min(note.tags, default=""), note.id),
        )

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
        self.favorite = False

    def __setstate__(self, state):
        # Older address books may lack these fields.
        self.favorite = False
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
        if phone is None:
            return False
        self.phones.remove(phone)
        return True

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
        marker = "[Favorite] " if self.favorite else ""
        return (
            f"{marker}Contact name: {self.name}, phones: {phones}, address: {address}, "
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
            phone_match = any(
                query == phone.value for phone in record.phones
            )
            email_match = (
                record.email is not None
                and query == record.email.value.lower()
            )

            if name_match or phone_match or email_match:
                results.append(record)

        return results    

    def get_upcoming_birthdays(self, days=None):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_date = record.birthday.value

            if days is None:
                next_birthday = birthday_in_year(birthday_date, today.year)

                if next_birthday < today:
                    next_birthday = birthday_in_year(
                        birthday_date, today.year + 1
                    )

                days_until_birthday = (next_birthday - today).days

                if not 0 <= days_until_birthday <= 7:
                    continue

            else:
                target_date = today + timedelta(days=days)
                next_birthday = birthday_in_year(
                    birthday_date, target_date.year
                )

                if next_birthday != target_date:
                    continue

            congratulation_date = next_birthday

            if next_birthday.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif next_birthday.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                (congratulation_date, record.name.value)
            )

        upcoming_birthdays.sort()

        return [
            {
                "name": name,
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
            }
            for congratulation_date, name in upcoming_birthdays
        ]


DATA_DIR = Path.home() / ".nova4lab"
DATA_FILE = DATA_DIR / "data.pkl"


def save_data(book, notebook):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "wb") as file:
        pickle.dump((book, notebook), file)


def load_data():
    try:
        with open(DATA_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook(), NoteBook()


def input_error(func):
    @wraps(func)
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as error:
            return str(error)
    return wrapper


def require_args(args, count, usage):
    if len(args) == count and all(arg.strip() for arg in args):
        return

    raise ValueError(f"Usage: {usage}")

    examples = {
        "add-contact": "add-contact Anna Smith, 7045550123",
        "change": "change Anna Smith, 7045550123, 7045550199",
        "remove-phone": "remove-phone Anna Smith, 7045550123",
        "set-email": "set-email Anna Smith, anna@example.com",
        "rename-contact": "rename-contact Anna Smith, Anna Brown",
        "add-birthday": "add-birthday Anna Smith, 26.11.1998",
    }

    command = usage.split(maxsplit=1)[0]
    example = examples.get(command)
    if example:
        raise ValueError(f"Separate the fields with commas.\nExample: {example}")
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
def show_contact(args, book):
    require_args(args, 1, "show-contact [name]")
    return str(get_record(book, args[0]))


@input_error
def remove_phone(args, book):
    require_args(args, 2, "remove-phone [name], [phone]")
    name, phone = args
    record = get_record(book, name)
    if not record.remove_phone(phone):
        raise ValueError(f"Phone number {phone} was not found for {name}.")
    return "Phone number removed."


@input_error
def favorite_contact(args, book):
    require_args(args, 1, "favorite [name]")
    record = get_record(book, args[0])
    record.favorite = True
    return f"{record.name} marked as a favorite."


@input_error
def unfavorite_contact(args, book):
    require_args(args, 1, "unfavorite [name]")
    record = get_record(book, args[0])
    record.favorite = False
    return f"{record.name} removed from favorites."


@input_error
def show_favorites(args, book):
    require_args(args, 0, "favorites")
    favorites = (str(record) for record in book.values() if record.favorite)
    return "\n".join(favorites) or "No favorite contacts."


@input_error
def show_all(args, book):
    require_args(args, 0, "all")
    records = sorted(book.values(), key=lambda record: not record.favorite)
    return "\n".join(str(record) for record in records) or "No contacts."

@input_error
def search_contact(args, book):
    require_args(args, 1, "search-contact [name, phone or email]")
    matches = book.search_contacts(args[0])
    return "\n".join(str(record) for record in matches) or "No matching contacts found."

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
    if len(args) > 1:
        return "Usage: birthdays [days]"

    days = None

    if args:
        if not args[0].isascii() or not args[0].isdecimal():
            return "Number of days must be a non-negative integer."

        try:
            days = int(args[0])
            date.today() + timedelta(days=days)
        except (ValueError, OverflowError):
            return "Number of days is too large."

    try:
        upcoming = book.get_upcoming_birthdays(days)
    except OverflowError:
        return "Number of days is too large."

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


@input_error
def list_notes(args, notebook):
    require_args(args, 0, "list-notes")
    return "\n".join(str(note) for note in notebook.list_notes()) or "No notes yet."


@input_error
def pin_note(args, notebook):
    require_args(args, 1, "pin-note [id]")
    note = notebook.get(args[0])
    note.pinned = True
    return f"Note #{note.id} pinned."


@input_error
def unpin_note(args, notebook):
    require_args(args, 1, "unpin-note [id]")
    note = notebook.get(args[0])
    note.pinned = False
    return f"Note #{note.id} unpinned."


@input_error
def tag_note(args, notebook):
    require_args(args, 2, "add-tag [id] [tag]")
    note = notebook.get(args[0])
    note.add_tag(args[1])
    return f"Tag added to note #{note.id}."


@input_error
def search_note_tag(args, notebook):
    require_args(args, 1, "search-tag [tag]")
    notes = notebook.search_by_tag(args[0])
    return "\n".join(str(note) for note in notes) or "No matching notes."


@input_error
def sort_notes_by_tag(args, notebook):
    require_args(args, 0, "sort-notes-by-tag")
    notes = notebook.sort_by_tags()
    return "\n".join(str(note) for note in notes) or "No notes yet."


def remove_note_quotes(text):
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def parse_input(user_input):
    parts = user_input.split(maxsplit=1)
    if not parts:
        return "", []

    command = parts[0].lower()
    text = parts[1].strip() if len(parts) == 2 else ""

    if text.count('"') % 2 != 0:
        raise ValueError("Invalid input. Check your quotation marks.")

    if not text:
        return command, []

    if command == "set-address":
        name, comma, address = text.partition(",")
        if not comma or not name.strip() or not address.strip():
            raise ValueError(
                "Separate the name and address with a comma. "
                "Example: set-address Anna Smith, 100 Main St"
            )
        return command, [
            remove_note_quotes(name.strip()),
            remove_note_quotes(address.strip())
        ]

    if command in ("edit-note", "add-tag", "tag-note"):
        args = re.split(r"\s*,\s*|\s+", text, maxsplit=1)
        return command, [remove_note_quotes(arg) for arg in args]

    comma_commands = {
        "add-contact": 1,
        "change": 2,
        "remove-phone": 1,
        "set-email": 1,
        "rename-contact": 1,
        "add-birthday": 1,
    }

    if command in comma_commands:
        args = [
            remove_note_quotes(part.strip())
            for part in text.split(",", maxsplit=comma_commands[command])
        ]
        return command, args

    return command, [remove_note_quotes(text)]


def suggest_command(user_input, known_commands):
    """Suggest a command and keep its arguments as entered."""
    words = user_input.strip().split(maxsplit=1)
    if not words:
        return None

    phrase_commands = {
        "find a contact": "search-contact",
        "find a note": "search-note",
        "add a contact": "add-contact",
        "add a note": "add-note",
    }
    phrase = " ".join(user_input.casefold().split())
    if phrase in phrase_commands:
        return phrase_commands[phrase]

    matches = get_close_matches(
        words[0].casefold(), known_commands, n=1, cutoff=0.65
    )
    if not matches:
        return None
    return " ".join([matches[0], *words[1:]])


def show_help():
    print("""
========================================================
                  NOVA4LAB ASSISTANT
========================================================

CONTACT COMMANDS

add-user name
add-contact name, phone
change name, old_phone, new_phone
remove-phone name, phone
phone name
set-address name, address
set-email name, email
rename-contact old_name, new_name
delete-contact name
show-contact name
search-contact query
all
favorite name
unfavorite name
favorites
add-birthday name, DD.MM.YYYY
show-birthday name
birthdays [days]

NOTE COMMANDS

add-note text
list-notes
search-note text
edit-note id, new_text
delete-note id
pin-note id
unpin-note id
add-tag id tag
search-tag tag
sort-notes-by-tag

SYSTEM COMMANDS

hello       - Greeting
help        - Show available commands
exit        - Save data and exit
close       - Save data and exit

Separate arguments with commas where indicated.
Double quotation marks are optional.

========================================================
""")

def main():
    book, notebook = load_data()
    handlers = {
        "add-user": (add_user, book),
        "add-contact": (add_contact, book),
        "change": (change_contact, book),
        "set-address": (set_address, book),
        "set-email": (set_email, book),
        "rename-contact": (rename_contact, book),
        "delete-contact": (delete_contact, book),
        "phone": (show_phone, book),
        "all": (show_all, book),
        "show-contact": (show_contact, book),
        "remove-phone": (remove_phone, book),
        "favorite": (favorite_contact, book),
        "unfavorite": (unfavorite_contact, book),
        "favorites": (show_favorites, book),
        "search-contact": (search_contact, book),
        "add-birthday": (add_birthday, book),
        "show-birthday": (show_birthday, book),
        "birthdays": (birthdays, book),
        "add-note": (add_note, notebook),
        "search-note": (search_note, notebook),
        "edit-note": (edit_note, notebook),
        "delete-note": (delete_note, notebook),
        "list-notes": (list_notes, notebook),
        "pin-note": (pin_note, notebook),
        "unpin-note": (unpin_note, notebook),
        "add-tag": (tag_note, notebook),
        "search-tag": (search_note_tag, notebook),
        "sort-notes-by-tag": (sort_notes_by_tag, notebook),
    }
    known_commands = (*handlers, "hello", "help", "exit", "close")
    handlers["tag-note"] = handlers["add-tag"]
    handlers["search-note-tag"] = handlers["search-tag"]

    print("Welcome to the Nova4Lab assistant bot!")
    show_help()

    while True:
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)
        except ValueError as error:
            print(error)
            continue
        except (EOFError, KeyboardInterrupt):
            save_data(book, notebook)
            print("\nGood bye!")
            break

        if command in ("close", "exit", "hello", "help") and args:
            print(f"Usage: {command}")
            continue

        if command in ("close", "exit"):
            save_data(book, notebook)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            show_help()

        elif command in handlers:
            handler, collection = handlers[command]
            print(handler(args, collection))

        else:
            suggestion = suggest_command(user_input, known_commands)
            if suggestion:
                print(f"Invalid command. Did you mean '{suggestion}'?")
            else:
                print("Invalid command. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
