# Contributing

## Getting Started

```shell
python -m venv .venv
source .venv\bin\activate
pip install -e .[dev]
```

## Build

```shell
download edoc.proto from internal version control
python _generate\__main__.py
```

## Linting

```shell
black . --config pyproject.toml
```

## Running Tests

```shell
coverage run -m ward; coverage report
```
