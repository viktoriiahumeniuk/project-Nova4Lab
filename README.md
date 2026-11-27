# Nova Lab Personal Assistant

A Python assistant for managing contacts, birthdays, and notes. It runs in the terminal and has a browser interface. This is the Nova Lab team's final project for Neoversity's Python Programming course.

## Run locally

You need Python 3.10 or later. The CLI uses the Python standard library and does not require additional dependencies.

```bash
git clone https://github.com/viktoriiahumeniuk/project-Nova4Lab.git
cd project-Nova4Lab
```

### Terminal

```bash
python3 main.py
```

On startup, the assistant displays a menu with all available commands. Enter `help` to display the menu again.

Use commas between separate fields where indicated. Full names, addresses, and notes can contain spaces. Double quotation marks are optional.

Enter birthdays as `DD.MM.YYYY` and phone numbers as exactly 10 digits.

Examples:

```text
add-contact Anna Smith, 7045550123
add-contact "Anna Smith", 7045550123
set-address Anna Smith, 100 Main St, Charlotte
set-address "Anna Smith", "100 Main St, Charlotte"
add-note Pick up balloons on Friday
add-note "Pick up balloons on Friday"
```

Invalid input displays an error without stopping the assistant. For a likely typo such as `add-nte`, it suggests the closest command, such as `add-note`.

### Browser

Keep `index.html` and `main.py` in the same folder. Start a local server from that folder:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000).

The **Contacts** tab lets you search, edit, favorite, and delete contacts or remove individual phone numbers.

The **Notes** tab lets you search, edit, pin, and delete notes.

An internet connection is needed to load the Pyodide runtime that runs the Python models in the browser.

## CLI command reference

### Contacts and birthdays

| Command | What it does |
| --- | --- |
| `add-user Anna Smith` | Create a contact with just a name |
| `add-contact Anna Smith, 7045550123` | Create a contact with a phone number or add another number to an existing contact |
| `show-contact Anna Smith` | Show one contact's details |
| `all` | List contacts with favorites first |
| `phone Anna Smith` | Show all phone numbers for one contact |
| `change Anna Smith, 7045550123, 7045550199` | Replace a saved phone number |
| `remove-phone Anna Smith, 7045550199` | Remove one number from a contact |
| `set-address Anna Smith, 100 Main St, Charlotte` | Add or update an address |
| `set-email Anna Smith, anna@example.com` | Add or update an email |
| `rename-contact Anna Smith, Anna Brown` | Rename a contact |
| `delete-contact Anna Brown` | Delete a contact |
| `search-contact Anna` | Search contacts by name, phone number, or email |
| `favorite Anna Smith` | Mark a contact as a favorite |
| `unfavorite Anna Smith` | Remove a contact from favorites |
| `favorites` | List favorite contacts |
| `add-birthday Anna Smith, 26.11.1998` | Add or update a birthday |
| `show-birthday Anna Smith` | Show one contact's birthday |
| `birthdays` | Show birthdays from today through seven days ahead |
| `birthdays 3` | Show birthdays occurring exactly three days from today |

Birthday congratulations that fall on a weekend are moved to the following Monday.

### Notes

| Command | What it does |
| --- | --- |
| `add-note Pick up balloons on Friday` | Create a note and show its ID |
| `list-notes` | List notes and IDs with pinned notes first |
| `search-note balloons` | Find notes by a case-insensitive text fragment |
| `edit-note 1, Pick up balloons on Saturday` | Update note 1 |
| `delete-note 1` | Delete note 1 |
| `pin-note 1` | Pin note 1 |
| `unpin-note 1` | Unpin note 1 |
| `tag-note 1, project` | Add a single-word tag |
| `search-note-tag project` | Find notes by a tag, ignoring case |
| `sort-notes-by-tag` | Sort notes by their tags, with untagged notes last |

### System commands

| Command | What it does |
| --- | --- |
| `hello` | Display a greeting |
| `help` | Display all available commands |
| `exit` | Save contacts and notes and exit the assistant |
| `close` | Save contacts and notes and exit the assistant |

## Data storage

### CLI

The assistant uses Python's `pickle` module to save contacts and notes in a permanent directory inside the user's home folder:

```text
~/.nova4lab/data.pkl
```

The directory and data file are created automatically when the data is first saved.

On the first launch, the assistant starts with an empty address book and notebook.

The following data is saved:

- Contacts and phone numbers
- Addresses and email addresses
- Birthdays
- Favorite contacts
- Notes, tags, and pins
- Note IDs and the next available note ID

Data is saved when the user enters `exit` or `close`, presses Ctrl+C, or sends an end-of-file signal at the command prompt.

On the next launch, contacts and notes are restored automatically, including previous edits and deletions.

The data location is independent of the current working directory, so the assistant can be launched from different directories without losing access to saved data.

New notes receive unique IDs, including after restarting the assistant.

### Browser

The browser version saves contacts, favorites, notes, and pins in the current browser's local storage.

The browser and CLI have separate data storage.

## Publish the browser version

Once `index.html` and `main.py` are in the root of `main`, open the GitHub repository's **Settings → Pages**.

Choose **Deploy from a branch**, then **main** and **/(root)**.

Save and open the URL shown by GitHub Pages.

## Team workflow

Pick a Trello card, create a feature branch, and link the card in your pull request.

Request a review before merging and keep the merged pull request link for the course submission.

Before the final submission, test all CLI commands, error handling, and data persistence. Review the final implementation with the mentor and resolve any critical issues.
