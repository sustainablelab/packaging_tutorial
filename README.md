# Also see

- [PackageFileStructure.md](PackageFileStructure.md)
- [PackagingTutorial.md](PackagingTutorial.md)
- [Questions.md](Questions.md)
- [PublishOnPyPI.md](PublishOnPyPI.md)

# PyPI Publishing Summary

## Distribution Tools

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

## Distribution Build Commands

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

## Distribution Publishing Commands

Upload to TestPyPI:

```bash
$ twine upload --repository testpypi dist/*
```

## Distribution Testing Commands

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

Example, test installing `microspec`:

```powershell
(test-install) > pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ microspec
```

The `--extra-index-url` is required for `pip` to find requirement
`pyserial`.

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

# PyPI Publishing Details

I highlight two issues here that I found to be poorly documented
at the time that I wrote this up:

- naming conventions
- packaging data files

For more details about project setup and publishing:

- [PackageFileStructure.md](PackageFileStructure.md)
- [PublishOnPyPI.md](PublishOnPyPI.md)

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

## Maintain three separate documents

I put the real documentation on *Read the Docs*. This includes
tutorials, how-to guides, explanatory discussion, and reference
docs auto-generated with Sphinx extension `sphinx.ext.autodoc`.

In addition to the *real* documentation there are two more short
but important documents: `PyPI.md` and `README.md`.

When users land on the PyPI page, they need just enough
information to install the project and test the install works.
More information is just noise and doesn't belong here.

If there are common problems with install or basic use, the PyPI
page also needs that troubleshooting information.

Installation and use are short, hopefully a line or two dedicated
to each.

The only section that deserves length is troubleshooting because
the user cannot do much if they cannot install and do some basic
operation to see that the installation worked.

Absolutely no explanations or details about the project belong
in PyPI.md.

I like to hide `PyPI.md` in a `doc/` folder. To use `PyPI.md` in
`setup.py`:

```python
with open("doc/PyPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
```

*The build process cannot find "doc/PyPI.md" if it is not in the
`MANIFEST.in`. Make sure the file is under version control, then
`check-manifest` takes care of `MANIFEST.in`.*

The `README.md` is the landing page for the project homepage. Use
`README.md` for project development notes. The project homepage
should link to the PyPI landing page (or the repository's copy of
PyPI.md) for the basic install/use/troubleshoot instructions.

## Follow these project and package naming rules

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

And

```python
>>> import NAME
```

Use the same NAME.

I broke this rule: `microspec` named its package `microspeclib`
planning for future packages that depend on `microspeclib`.

In hindsight, the better solution is to put those future packages
in their own distributions (then I could have named the package
`microspec` and dropped the `lib`).

This is better because it is simpler to test and document a
smaller project *and* it gives the end user more control over
what gets installed.

Future distributions, like `microspecgui` use the
`install_requires` parameter in `setuptools.setup()` to
automatically install `microspec`.

## Include data files

Projects depend on files that are not part of Python packages.
For example, project `mirospecgui` installs a GUI application,
`microspec-gui`. The application needs a font file and an image
file for the Window icon.

Here is the package structure:

```
.
├── doc
│   └── PyPI.md
├── LICENSE.md
├── MANIFEST.in
├── microspecgui
│   ├── __init__.py
│   ├── __main__.py
│   └── _gui
│       ├── consola.ttf
│       └── icon.png
├── README.md
└── setup.py
```

Using the generic `setuptools.setup()` call, the `_gui/` folder
is *not* included in the distribution because it is not a Python
package.

Here is that generic `setuptools.setup()`, ignoring the
irrelevant parameters that describe the project:

```python
setuptools.setup(
    ...
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "microspec-gui=microspecgui.__main__:main",
            ],
        },
    install_requires=[
        "pygstuff",
        "microspec"
        ],
    ...
)
```

The `setuptools.find_packages()` includes the Python packages in
the distribution. The only package is `microspecgui`. `_gui/` is
a sub-folder of `microspecgui` but since it does not contain an
`__init__.py`, it is not a package, so it is not included.

A solution often-cited, but incorrect, is to put an empty
`__init__.py` file in the `_gui/` folder. This *does* make it a
package, which *does* include the folder in the distribution. But
the data files inside `_gui/` **are not included**.

Try it out for yourself. There are three steps to make this a
repeatable experiment:

```bash
$ rm -fr build/ dist/ microspecgui.egg-info/
$ check-manifest
$ python.exe setup.py sdist bdist_wheel
```

I will break these down step-by-step:

1. Clean out the old build:

```bash
$ rm -fr build/ dist/ microspecgui.egg-info/
```

2. Run `check-manifest` to be sure `MANIFEST.in` matches the Git
   index of files under version control:

```bash
$ check-manifest
```

If `MANIFEST.in` does not exist yet, create it from the Git index
of files under version control:

```bash
$ check-manifest --create
```

Here is the `MANIFEST.in` that is created:

```
include *.md
recursive-include doc *.md
recursive-include microspecgui *.png
recursive-include microspecgui *.ttf
```

*There is no reason to manually edit this file.*

As long as everything that *should be* under version control is
under version control (i.e., *is part* of the Git index),
`check-manifest --create` does the right thing.

