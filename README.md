# Final Notes

Python packages used for packaging Python projects (e.g.,
`setuptools` and `wheel`) have changed significantly over the
past decade. Any information on the internet needs to be
cross-checked against the official documentation for that
package. Be especially careful of answers on StackOverflow.

## Put a package on PyPI

To put a package on PyPI, there are two things to upload:

### Upload the wheel

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

### Upload the source

- this is the entire project
- equivalent to cloning the project repository in terms of which
  project files are included
- but better than cloning since installing from the source
  distribution also takes care of putting the project's files in
  the sys.path

## Python tools for working with packages

- [`setuptools`](https://setuptools.readthedocs.io/en/latest/)
  provides commands to build the wheel and source distributions.
    - `setuptools` is also a low-level alternative to installing
      with `pip`
- [`wheel`](https://wheel.readthedocs.io/en/stable/)
  provides the `bdist_wheel` command used in `setuptools` to
  build the wheel binary distribution
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
- `pip` is a high-level installer
    - package developers use `setuptools`, `wheel`, and `twine`,
      and `pip`
    - package users just use `pip`

# Packaging Tutorial

## Unofficial YouTube tutorial reference
See YouTube tutorial here:
[Lesson 8 - Python Applications Packaging with Setuptools
](https://www.youtube.com/watch?v=wCGsLqHOT2I)

This short video is a good summary of what packaging looks like
in practice. In addition it shows:

- virtual environment setup
- using setup.py for *development* builds (replaces editing
  PYTHONPATH or the creation of the USERSITE path)
    - See https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode

It does not cover:

- creating an account
- TestPyPI vs PyPI
- API Token creation
    - project write access *without* the account password
- declaring dependencies with `install_requires`
    - see https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies
- entry points
    - make package scripts available as executables
    - see [Pheonix Zerin's talk](https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies)

And it does not use the latest features of `setuptools`:

- the MANIFEST.in file is no longer required

## Summary of video tutorial

### `packages=setuptools.find_packages()`

Create a `setup.py` script.

- import `setuptools`
- call `setuptools.setup()`

In the call to `setup`, the key line is:

```python
packages=setuptools.find_packages()
```

This finds all of the modules defined in the package and includes
them in the package distribution.

Python identifies modules as any sub-folder containing a
`__init__.py` file.

This *does not* handle:

- requirements (dependencies on other packages), for example:
    - pygame
    - pyserial
- files that are not part of package modules, for example:
    - LICENSE.md
    - example-scripts/example.py

### test in a virtual environment

Create and activate virtual environment `virt`:

```bash
$ python -m venv virt
$ source virt/bin/activate
```

On Windows PowerShell, that looks like this:

```powershell
PS C:\Users\mike> python -m venv virt
PS C:\Users\mike> .\virt\Scripts\activate
(virt) PS C:\Users\mike>
```

To leave the virtual environment, run `deactivate`:

```powershell
(virt) PS C:\Users\mike> deactivate
PS C:\Users\mike>
```

Test that `setuptools` is installed (if the import fails, then
install setuptools):
```bash
(virt) $ python -c 'import setuptools'
```

Create the distribution:
```bash
(virt) $ python setup.py sdist
```

Doing this in PowerShell, first `cd` to the `packaging_tutorial` folder:

```powershell
(virt) PS C:\cygwin64\home\mike\programming\python\packaging_tutorial>
```

*...I omit the prompt path below for readability...*

```powershell
(virt) > python setup.py sdist
running sdist
running egg_info
creating example_pkg_mostly_upright.egg-info
writing example_pkg_mostly_upright.egg-info\PKG-INFO
writing dependency_links to example_pkg_mostly_upright.egg-info\dependency_links.txt
writing top-level names to example_pkg_mostly_upright.egg-info\top_level.txt
writing manifest file 'example_pkg_mostly_upright.egg-info\SOURCES.txt'
reading manifest file 'example_pkg_mostly_upright.egg-info\SOURCES.txt'
writing manifest file 'example_pkg_mostly_upright.egg-info\SOURCES.txt'
running check
creating example-pkg-mostly-upright-0.0.1
creating example-pkg-mostly-upright-0.0.1\example_pkg
creating example-pkg-mostly-upright-0.0.1\example_pkg_mostly_upright.egg-info
copying files to example-pkg-mostly-upright-0.0.1...
copying README.md -> example-pkg-mostly-upright-0.0.1
copying setup.py -> example-pkg-mostly-upright-0.0.1
copying example_pkg\__init__.py -> example-pkg-mostly-upright-0.0.1\example_pkg
copying example_pkg_mostly_upright.egg-info\PKG-INFO -> example-pkg-mostly-upright-0.0.1\example_pkg_mostly_upright.egg-info
copying example_pkg_mostly_upright.egg-info\SOURCES.txt -> example-pkg-mostly-upright-0.0.1\example_pkg_mostly_upright.egg-info
copying example_pkg_mostly_upright.egg-info\dependency_links.txt -> example-pkg-mostly-upright-0.0.1\example_pkg_mostly_upright.egg-info
copying example_pkg_mostly_upright.egg-info\top_level.txt -> example-pkg-mostly-upright-0.0.1\example_pkg_mostly_upright.egg-info
Writing example-pkg-mostly-upright-0.0.1\setup.cfg
creating dist
Creating tar archive
removing 'example-pkg-mostly-upright-0.0.1' (and everything under it)
```

This creates the distribution package inside folder `dist` and
prints all actions. The very last action printed is the creation
of `dist` and the tar archive in that folder.

View the contents of `dist`:
```bash
(virt) $ tar --list -f dist/PACKAGENAME-VERSION.tar.gz
```

In PowerShell:

```powershell
(virt) > tar --list -f .\dist\example-pkg-mostly-upright-0.0.1.tar.gz
example-pkg-mostly-upright-0.0.1/
example-pkg-mostly-upright-0.0.1/PKG-INFO
example-pkg-mostly-upright-0.0.1/README.md
example-pkg-mostly-upright-0.0.1/example_pkg/
example-pkg-mostly-upright-0.0.1/example_pkg/__init__.py
example-pkg-mostly-upright-0.0.1/example_pkg_mostly_upright.egg-info/
example-pkg-mostly-upright-0.0.1/example_pkg_mostly_upright.egg-info/PKG-INFO
example-pkg-mostly-upright-0.0.1/example_pkg_mostly_upright.egg-info/SOURCES.txt
example-pkg-mostly-upright-0.0.1/example_pkg_mostly_upright.egg-info/dependency_links.txt
example-pkg-mostly-upright-0.0.1/example_pkg_mostly_upright.egg-info/top_level.txt
example-pkg-mostly-upright-0.0.1/setup.cfg
example-pkg-mostly-upright-0.0.1/setup.py
```

This prints a list of files and folders in the tarball. Confirm
`find_packages()` did its job.

But note that all non-modules are missing, except for
`README.md`.

For example:

- non-Python file `LICENSE.md` is missing
- Python files that are part of the package but are not modules,
  such as an example scripts folder, are also not included by
  `find_packages()`

`README.md` is special. If a `README.md` file exists, the
`sdist` command includes it in the package distribution.

This has nothing to do with the file `setup.py` reads to generate
the `long_description` in `setuptools.setup()`.

Another special file is `MANIFEST.in`.

Remedy the missing files by creating a `MANIFEST.in` file:

```
include README
include LICENSE
include requirements.txt
recursive-include packaging_tutorial/examples/ *
```

The `MANIFEST.in` is really a list of commands and file patterns,
not a simple list of files to include.

See the full list of `MANIFEST.in` commands here:

https://packaging.python.org/guides/using-manifest-in/#manifest-in-commands

- include/exclude all files matching any of the listed patterns:
    - include pat1 pat2 ...
    - exclude pat1 pat2 ...
- include/exclude all files under directories matching
  dir-pattern that also match any of the listed patterns:
    - recursive-include dir-pattern pat1 pat2 ...
    - recursive-exclude dir-pattern pat1 pat2 ...
- include/exclude all files anywhere in the source tree matching
  any of the listed patterns:
    - global-include pat1 pat2
    - global-exclude pat1 pat2
- include/exclude all files under directories matching dir-pattern:
    - graft dir-pattern
    - prune dir-pattern

The patterns are *glob-style*:

- `*` matches zero or more characters
- `?` matches a single character
- `[chars]` matches any one of the characters inside brackets
    - the characters can be listed as in [swp] or a range as in
      [a-f], or a list of multiple ranges as in [a-fA-F0-9]

The commands are executed in the order they appear. For example,
if the goal is to include a large group of files except for some
subset, then the command to include comes first, followed by the
command to exclude.

Build the distribution again:

```bash
(virt) $ python setup.py sdist
```

In PowerShell:

```powershell
(virt) > python setup.py sdist
```

I see from the output that the new MANIFEST.in file is used. It
is read before writing the final version of SOURCES.txt:

```
reading manifest file 'example_pkg_mostly_upright.egg-info\SOURCES.txt'
reading manifest template 'MANIFEST.in'
writing manifest file 'example_pkg_mostly_upright.egg-info\SOURCES.txt'
```

And check the tarball again:

```bash
(virt) $ tar --list -f dist/packaging_tutorial-1.0.tar.gz
```

The missing files are included now.

Note that `MANIFEST.in` is an *older* way of specifying files in
the source distribution. It seems the `setuptools` package
eliminates the need to maintain a `MANIFEST.in` file, but it is
not clear to me how to include a file such as `LICENSE.md`
without writing a `MANIFEST.in`. See
https://setuptools.readthedocs.io/en/latest/setuptools.html.

I am going to continue using a `MANIFEST.in` file.

The full list of default files that are included with the `sdist`
command (generate source distribution archive) is here:

https://packaging.python.org/guides/using-manifest-in/#how-files-are-included-in-an-sdist

It is not necessary to include a default file in the
`MANIFEST.in`, but there is not harm in doing so.

It is possible to exclude a default file using an exclude or
prune command in the `MANIFEST.in`.

### upload to PyPI with Twine

```bash
(virt) $ twine upload dist/*
```

That is it. The package is searchable on PyPI.

Twine assumes the existence of a file that has fields username set to `__token__` and password set to the API Token that has write access for the project. This is not covered in the video. See the Python Pacaking Tutorial and the Python Packaging Guide.

### or use `setup.py` to continue development

Instead of uploading to PyPI, make the package available to any
Python script:

```bash
(virt) $ python setup.py develop
```

This creates a symbolic link in the site-package folder of the
virtual environment `virt`. It as as-if `import
packaging_tutorial` finds `packaging_tutorial` in the
site-packages folder. But it really finds a symbolic link
pointing to the development folder which is not in site-packages
(no development should ever be done on a folder inside
site-packages).

From the `setuptools` documentation:

> To do this, use the setup.py develop command. It works very
> similarly to setup.py install, except that it doesn’t actually
> install anything. Instead, it creates a special .egg-link file
> in the deployment directory, that links to your project’s
> source code. And, if your deployment directory is Python’s
> site-packages directory, it will also update the
> easy-install.pth file to include your project’s source code,
> thereby making it available on sys.path for all programs using
> that Python installation.

When the package is eventually ready to upload to PyPI and is
then installed with pip, the experience using the package is
identical.

This avoids repeatedly uploading to PyPI and upgrading with pip.

This is also a better method to share packages without PyPI. My
old method is to either edit the PYTHONPATH environment variable
to point to the cloned package location, or to clone to the
USERSITE folder. Instead, simply clone anywhere, then run the
`setup.py` script with the `develop` option, and the package is
effectively installed via the symbolic link. Obviously `pip` is
preferable. In this scheme, `git` takes the place of `pip` as the
package manager, using `git pull` in place of `pip --upgrade`.

## Phoenix Zerin New Zealand Python talk

https://www.youtube.com/watch?v=0W0k6zP_Lto

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
- [bdist_wheel](https://setuptools.readthedocs.io/en/latest/setuptools.html#distributing-a-setuptools-based-project) creates **binary** distribution archives in the `dist` directory
    - the archive is the .tar.gz that gets uploaded to PyPI

Commands can be combined, for example:

```powershell
$ python setup.py sdist bdist_wheel
```

This generates both the source distribution and the binary
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

