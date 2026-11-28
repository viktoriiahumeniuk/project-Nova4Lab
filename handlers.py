from datetime import date, timedelta
from models import Name, Record
from utils import input_error, require_args, get_record


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
    return (
        "\n".join(str(record) for record in matches)
        or "No matching contacts found."
    )


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


def birthday_results(book, days_text=""):
    """Validate the day offset and return results for the CLI and website."""
    if days_text and (not days_text.isascii() or not days_text.isdecimal()):
        raise ValueError("Number of days must be a non-negative integer.")

    try:
        days = int(days_text) if days_text else None
        date.today() + timedelta(days=days or 0)
        return book.get_upcoming_birthdays(days)
    except (ValueError, OverflowError):
        raise ValueError("Number of days is too large.") from None


@input_error
def birthdays(args, book):
    if len(args) > 1:
        return "Usage: birthdays [days]"

    upcoming = birthday_results(book, args[0] if args else "")

    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['congratulation_date']} — {item['name']}" for item in upcoming
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
    return (
        "\n".join(str(note) for note in notebook.list_notes())
        or "No notes yet."
    )


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