Files are not part of the Git index if they are ignored in a
.gitignore, excluded in a .git/info/exclude, or simply new files
that have not been added to the index yet.

And if any files are under version control that *should not be*
under version control, `check-manifest` issues a warning and
specifies which files it recommends removing from the Git index.

`check-manifest` is fantastic.

3. Build:

```bash
$ python.exe setup.py sdist bdist_wheel
```

Now inspect the `sdist` (source distribution) and `bdist_wheel`
(build distribution) to see if they include the data files.

Look at the contents of the `sdist`:

```bash
$ tar --list -f dist/microspecgui-0.0.1a6.tar.gz
microspecgui-0.0.1a6/
...
microspecgui-0.0.1a6/microspecgui/__init__.py
microspecgui-0.0.1a6/microspecgui/__main__.py
microspecgui-0.0.1a6/microspecgui/_gui/
microspecgui-0.0.1a6/microspecgui/_gui/consola.ttf <-- yay!
microspecgui-0.0.1a6/microspecgui/_gui/icon.png    <-- yay!
...
```

So the `sdist` includes the data files if `MANIFEST.in` says to
include them. There is nothing extra to do. The generic
`setuptools.setup()` is sufficient *for the sdist*.

Look at the contents of the `bdist`:

```bash
$ python check-whl.py
microspecgui/__init__.py
microspecgui/__main__.py
microspecgui-0.0.1a6.dist-info/LICENSE.md
microspecgui-0.0.1a6.dist-info/METADATA
microspecgui-0.0.1a6.dist-info/WHEEL
microspecgui-0.0.1a6.dist-info/entry_points.txt
microspecgui-0.0.1a6.dist-info/top_level.txt
microspecgui-0.0.1a6.dist-info/RECORD
```

Where `check-whl.py` is this three line script:

```python
from zipfile import ZipFile
path = "dist/microspecgui-0.0.1a6-py3-none-any.whl"
print('\n'.join(ZipFile(path).namelist()))
```

The *bdist* is missing the data files.

The `_gui/` folder is completely missing.

What if I create `_gui/__init__.py`? *The data files are still
not there!* The `_gui/` folder *is included* but it does not
contain the icon and font files!

Nevermind the legacy-bollocks on StackOverflow. The fix is *one
line of code* in setup.py:

```python
setuptools.setup(
    ...
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "microspec-gui=microspecgui.__main__:main",
            ],
        },
    install_requires=[
        "pygstuff",
        "microspec"
        ],
    include_package_data=True, # <-- adds data files to bdist
    ...
)
```

With the fix in place, redo the experiment:

```bash
$ rm -fr build/ dist/ microspecgui.egg-info/
$ check-manifest
$ python.exe setup.py sdist bdist_wheel
```

Make sure the `sdist` still has the data files:

```bash
$ tar --list -f dist/microspecgui-0.0.1a6.tar.gz
microspecgui-0.0.1a6/
...
microspecgui-0.0.1a6/microspecgui/__init__.py
microspecgui-0.0.1a6/microspecgui/__main__.py
microspecgui-0.0.1a6/microspecgui/_gui/
microspecgui-0.0.1a6/microspecgui/_gui/consola.ttf <-- yay!
microspecgui-0.0.1a6/microspecgui/_gui/icon.png    <-- yay!
...
```

Look at the contents of the `bdist`:

```bash
$ python check-whl.py
microspecgui/__init__.py
microspecgui/__main__.py
microspecgui/_gui/consola.ttf        <--- yay!
microspecgui/_gui/icon.png           <--- yay!
microspecgui-0.0.1a6.dist-info/LICENSE.md
microspecgui-0.0.1a6.dist-info/METADATA
microspecgui-0.0.1a6.dist-info/WHEEL
microspecgui-0.0.1a6.dist-info/entry_points.txt
microspecgui-0.0.1a6.dist-info/top_level.txt
microspecgui-0.0.1a6.dist-info/RECORD
```

Note that `pip install -e .` *is not* a way to test if data files
are included in the bdist. The symbolic link causes the
installation to behave as if the data files are included (because
they already exist locally on the developer's computer).

After `pip install microspecgui`, the data files are in the
virtual environment's `lib/site-packages/microspecgui/` folder,
using the exact same file structure shown above in the list of
the `whl` contents.

# Final Notes

Experimentation is key. Use TestPyPI because `pip install -e .`
can hide missing data files. And do all install tests inside
virtual environments.

Python packages used for packaging Python projects (e.g.,
`setuptools` and `wheel`) have changed significantly over the
past decade. Any information on the internet needs to be
cross-checked against the official documentation for that
package. Be especially careful of answers on StackOverflow.

For example, the "solutions" on StackOverflow about how to
include package data are contradictory and outdated.

I'm using `setuptools` because it's currently what is officially
recommended. But `poetry` seems like it will win out eventually
because it is based on Rust's *Cargo* package manager (which
people like) and people say it is simpler than using
`setuptools`.

Anyway, this XKCD comic sums it up best:

![https://xkcd.com/1987/](https://imgs.xkcd.com/comics/python_environment.png)

