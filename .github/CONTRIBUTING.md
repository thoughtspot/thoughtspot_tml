# Contributing

Contributions to `thoughtspot_tml` are encouraged and very welcome!

Contributions can come in many forms: documentation enhancements, features, bug fixes, creating issues, and participating in the community.

If you're interested in helping out, you might find some inspiration in [Issues](https://github.com/thoughtspot/thoughtspot_tml/issues). If you have an idea, but don't see it there, don't hesitate to open a new issue.

Before submitting a pull request, please make sure the enhancement or bugfix you've made has been discussed.

This will ensure no work is duplicated, and that a general approach has been agreed.

## Local development setup

```shell
python -m venv .venv
source .venv\bin\activate
pip install -e .[dev]
```

## Build

> [!IMPORTANT]
> If you're writing support for a new version of ThoughtSpot, this step requires you to download `scriptability`'s EDoc protocol buffer specification from ThoughtSpot's internal version control.
>
> ```shell
> python _generate\__main__.py
> ```

If you're not building support for a new version of ThoughtSpot, simply **[Fork this repository](https://github.com/thoughtspot/thoughtspot_tml/fork)** and when ready, **[Open a Pull Request](https://github.com/thoughtspot/thoughtspot_tml/compare)** to contribute your changes.

## Linting

```shell
ruff check src/ --config pyproject.toml
```

## Running Tests

```shell
coverage run -m ward; coverage report
```
