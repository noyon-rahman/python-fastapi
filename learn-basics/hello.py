print("Hello from Python!")

term = "variable"
print(f"Today: {term}")

learned = False
definition = None

print(learned, definition)

if learned:
  print("Already learned!")
else:
  print("Still learning...")

if term == "variable" and not learned:
  print("Time to learn variables!")

tags = ["python", "basics"]
tags.append("api")
print(len(tags))
print("api" in tags)

note = { "term": "variable", "definition": "A name that stores a value."}
print(note["term"])

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

for note in notes:
  print(note["term"])

query = "LI"
for note in notes:
  if query.lower() in note["term"].lower():
    print("Found:", note["term"])

def find_term(notes: list, name: str):
  for note in notes:
    if note["term"] == name:
      return note

print(find_term(notes, "dict"))
print(find_term(notes, "class"))
print(find_term(notes, 42))