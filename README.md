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

Invalid input displays an error without stopping the assistant. For a likely typo such as `brithdays 7`, it suggests `birthdays 7`. A phrase such as `find a contact` suggests `search-contact`.

### Browser

From the repository root, where `index.html` and the Python modules are located, start a local server:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000).

The **Contacts** tab lets you search, edit, favorite, and delete contacts or remove individual phone numbers.

The **Notes** tab lets you create, search, edit, pin, and delete notes. You can also add tags, filter by tag, and sort notes by tag.

The **Birthdays** tab shows upcoming reminders and supports looking up birthdays an exact number of days ahead.

An internet connection is needed to load Pyodide. JavaScript loads the Python modules into Pyodide and sends JSON requests to the Python bridge in `index.html`. The bridge uses the shared Python models and handlers to validate inputs and process requests. JavaScript renders the results and saves browser data in local storage.

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | CLI entry point and command dispatch |
| `models.py` | Contacts, birthdays, notes, and field validation |
| `handlers.py` | Command handlers and shared birthday lookup |
| `utils.py` | Input parsing, command suggestions, and validation helpers |
| `menu.py` | CLI help menu |
| `storage.py` | CLI data loading and saving |
| `index.html` | Browser interface and JavaScript–Python bridge |
| `tests/` | Automated tests for contacts, notes, validation, parsing, and storage |

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
| `add-tag 1 project` | Add a single-word tag to note 1. Repeat to add another tag |
| `search-tag project` | Find notes by a tag, ignoring case |
| `sort-notes-by-tag` | Sort by each note's first tag alphabetically, with untagged notes last |

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

The browser version saves contacts, favorites, notes, tags, and pins in the current browser's local storage.

The browser and CLI have separate data storage.

## Automated tests

From the repository root, run:

```bash
python3 -m unittest discover -s tests -v
```

The suite contains 69 tests and uses the Python standard library.

## Publish the browser version

Keep `index.html`, `main.py`, `models.py`, `utils.py`, `handlers.py`, `storage.py`, and `menu.py` in the root of `main`. Open the GitHub repository's **Settings → Pages**.

Choose **Deploy from a branch**, then **main** and **/(root)**.

Save and open the URL shown by GitHub Pages.

## Team Members & Contributions

- **Viktoriia Humeniuk (`viktoriiahumeniuk`)** (Team Lead) built the original CLI assistant, including the address book, phone and birthday validation, weekend-adjusted birthday reminders, and contact persistence. She added address and email fields, contact renaming and deletion, and the original note creation, editing, search, and deletion commands. She also implemented contact favorites, individual phone removal, note listing and pinning, and the Pyodide browser interface with local storage. Later updates added a browser birthday view and brought the CLI’s contact search and note-tag features into the browser. [Starter CLI](https://github.com/viktoriiahumeniuk/project-Nova4Lab/pull/1) · [Contact management](https://github.com/viktoriiahumeniuk/project-Nova4Lab/pull/3) · [Notes](https://github.com/viktoriiahumeniuk/project-Nova4Lab/pull/4) · [Browser interface](https://github.com/viktoriiahumeniuk/project-Nova4Lab/pull/5) · [Browser updates](https://github.com/viktoriiahumeniuk/project-Nova4Lab/pull/8)
- **Dmytro Stasyuk (`dimastasyuk`)** (Scrum Master) implemented CLI contact search by partial name or exact phone number or email address. He extended birthday lookup to support an exact day offset while retaining the default seven-day window. He expanded CLI persistence to save and restore contacts and notes together, including note IDs and the next available ID, in `~/.nova4lab/data.pkl`. He also added the startup and `help` menus, improved handling of quoted command arguments, saved data on Ctrl+C and end-of-file, and expanded the README’s command and storage documentation. [Contact search and birthday lookup](https://github.com/viktoriiahumeniuk/project-Nova4Lab/commit/7c6ac8d) · [Persistence, CLI help, and documentation](https://github.com/viktoriiahumeniuk/project-Nova4Lab/commit/c35c42a)
- **`embarcaderestudio-wq`** (Developer) implemented CLI note tagging, case-insensitive tag search, and sorting by tag, with support for notes saved before tags were introduced. They refactored CLI command dispatch into a handler table and added suggestions for mistyped commands. They then expanded suggestions to recognize phrases such as `find a contact` and preserve arguments when suggesting a typo correction. They also documented the tag commands in the README. [Note tags and initial suggestions](https://github.com/viktoriiahumeniuk/project-Nova4Lab/commit/0428f36) · [Command and suggestion refinements](https://github.com/viktoriiahumeniuk/project-Nova4Lab/commit/83ba018)

The contribution summaries are based on Git history.

## Team workflow

Pick a Trello card, create a feature branch, and link the card in your pull request.

Request a review before merging and keep the merged pull request link for the course submission.

Before the final submission, test all CLI commands, error handling, and data persistence. Review the final implementation with the mentor and resolve any critical issues.
