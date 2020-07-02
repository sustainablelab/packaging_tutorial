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


