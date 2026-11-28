import pickle
from pathlib import Path
from models import AddressBook, NoteBook


DATA_DIR = Path.home() / ".nova4lab"
DATA_FILE = DATA_DIR / "data.pkl"


def save_data(book, notebook):
    """Save contacts and notes together in the user's home folder."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "wb") as file:
        pickle.dump((book, notebook), file)


def load_data():
    """Load both collections or start empty if the file is missing."""
    try:
        with open(DATA_FILE, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        return AddressBook(), NoteBook()

    if (
        not isinstance(data, tuple)
        or len(data) != 2
        or not isinstance(data[0], AddressBook)
        or not isinstance(data[1], NoteBook)
    ):
        raise ValueError("Expected saved contacts and notes.")

    return data
