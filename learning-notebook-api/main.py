# import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from storage import (
    add_note,
    delete_note,
    get_note,
    get_stats,
    list_notes,
    random_note,
    term_exists,
    update_note,
)

app = FastAPI()

# --- OLD: in-memory list as the "database" ---
# notes = [
#   {
#     "id": 1,
#     "term": "variable",
#     "definition": "A name that stores a value.",
#     "js_equivalent": "let / const",
#     "tags": ["python", "basics"],
#     "learned": True,
#   },
#     {
#     "id": 2,
#     "term": "list",
#     "definition": "An orderded collection of values.",
#     "js_equivalent": "array",
#     "tags": ["python", "data"],
#     "learned": True,
#   },
#   {
#     "id": 3,
#     "term": "dictionary",
#     "definition": "An unordered collection of key-value pairs.",
#     "js_equivalent": "object",
#     "tags": ["python", "data"],
#     "learned": False,
#   },
#     {
#     "id": 4,
#     "term": "function",
#     "definition": "A block of code that can be reused.",
#     "js_equivalent": "function",
#     "tags": ["python", "basics"],
#     "learned": False,
#   },
# ]
# --- NEW: notes are persisted in notes.json via storage.py ---

class NoteIn(BaseModel):
  term: str
  definition: str
  js_equivalent: str | None = None
  tags: list[str] = []
  learned: bool = False

class Note(NoteIn):
  id: int

class NoteUpdate(BaseModel):
  term: str | None = None
  definition: str | None = None
  js_equivalent: str | None = None
  tags: list[str] | None = None
  learned: bool | None = None

class Message(BaseModel):
  message: str

class Stats(BaseModel):
  total: int
  learned: int
  by_tag: dict[str, int]

@app.get("/", response_model=Message)
def root():
  return {"message": "Learning Notebook API is running"}

@app.get("/terms", response_model=list[Note])
def get_terms(tag: str | None = None, q: str | None = None):
  # OLD: filtered the in-memory list
  # result = []
  # for note in notes:
  #   if tag is not None and tag not in note["tags"]:
  #     continue
  #   if q and q.lower() not in note["term"].lower():
  #     continue
  #   result.append(note)
  # return result
  # NEW: storage reads notes.json and filters the same way
  return list_notes(tag=tag, q=q)

@app.get("/terms/random", response_model=Note)
def random_term():
  # OLD: random.choice on the in-memory list
  # if len(notes) == 0:
  #   raise HTTPException(status_code=404, detail="No terms yet!")
  # return random.choice(notes)
  # NEW:
  note = random_note()
  if note is None:
    raise HTTPException(status_code=404, detail="No terms yet!")
  return note

@app.post("/terms", status_code=201, response_model=Note)
def add_term(note: NoteIn):
  # OLD: checked duplicates, built the id, appended to the list
  # for existing in notes:
  #   if existing["term"].lower() == note.term.lower():
  #     raise HTTPException(status_code=409, detail="Term already exists")
  # new_id = max((nt["id"] for nt in notes), default=0) + 1
  # new_note = {"id": new_id}
  # new_note.update(note.model_dump())
  # notes.append(new_note)
  # return new_note
  # NEW: storage checks duplicates, assigns the id and writes notes.json
  if term_exists(note.term):
    raise HTTPException(status_code=409, detail="Term already exists")
  return add_note(note.model_dump())

@app.get("/terms/{term_id}", response_model=Note)
def get_term(term_id: int):
  # OLD: linear search over the in-memory list
  # for note in notes:
  #   if note["id"] == term_id:
  #     return note
  # raise HTTPException(status_code=404, detail="Term not found")
  # NEW:
  note = get_note(term_id)
  if note is None:
    raise HTTPException(status_code=404, detail="Term not found")
  return note

@app.patch("/terms/{term_id}", response_model=Note)
def update_term(term_id: int, changes: NoteUpdate):
  # OLD: mutated the dict inside the in-memory list
  # for note in notes:
  #   if note["id"] == term_id:
  #     note.update(changes.model_dump(exclude_unset=True))
  #     return note
  # raise HTTPException(status_code=404, detail="Term not found")
  # NEW:
  note = update_note(term_id, changes.model_dump(exclude_unset=True))
  if note is None:
    raise HTTPException(status_code=404, detail="Term not found")
  return note

@app.delete("/terms/{term_id}", status_code=204, response_model=None)
def delete_term(term_id: int):
  # OLD: removed from the in-memory list
  # for note in notes:
  #   if note["id"] == term_id:
  #     notes.remove(note)
  #     return
  # raise HTTPException(status_code=404, detail="Term not found")
  # NEW:
  if not delete_note(term_id):
    raise HTTPException(status_code=404, detail="Term not found")

@app.get("/stats", response_model=Stats)
def get_stats_endpoint():
  # OLD: counted over the in-memory list
  # learned = 0
  # by_tag = {}
  # for note in notes:
  #   if note["learned"]:
  #     learned += 1
  #   for tag in note["tags"]:
  #     by_tag[tag] = by_tag.get(tag, 0) + 1
  # return {"total": len(notes), "learned": learned, "by_tag": by_tag}
  # NEW: storage computes the same counts from notes.json
  return get_stats()
