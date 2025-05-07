
# Contributing

This project adheres to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Please read the first section of `CHANGELOG.md`.

Clone the repository from [GitHub](https://github.com/adrian-gallus/lazy-signals-python/).
Make sure that you have `pipenv` installed. You may change the required python version in `Pipfile` to match your local installation; we recommend sticking with `>=3.6`. Run `pipenv install --dev` to resolve all (development) dependencies. (You can locally install this library by running `pipenv install -e .`; it will adhere to changes made to the source code. However, it should already be installed by the previous step, as specified in the `Pipfile`.)

Use
 - `pipenv run example` to test the installation,
 - `pipenv run docs` to build the docs,
-  `pipenv run read` to open them via `xdg-open`, and
 - `pipenv run package` to package the project.
