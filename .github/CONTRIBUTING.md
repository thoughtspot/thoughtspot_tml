# Feedback and Contribution

We welcome any input, feedback, bug reports, and contributions via [__ThoughtSpot TML__'s GitHub Repository](http://github.com/thoughtspot/thoughtspot_tml/).

All contributions, suggestions, and feedback you submitted are accepted under the [Project's license](./LICENSE). You represent that if you do not own copyright in the code that you have the authority to submit it under the [Project's license](./LICENSE). All feedback, suggestions, or contributions are not confidential.

### Setting Up Your Environment

Fork the __ThoughtSpot TML__ repository on GitHub and then clone the fork to you local machine. For more details on forking see the [GitHub Documentation](https://help.github.com/en/articles/fork-a-repo).

```bash
git clone https://github.com/YOUR-USERNAME/thoughtspot_tml.git
```

To keep your fork up to date with changes in this repo, you can [use the fetch upstream button on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

__ThoughtSpot TML__ uses `uv` ([__docs__](https://docs.astral.sh/uv/)) to manage its dependencies. Once you have cloned the repository, run the following command from the root of the repository to setup your development environment:

```bash
cd thoughtspot_tml/
uv pip install -e ".[dev]"
uv run hatch run dev:setup
```

Now you can install the latest version of __ThoughtSpot TML__ locally using `pip`. The `-e` flag indicates that your local changes will be reflected every time you open a new Python interpreter (instead of having to reinstall the package each time).

`[dev]` indicates that pip should also install the development and documentation requirements which you can find  in `pyproject.toml` (`[project.optional-dependencies]/dev`)

__ThoughtSpot TML__ also uses [__Hatch__](https://hatch.pypa.io/latest/) to group together commands (`hatch run dev:setup`) for simpler maintenance of irregular contributors. You can observe the individual commands that are run within each named script under `[tool.hatch.envs.dev.scripts]`.

### Creating a Branch

Once your local environment is up-to-date, you can create a new git branch which will contain your contribution (always create a new branch instead of making changes to the main branch):

```bash
git switch -c <your-branch-name> dev
```

With this branch checked-out, make the desired changes to the package.

### Creating a Pull Request

When you are happy with your changes, you can commit them to your branch by running

```bash
git add <modified-file>
git commit -m "Some descriptive message about your change"
git push origin <your-branch-name>
```

You will then need to submit a pull request (PR) on GitHub asking to merge your example branch into the main __ThoughtSpot TML__ repository. For details on creating a PR see GitHub documentation [__Creating a pull request__](https://help.github.com/en/articles/creating-a-pull-request).

You can add more details about your example in the PR such as motivation for the example or why you thought it would be a good addition. You will get feedback in the PR discussion if anything needs to be changed. To make changes continue to push commits made in your local example branch to origin and they will be automatically shown in the PR.

Hopefully your PR will be answered in a timely manner and your contribution will help others in the future.

> [!IMPORTANT]
> :exclamation: __If you're writing support for a new version of ThoughtSpot__ :exclamation:
> 
> this step requires you to download `scriptability`'s EDoc protocol buffer specification from ThoughtSpot's internal version control.
>
> Building from source protos will require you to [__install the Protobuf compiler__](https://github.com/protocolbuffers/protobuf?tab=readme-ov-file#protobuf-compiler-installation) (`protoc`).
>
>  - __MacOS__ users can `brew install protobuf`
>  - __Windows__ users can `choco install protobuf`
>  - or .. manually [__download__](https://github.com/protocolbuffers/protobuf/releases), unzip, and add to your `PATH` variable.
>
> From here, you can run the following command to generate the `_scriptability.py` python module.
>
> ```bash
> uv run hatch run dev:compile
> ```
>
> If the edoc spec has significantly changed since the last built version, you _may_ need to investigate fixes. A good place to start is [`_generate/__main__.py`](../_generate/__main__.py), where the code has been heavily commented.
>

---

### Readying a Release

The __ThoughtSpot TML's__ release process is managed by [__Github Actions__](./workflows/publish.yml)!

Simply publish a new release here on Github with the appropriate next-version tag, and Github will take care of publishing it to PyPI.