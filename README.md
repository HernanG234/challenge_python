# Python Challenge

This challenge was developed as part of an interview process.

## How to run

The code itself does nothing, all the functions and classes declared are not being properly used.
BUT we can run the tests provided to see that it's working code.

### Docker (Recommended)

1. Using `Make`:
```bash
    $ make build
    $ make test
```

2. Using `docker-compose`:
```bash
    $ docker compose build
    $ docker-compose run --entrypoint "pytest" -v "${PWD}":/app challenge
```

### Virtual Env
```bash
    $ python -m venv .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt
    $ pytest
```
