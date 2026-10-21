# API examples

Start server:
```bash
uvicorn app.main:app --app-dir backend --reload
```

## Service status
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

## Submit symptom information
```bash
curl -X POST http://127.0.0.1:8000/api/triage \
  -H 'Content-Type: application/json' \
  -d '{"symptoms":"mild headache","age":20,"duration":"since this morning","severity":3}'
```

## List recent sessions
```bash
curl 'http://127.0.0.1:8000/api/sessions?limit=10'
```

## Get one session
```bash
curl http://127.0.0.1:8000/api/sessions/1
```

The `/docs` page lets you run these requests interactively. Use only synthetic sample data.
