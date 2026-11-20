import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

notes = [
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
  result = []
  for note in notes:
    if tag is not None and tag not in note["tags"]:
      continue
    if q and q.lower() not in note["term"].lower():
      continue
    result.append(note)
  return result

@app.get("/terms/random", response_model=Note)
def random_term():
  if len(notes) == 0:
    raise HTTPException(status_code=404, detail="No terms yet!")
  return random.choice(notes)

@app.post("/terms", status_code=201, response_model=Note)
def add_term(note: NoteIn):
  for existing in notes:
    if existing["term"].lower() == note.term.lower():
      raise HTTPException(status_code=409, detail="Term already exists")
  new_id = max((nt["id"] for nt in notes), default=0) + 1
  new_note = {"id": new_id}
  new_note.update(note.model_dump())
  notes.append(new_note)
  return new_note

@app.get("/terms/{term_id}", response_model=Note)
def get_term(term_id: int):
  for note in notes:
    if note["id"] == term_id:
      return note
  raise HTTPException(status_code=404, detail="Term not found")

@app.patch("/terms/{term_id}", response_model=Note)
def update_term(term_id: int, changes: NoteUpdate):
  for note in notes:
    if note["id"] == term_id:
      note.update(changes.model_dump(exclude_unset=True))
      return note
  raise HTTPException(status_code=404, detail="Term not found")

@app.delete("/terms/{term_id}", status_code=204, response_model=None)
def delete_term(term_id: int):
  for note in notes:
    if note["id"] == term_id:
      notes.remove(note)
      return
  raise HTTPException(status_code=404, detail="Term not found")

@app.get("/stats", response_model=Stats)
def get_stats():
  learned = 0
  by_tag = {}
  for note in notes:
    if note["learned"]:
      learned += 1
    for tag in note["tags"]:
      by_tag[tag] = by_tag.get(tag, 0) + 1
  return {"total": len(notes), "learned": learned, "by_tag": by_tag}