# Python + FastAPI Workshop

Hands-on workshop material for learning Python from a JavaScript background, culminating in a small REST API built with FastAPI.

## What's inside

| Folder | Description |
| --- | --- |
| [`learn-basics/`](learn-basics/) | Side-by-side Python and JavaScript scripts covering the same concepts: variables, conditionals, lists/arrays, dictionaries/objects, loops, and functions. |
| [`learning-notebook-api/`](learning-notebook-api/) | A FastAPI app — a "learning notebook" where you store programming terms, tags, and whether you've learned them. |

## Comparing Python and JavaScript

The same program is written in both languages so you can diff them side by side:

- [`learn-basics/hello.py`](learn-basics/hello.py) — Python version
- [`learn-basics/hello.js`](learn-basics/hello.js) — JavaScript version

A few of the translations it demonstrates:

| Concept | Python | JavaScript |
| --- | --- | --- |
| Variable | `term = "variable"` | `const term = "variable"` |
| None / null | `None` | `null` |
| Logic | `and` / `not` | `&&` / `!` |
| Collection | `list` | `array` |
| Key-value store | `dict` (`note["term"]`) | `object` (`note.term`) |
| Length | `len(tags)` | `tags.length` |

Run them with:

```bash
python learn-basics/hello.py
node learn-basics/hello.js
```

## The Learning Notebook API

`learning-notebook-api/main.py` is a single-file FastAPI application. Data is held in memory — it resets whenever the server restarts.

### Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (the project is managed with uv)

### Run the API

```bash
cd learning-notebook-api
uv run fastapi dev main.py
```

The server starts on <http://127.0.0.1:8000>. Interactive API docs are available at:

- Swagger UI — <http://127.0.0.1:8000/docs>
- ReDoc — <http://127.0.0.1:8000/redoc>

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Health check — confirms the API is running |
| `GET` | `/terms` | List all terms. Filter with `?tag=basics` and/or `?q=var` |
| `GET` | `/terms/random` | Get a random term (404 if the notebook is empty) |
| `GET` | `/terms/{term_id}` | Get a single term by id |
| `POST` | `/terms` | Add a term (409 if the term already exists) |
| `PATCH` | `/terms/{term_id}` | Partially update a term |
| `DELETE` | `/terms/{term_id}` | Delete a term |
| `GET` | `/stats` | Totals: number of terms, how many learned, counts by tag |

### Term model

```json
{
  "id": 1,
  "term": "variable",
  "definition": "A name that stores a value.",
  "js_equivalent": "let / const",
  "tags": ["python", "basics"],
  "learned": true
}
```

When creating a term, `id` is assigned by the server. `js_equivalent`, `tags`, and `learned` are optional.

### Example requests

```bash
# List everything
curl http://127.0.0.1:8000/terms

# Search and filter
curl "http://127.0.0.1:8000/terms?q=list&tag=data"

# Add a term
curl -X POST http://127.0.0.1:8000/terms \
  -H "Content-Type: application/json" \
  -d '{"term": "tuple", "definition": "An immutable ordered collection.", "tags": ["python", "data"]}'

# Mark it as learned
curl -X PATCH http://127.0.0.1:8000/terms/5 \
  -H "Content-Type: application/json" \
  -d '{"learned": true}'

# View stats
curl http://127.0.0.1:8000/stats
```

## License

Workshop material — use freely for learning.
