"""JSON file storage for the Learning Notebook API.

All notes live in notes.json next to this file. Every helper loads the file,
changes what it needs, and writes the whole list back, so the file on disk is
always the source of truth (nothing is kept in memory between requests).
"""

import json
import random
from pathlib import Path

DATA_FILE = Path(__file__).parent / "notes.json"

SEED_NOTES = [
    {
        "id": 1,
        "term": "variable",
        "definition": "A name that stores a value.",
        "js_equivalent": "let / const",
        "tags": ["python", "basics"],
        "learned": True,
    },
    {
        "id": 2,
        "term": "list",
        "definition": "An orderded collection of values.",
        "js_equivalent": "array",
        "tags": ["python", "data"],
        "learned": True,
    },
    {
        "id": 3,
        "term": "dictionary",
        "definition": "An unordered collection of key-value pairs.",
        "js_equivalent": "object",
        "tags": ["python", "data"],
        "learned": False,
    },
    {
        "id": 4,
        "term": "function",
        "definition": "A block of code that can be reused.",
        "js_equivalent": "function",
        "tags": ["python", "basics"],
        "learned": False,
    },
]


def load_notes() -> list[dict]:
    """Read notes.json. On the first run, create it from SEED_NOTES."""
    if not DATA_FILE.exists():
        save_notes(SEED_NOTES)
        return [note.copy() for note in SEED_NOTES]
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def save_notes(notes: list[dict]) -> None:
    """Write the full list of notes to notes.json (atomically via a temp file)."""
    temp_file = DATA_FILE.with_suffix(".json.tmp")
    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2, ensure_ascii=False)
    temp_file.replace(DATA_FILE)


def list_notes(tag: str | None = None, q: str | None = None) -> list[dict]:
    """All notes, optionally filtered by tag and by a substring of the term."""
    notes = load_notes()
    result = []
    for note in notes:
        if tag is not None and tag not in note["tags"]:
            continue
        if q and q.lower() not in note["term"].lower():
            continue
        result.append(note)
    return result


def random_note() -> dict | None:
    """A single random note, or None when there are no notes."""
    notes = load_notes()
    if not notes:
        return None
    return random.choice(notes)


def term_exists(term: str) -> bool:
    """Case-insensitive check for an existing term."""
    return any(note["term"].lower() == term.lower() for note in load_notes())


def add_note(data: dict) -> dict:
    """Append a note (without id) and give it the next id."""
    notes = load_notes()
    new_id = max((note["id"] for note in notes), default=0) + 1
    new_note = {"id": new_id, **data}
    notes.append(new_note)
    save_notes(notes)
    return new_note


def get_note(term_id: int) -> dict | None:
    """Find one note by id, or None."""
    for note in load_notes():
        if note["id"] == term_id:
            return note
    return None


def update_note(term_id: int, changes: dict) -> dict | None:
    """Apply changes to a note and persist them. None if the id doesn't exist."""
    notes = load_notes()
    for note in notes:
        if note["id"] == term_id:
            note.update(changes)
            save_notes(notes)
            return note
    return None


def delete_note(term_id: int) -> bool:
    """Remove a note. Returns False if the id doesn't exist."""
    notes = load_notes()
    for note in notes:
        if note["id"] == term_id:
            notes.remove(note)
            save_notes(notes)
            return True
    return False


def get_stats() -> dict:
    """Totals and per-tag counts computed from the stored notes."""
    notes = load_notes()
    learned = 0
    by_tag = {}
    for note in notes:
        if note["learned"]:
            learned += 1
        for tag in note["tags"]:
            by_tag[tag] = by_tag.get(tag, 0) + 1
    return {"total": len(notes), "learned": learned, "by_tag": by_tag}
