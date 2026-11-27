# Nova Lab Personal Assistant

A Python assistant for managing contacts, birthdays, and notes. It runs in the terminal and has a browser interface. This is the Nova Lab team's final project for Neoversity's Python Programming course.

## Run locally

You need Python 3.10 or later. The CLI uses the Python standard library.

```bash
git clone https://github.com/viktoriiahumeniuk/project-Nova4Lab.git
cd project-Nova4Lab
```

### Terminal

```bash
python3 main.py
```

Enter a command at the prompt. Use commas between separate fields. Full names and addresses can contain spaces. Enter birthdays as `DD.MM.YYYY` and phone numbers as 10 digits.

### Browser

Keep `index.html` and `main.py` in the same folder. Start a local server from that folder:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000). The **Contacts** tab lets you search, edit, favorite, and delete contacts or remove individual phone numbers. The **Notes** tab lets you search, edit, pin, and delete notes. An internet connection is needed to load the Pyodide runtime that runs the Python models in the browser.

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
| `favorite Anna Smith` / `unfavorite Anna Smith` | Add or remove a favorite |
| `favorites` | List favorite contacts |
| `add-birthday Anna Smith, 26.11.1998` | Add or update a birthday |
| `show-birthday Anna Smith` | Show one contact's birthday |
| `birthdays` | Show birthdays from today through seven days ahead |

### Notes

| Command | What it does |
| --- | --- |
| `add-note Pick up balloons on Friday` | Create a note and show its ID |
| `list-notes` | List notes and IDs with pinned notes first |
| `search-note balloons` | Find notes by a case-insensitive text fragment |
| `edit-note 1, Pick up balloons on Saturday` | Update note 1 |
| `delete-note 1` | Delete note 1 |
| `pin-note 1` / `unpin-note 1` | Pin or unpin note 1 |

Enter `hello` for a greeting. Enter `exit` or `close` to save contacts and close the CLI.

## Data storage

- **CLI** saves contacts and favorites to `addressbook.pkl` in the directory from which you launch the app. Notes and pins are kept for the current session.
- **Browser** saves contacts, favorites, notes, and pins in the current browser's local storage. The browser and CLI have separate data.

## Publish the browser version

Once `index.html` and `main.py` are in the root of `main`, open the GitHub repository's **Settings → Pages**. Choose **Deploy from a branch**, then **main** and **/(root)**. Save and open the URL shown by GitHub Pages.

## Team workflow

Pick a Trello card, create a feature branch, and link the card in your pull request. Request a review before merging and keep the merged pull request link for the course submission.