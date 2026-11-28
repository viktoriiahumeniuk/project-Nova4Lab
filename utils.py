import re
from difflib import get_close_matches
from functools import wraps


def input_error(func):
    """Turn a command's validation error into a message for the user."""

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
        raise ValueError(
            f"Separate the fields with commas.\nExample: {example}"
        )
    raise ValueError(f"Usage: {usage}")


def get_record(book, name):
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' was not found.")
    return record


def remove_note_quotes(text):
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text


def parse_input(user_input):
    """Split a CLI command into its name and arguments.

    Keep spaces inside names and notes. Split addresses only at
    the first comma so the rest of the address stays intact.
    """
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
            remove_note_quotes(address.strip()),
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
