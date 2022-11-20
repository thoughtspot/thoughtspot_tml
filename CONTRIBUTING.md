# Contributing

```shell
python -m venv .venv
source .venv\bin\activate
pip install -e .[dev]
```

```shell
black . --config pyproject.toml
```

```shell
download edoc.proto from internal version control
python _generate\__main__.py
```
