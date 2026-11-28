import pickle

from models import (
    Field,
    Name,
    Phone,
    Address,
    Email,
    Birthday,
    Note,
    NoteBook,
    Record,
    AddressBook,
)

from storage import DATA_FILE, save_data, load_data
from utils import parse_input, suggest_command
from menu import show_help

from handlers import (
    add_user,
    add_contact,
    change_contact,
    set_address,
    set_email,
    rename_contact,
    delete_contact,
    show_phone,
    show_all,
    show_contact,
    remove_phone,
    favorite_contact,
    unfavorite_contact,
    show_favorites,
    search_contact,
    add_birthday,
    show_birthday,
    birthdays,
    add_note,
    search_note,
    edit_note,
    delete_note,
    list_notes,
    pin_note,
    unpin_note,
    tag_note,
    search_note_tag,
    sort_notes_by_tag,
)


def main():
    try:
        book, notebook = load_data()
    except (OSError, EOFError, pickle.UnpicklingError, ValueError) as error:
        print(f"Could not read {DATA_FILE}: {error}")
        return

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
        input_closed = False
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)
        except ValueError as error:
            print(error)
            continue
        except (EOFError, KeyboardInterrupt):
            print()
            command, args = "exit", []
            input_closed = True

        if command in ("close", "exit", "hello", "help") and args:
            print(f"Usage: {command}")
            continue

        if command in ("close", "exit"):
            try:
                save_data(book, notebook)
            except OSError as error:
                print(f"Could not save {DATA_FILE}: {error}")
                if input_closed:
                    break
                continue
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
