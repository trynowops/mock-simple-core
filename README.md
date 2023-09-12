## Installing and Running

This is a FastAPI app.  Setup is similar to most Python projects:

1. Clone the repo.
2. Create and activate a virtual environment.

```shell
python3 -m venv venv
. ./venv/bin/activate
```

3. Install the requirements.

```shell
pip install -r requirements.txt
```

4. Run the app with an API key defined.

```shell
CORE_API_KEY=<secret> uvicorn main:app --reload
```

### Codestyle

1. Use `black`.

```shell
black .
```