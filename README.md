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

- PackageFileStructure.md
- PackagingTutorial.md
- Questions.md

# Put a package on PyPI

To put a package on PyPI, there are two things to upload:

## Upload the wheel

A `wheel` is a [built
distribution](https://packaging.python.org/glossary/#term-built-distribution).
It contains just the parts of the project necessary to run the
project on the target system. For example, the wheel contains all
the Python packages and other files necessary to import the
package. The wheel also contains any executables installed by the
package.

Python packages `setuptools` and `wheel` decide which project
files go into the wheel.

Script `setup.py` adds additional files to the wheel with
`setuptools.setup()` argument `package_data={}`:

- includes non-Python files inside of packages
- specified as a dictionary with the key as a string
  and the value as a list of strings
- if the key is an empty string, it means look for
  the files in all packages
- the strings in the value can be specific file names
  or glob-style search patterns

## Upload the source

- this is the entire project
- equivalent to cloning the project repository in terms of which
  project files are included
- but better than cloning since installing from the source
  distribution also takes care of putting the project's files in
  the sys.path

The `source distribution` should not include files that are not
included in the Git repository. The easy way to do this is to
make a `.gitignore` file. This is a top-level file with the same
syntax is the same as the `.git/info/exclude` file. Exclude
anything the user can build, e.g., `__pycache__`, `dist/`,
`*.egg-info`.

[gitignore.io](https://www.toptal.com/developers/gitignore/api/python)
has many more suggestions for what to ignore. But they include
the `MANIFEST` in this list, which doesn't make sense to me. If a
MANIFEST file exists, then I had to explicitly make it for the
source distribution build to include the necessary files, so if I
expect a user to build their own source distribution, don't they
also need the MANIFEST file? In fact, [Mark Smith's 2019
talk](https://www.youtube.com/watch?v=-WDV0-OB4fE) agrees with
me. At the 23min mark, he does `git add MANIFEST.in` after using
`check-manifest --create` to create the `MANIFEST.in` file.

# Python tools for working with packages

- [`setuptools`](https://setuptools.readthedocs.io/en/latest/)
  provides commands to build the wheel and source distributions.
    - `setuptools` is also a low-level alternative to installing
      with `pip`
- [`wheel`](https://wheel.readthedocs.io/en/stable/)
  provides the `bdist_wheel` command used in `setuptools` to
  build the wheel
    - `wheel` is not meant to be used directly
    - just install `wheel`:
        - `pip install --upgrade wheel`
    - then build the project wheel using `setuptools` in a
      `setup.py` script:
        - `python setup.py bdist_wheel`
    - typically both the source and wheel distributions are built
      in the same command:
        - `python setup.py sdist bidst_wheel`
    - this puts the distributions in a `dist/` folder
- [`pkg_resources`](https://setuptools.readthedocs.io/en/latest/pkg_resources.html)
  is distributed with `setuptools`. It provides tools to
  introspect the package.
- [`twine`](https://setuptools.readthedocs.io/en/latest/)
  provides the `upload` command to upload the project to PyPI and
  TestPyPI.
    - install `twine`:
        - `pip install --upgrade twine`
    - upload to TestPyPi:
        - `twine upload -r testpypi dist/*`
    - Twine prompts for a username and password
    - for now, just enter these each time
    - if I do this a lot, make a [keyring](https://twine.readthedocs.io/en/latest/#keyring-support)
    - or create a `~/.pypirc` file [with API tokens](https://packaging.python.org/specifications/pypirc/#using-a-pypi-token)
    - it is not secure to put the account password in the
      `~/.pypirc` file
- `check-manifest`
    - creates a `MANIFEST.in` file to match the `.gitignore`
      file, i.e., it makes the `sdist` (source distribution)
      match exactly what is on the GitHub repo
- `pip` is a high-level installer
    - package developers use `setuptools`, `wheel`, and `twine`,
      and `pip`
    - package users just use `pip`

# Documentation for setuptools

https://setuptools.readthedocs.io/en/latest/setuptools.html

This is the latest information on the correct way to use
`setuptools`. Review the documentation here before going further.
Tutorials are likely to be out-of-date.

In particular see:

https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies

> setuptools supports automatically installing dependencies when
> a package is installed

Note that `setuptools` is both a package imported in the
`setup.py` script *and* a commandline utility run as `setup.py`
followed by a command.

For example, this runs the `sdist` command:

```powershell
PS > python setup.py sdist
```

The project details are in the `setup.py` I write; the `setup`
action depends on the command following `python setup.py`.

The commands are documented here:

https://setuptools.readthedocs.io/en/latest/setuptools.html#command-reference

Important commands are:

- [develop](https://setuptools.readthedocs.io/en/latest/setuptools.html#develop-deploy-the-project-source-in-development-mode) creates a symbolic link, as if the project was installed on sys.path
- [sdist](https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use) creates **source** distribution archives in the `dist` directory
    - the archive is the .tar.gz that gets uploaded to PyPI
- [bdist_wheel](https://setuptools.readthedocs.io/en/latest/setuptools.html#distributing-a-setuptools-based-project) creates **built** distribution archives in the `dist` directory
    - the archive is the .tar.gz that gets uploaded to PyPI

Commands can be combined, for example:

```powershell
$ python setup.py sdist bdist_wheel
```

This generates both the source distribution and the built
distribution.

Note that `setup.py` does not have a command to upload to PyPI.
Use *Twine* to upload:

```bash
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

`dist/*` contains the archives created with the `python setup.py
sdist bdist_wheel` command.

And package installation from PyPI or TestPyPI is handled by
`pip`:

```bash
$ pip install --index-url https://test.pypi.org/simple/ example_pkg
```

# Official Python Packaging tutorial
See tutorial here:
https://packaging.python.org/tutorials/packaging-projects/

The tutorial uses TestPyPI instead of PyPI.

After doing the tutorial, read the Python Packaging User Guide
(see next section).

# Official Python Packaging Guide

See the user guide here:
https://packaging.python.org/guides/distributing-packages-using-setuptools/#create-an-account

The packaging tutorial creates a user account on TestPyPI. This
is NOT connected in any way to PyPI. When ready to actually
upload to PyPI, create a new user account on PyPI.

https://pypi.org/account/register/

Since the two are not connected, it is OK to use the same
username.

# Official Python Example Project
And see example project here:
https://github.com/pypa/sampleproject

# Package Directory Structure

```
packaging_tutorial
├── LICENSE.md
├── README.md
├── example_pkg
│   └── __init__.py
├── setup.py
└── tests
```

## `LICENSE.md`
The standard MIT License. Change line 1: name and copyright year.

## `README.md`
The markdown file for this package's PyPI page.

## `example_pkg`
The *actual* package (identified by the `__init__.py` file). In
practice this contains sub-folders with modules, each with their
own `__init__.py` file.

## `tests`
Make `tests` a package by adding a `__init__.py` file. The line
`packages = find_packages()` in `setuptools.setup()` adds this
`tests` folder to the distribution.

Put unit tests in `tests`. This implies that unit tests go
*outside* the actual package. Since the official Python Packaging
tutorial bothers to point this out, I will start putting my unit
tests here. Before now, I was putting unit tests inside the
package.

## `setup.py`
This script uses setuptools to install the package.

### Overview

The script contains basic info:

- package name
- version number
- author name
- author email
- link to project on GitHub

And optionally:

- required Python version
- dependencies available from PyPI
    - see `install_requires`
- dependencies available from a Git repository
    - see `dependency_links`
    - note `pip` will not install these dependencies
    - for a simple `pip` experience, put all dependencies on PyPI

The script controls what is displayed on PyPI using the file
assigned to the `long_description`.

Most importantly, this script automates discovery of Python
package dependencies using `packages = find_packages()`.

The script also lists classifiers (keywords) for:

- discovery in PyPI searches
- declaring readiness level (alpha, beta, etc.)

### Example `setup.py`

```python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-mostly-upright", # Replace with your own username
    version="0.0.1",
    author="Mike Gazes",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
```

### modules

Discovering all modules in the package is handled by this line in `setup.py`:

```python
    packages=setuptools.find_packages(),
```

### dependencies

#### Most cases: get from PyPI
Packages usually depend on other Python packages available from
PyPI.

This is handled on the line that starts `install_requires=[`

The syntax is a list of strings. Each string is, at a minimum,
the project’s PyPI name. If the package version matters, this is
included with a comparison operator: <, >, <=, >=, == or !=
followed by the version.

If the package provides extra functionality contingent on other
packages, then another line starting with `extras_require={`
defines a dictionary where the keys are the strings used by
`install_requires=[` and the values are the PyPI package names.
See:

https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies

The main effect of this line is that installing, either using `pip`  to install from PyPI or using `setup.py` to install locally, handles locating, downloading, and installing all of the dependencies.

> When your project is installed, either by using pip, setup.py
> install, or setup.py develop, all of the dependencies not
> already installed will be located (via PyPI), downloaded, built
> (if necessary), and installed.

#### Avoid using a repository URL
If a package has a dependency that is not on PyPI, this is
handled in the line starting with `dependency_links=[`

Again, this is a list of strings. Now each string is the link to
a repository URL.

See:

https://setuptools.readthedocs.io/en/latest/setuptools.html#dependencies-that-aren-t-in-pypi

But beware that dependency links are not supported by `pip`. So
I'm guessing this only works if the package is downloaded, then
`setup.py` is run manually.

#### Make dependencies platform specific

Some features are only available on some operating systems, or
sometimes a package is only required for a certain operating
system.

In this case, it makes sense to add platform information to the
`install_requires` line.

See:

https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies

### classifiers

Classifiers aid users searching PyPI.

See the full list of `classifiers` here:
https://pypi.org/classifiers/

Some that look interesting:

```python
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Embedded Systems",
    "Topic :: Terminals :: Serial",
    "Topic :: Software Development :: User Interfaces",
```

Each classifier is a link that searches PyPI. Follow the links to
get a sense of the kinds of projects that use that classifier.
For example, I wasn't sure about `Terminals :: Serial`, but
looking at the projects that use it, I'm confident it is
appropriate for a USB-connected development kit.

# Generate Package Distribution Archive (tarball)

Install the latest `setuptools` and `wheel`:

```bash
$ python3 -m pip install --user --upgrade setuptools wheel
```

Generate the distribution:

```bash
$ python3 setup.py sdist bdist_wheel
```

