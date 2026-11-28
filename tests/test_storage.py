import unittest
import tempfile
import pickle
from pathlib import Path
from unittest.mock import patch

from models import AddressBook, Record, NoteBook
from storage import save_data, load_data


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.data_dir = Path(self.temp_dir.name) / ".nova4lab"
        self.data_file = self.data_dir / "data.pkl"

        dir_patch = patch("storage.DATA_DIR", self.data_dir)
        file_patch = patch("storage.DATA_FILE", self.data_file)

        dir_patch.start()
        file_patch.start()

        self.addCleanup(dir_patch.stop)
        self.addCleanup(file_patch.stop)

        self.book = AddressBook()
        self.notebook = NoteBook()

    def test_load_missing_file(self):
        book, notebook = load_data()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(notebook.notes), 0)

    def test_save_data(self):
        save_data(self.book, self.notebook)
        self.assertTrue(self.data_file.exists())

    def test_save_and_load_contact(self):
        record = Record("John Smith")
        record.add_phone("7045550199")
        self.book.add_record(record)

        save_data(self.book, self.notebook)
        book, notebook = load_data()

        self.assertEqual(
            book.find("John Smith").phones[0].value,
            "7045550199"
        )

    def test_save_and_load_note(self):
        self.notebook.add("Buy groceries")

        save_data(self.book, self.notebook)
        book, notebook = load_data()

        self.assertEqual(
            notebook.get("1").text, "Buy groceries"
        )

    def test_save_and_load_tags(self):
        note = self.notebook.add("Buy groceries")
        note.add_tag("shopping")

        save_data(self.book, self.notebook)
        book, notebook = load_data()

        self.assertIn("shopping", notebook.get("1").tags)

    def test_save_and_load_pinned_note(self):
        note = self.notebook.add("Call John")
        note.pinned = True

        save_data(self.book, self.notebook)
        book, notebook = load_data()

        self.assertTrue(notebook.get("1").pinned)

    def test_save_and_load_favorite_contact(self):
        record = Record("John Smith")
        record.favorite = True
        self.book.add_record(record)

        save_data(self.book, self.notebook)
        book, notebook = load_data()

        self.assertTrue(book.find("John Smith").favorite)

    def test_invalid_saved_data(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        with open(self.data_file, "wb") as file:
            pickle.dump("Invalid data", file)

        with self.assertRaises(ValueError):
            load_data()


if __name__ == "__main__":
    unittest.main()
