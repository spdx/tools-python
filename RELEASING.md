# Releasing

(based on [documentation](https://realpython.com/pypi-publish-python-package/))


## Switch to venv:
```
. ./venv/bin/activate.fish
```
## Tag the version
```
git tag -a "v0.8.0a1" -m "First 0.8.0 alpha tag"
```
## Install Your Package Locally
```
python -m pip install -e .
```
## To build and upload your package to PyPI, you’ll use two tools ...
```
python -m pip install build twine
```
## Build Your Package
```
python -m build
```
## Confirm Your Package Build
```
twine check dist/*
```
## Upload Your Package
```
twine upload -r pypi dist/*
```
