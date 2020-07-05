# Summary

## Python tools for publishing

For `python setup.py sdist`:

```bash
$ pip install --upgrade setuptools
```

For `python setup.py bdist_wheel`:

```bash
$ pip install --upgrade wheel
```

For `twine check` and `twine upload`:

```bash
$ pip install --upgrade twine
```

For `check-manifest` and `check-manifest --create`:

```bash
$ pip install check-manifest
```

## Commands to publish

Enter the project folder.

Clean out the old build:

```bash
$ rm -fr build/ dist/ *.egg-info/
```

Check repo and sdist will match:

```bash
$ check-manifest.exe
```

*This check creates the `egg-info/` folder.*

Check the `*./egg-info/PKG-INFO` file. This information shows up
on the PyPI (or TestPyPI) page, and is displayed when users do
`pip show PACKAGENAME`. For example:

- check the `Home-page` is correct
- search for `UNKNOWN` to find arguments missing from the call to
  `setuptools.setup()` in `setup.py`.

Rebuild the distributions:

```bash
$ python.exe setup.py sdist bdist_wheel
```

Check the README is valid for PyPI:

```bash
$ twine check dist/*
```

Upload to TestPyPI:

```bash
$ twine upload --repository testpypi dist/*
```

## Commands to test

Do a test installation in a virtual environment.

Create a virtual environment:

```powershell
> python -m venv test-install
> .\test-install\Scripts\activate
(test-install) >
```

Install the package. Since the package is not on PyPI, use `-i`
or `--index-url` to specify the package URL is TestPyPI:

```powershell
(test-install) > pip install -i https://test.pypi.org/simple/ PROJECTNAME
```

If the package has dependencies on packages that are not on
TestPyPI, use `--extra-index-url` to get the dependencies from
PyPI:

```powershell
(test-install) > pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple PROJECTNAME
```

*Follow the rule that PROJECTNAME == PACKAGENAME.*

Check the package is installed:

```powershell
(test-install) > pip list
```

Test importing the packaging:

```powershell
(test-install) > python -c "import PACKAGENAME"
```

*There is no deleting packages once they are uploaded to PyPI.*

Re-upload by incrementing the version number.

By logging in and clicking "Manage", it is *possible* to delete a
specific version, but that same version cannot be re-uploaded. So
there is no reason to delete a version and the interface is set
up to discourage this.

Make sure the upload is good by uploading to TestPyPI first. The
same deletion rules apply (deleting is discouraged), but the
accounts and packages there are periodically deleted. So a
publish test on TestPyPI may require incrementing the version
number a few times to get it right.

**Remember to reset to the original version number before
uploading to PyPI.**

Import to PyPI by leaving off the `--repository` argument:

```bash
$ twine upload dist/*
```

## Use UTF-8 in the "Project description"
The following line in `setup.py` uses README.md as the *Project
description* on PyPI:

```python
# Show README.md as PyPI "Project description".
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
```

Note `encoding="utf-8"`. UTF-8 is not the default encoding.
Specify UTF-8 if the README.md includes any unicode, e.g., the
branch symbols (└─, ├─) used in the output of the utility `tree`.

## Follow these naming rules

### 1. No dashes or underscores in the name

Avoid dashes and underscores.

Underscores are converted to dashes when listing packages with
`pip list`.

But dashes are not allowed in the package name when doing
`import`.

So using either underscores or dashes violates the next rule.

### 2. Project and Package use the same name

Make the project name the same as the package name so that:

```bash
$ pip install NAME
```

and

```python
>>> import NAME
```

use the same NAME.

# Final Notes

Python packages used for packaging Python projects (e.g.,
`setuptools` and `wheel`) have changed significantly over the
past decade. Any information on the internet needs to be
cross-checked against the official documentation for that
package. Be especially careful of answers on StackOverflow.

I'm using `setuptools` because it's currently what is officially
recommended. But `poetry` seems like it will win out eventually
because it is based on Rust's *Cargo* package manager (which
people like) and (probably for that reason) it is simpler than
using `setuptools`.

Anyway, this XKCD comic sums it up best:

![https://xkcd.com/1987/](https://imgs.xkcd.com/comics/python_environment.png)

# Also see

- [PackageFileStructure.md](PackageFileStructure.md)
- [PackagingTutorial.md](PackagingTutorial.md)
- [Questions.md](Questions.md)
- [PublishOnPyPI.md](PublishOnPyPI.md)

