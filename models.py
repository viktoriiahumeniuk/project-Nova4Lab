import re
from collections import UserDict
from datetime import date, datetime, timedelta

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
        pattern = (
            rf"{local_part}(?:\.{local_part})*@"
            rf"{domain_label}(?:\.{domain_label})+"
        )
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
        """Restore a saved note and supply tags for older records."""
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
            note for note in self.list_notes() if query in note.text.casefold()
        ]

    def search_by_tag(self, tag):
        tag = normalize_note_tag(tag)
        return [note for note in self.list_notes() if tag in note.tags]

    def sort_by_tags(self):
        """Sort by the first tag alphabetically, with untagged notes last."""
        return sorted(
            self.notes.values(),
            key=lambda note: (
                not note.tags,
                min(note.tags, default=""),
                note.id,
            ),
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
        """Restore a saved contact with defaults for older records."""
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
        birthday = (
            str(self.birthday) if self.birthday is not None else "Not set"
        )
        address = str(self.address) if self.address is not None else "Not set"
        email = str(self.email) if self.email is not None else "Not set"
        marker = "[Favorite] " if self.favorite else ""
        return (
            f"{marker}Contact name: {self.name}, phones: {phones}, "
            f"address: {address}, email: {email}, birthday: {birthday}"
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
        """Update the contact name and its dictionary key."""
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
        """Find matches by part of a name or by an exact phone or email."""
        query = query.strip().lower()
        results = []

        if not query:
            return results

        for record in self.data.values():
            name_match = query in record.name.value.lower()
            phone_match = any(query == phone.value for phone in record.phones)
            email_match = (
                record.email is not None
                and query == record.email.value.lower()
            )

            if name_match or phone_match or email_match:
                results.append(record)

        return results

    def get_upcoming_birthdays(self, days=None):
        """Find birthdays on a date or in the default seven-day window.

        Use the actual birthday for matching. Move weekend reminders
        to Monday and include both dates in the result.
        """
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
                (congratulation_date, record.name.value, next_birthday)
            )

        upcoming_birthdays.sort()

        return [
            {
                "name": name,
                "congratulation_date": congratulation_date.strftime(
                    "%Y.%m.%d"
                ),
                "birthday_date": next_birthday.strftime("%Y.%m.%d"),
            }
            for congratulation_date, name, next_birthday in upcoming_birthdays
        ]
