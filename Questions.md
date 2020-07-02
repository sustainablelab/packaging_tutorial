# Questions

## Does the actual package usually go in a `src` folder?

*Answer: dealer's choice*

The community has no standard. Back in 2013, [there was a lot of
hate on using a `src`
folder](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application)
-- someone wrote a *definitive* article on this. Answers linking
this article get lots of upvotes. Here is [another 2013 article hating on
`src`](https://kenreitz.org/essays/repository-structure-and-python). And another [out-of-date approach](https://docs.python-guide.org/writing/structure/).

I ended up looking at what other packages do by searching the
package name on PyPI and following the link to the GitHub page.

Now using `src` seems to be the recommended practice. But in
every case, the `src` folder only contains one item: the
*package* folder. So what is the purpose of the `src` folder?
Sean used the `src` folder. I decided *not* to use it for my
packages for the simple reason that it is yet another thing to
remember. I'm thinking specifically of the edit to PYTHONPATH in
the case where I am not installing the package, but I want to
make it available via USERSITE.

## PyPA sample project

The PyPA [sample project](https://github.com/pypa/sampleproject):

- uses the package name `sample` as the project name with suffix
`project`
    - the repository is named `sampleproject`
    - the `setup.py` names the PyPI project as `sampleproject`
- the package code itself goes in `sampleproject/src/sample/`
- `sample` contains:
    - `__init__.py` to define `main()`
    - module `simple.py`
    - `package_data.dat`
- the `setup.py` has two arguments in `setuptools.setup()` to
  explain where things are:
    - `package_dir={'': 'src'},`
    - `packages=find_packages(where='src'),`

This line is *very* standard:

```python
package_dir={'': 'src'},
```

It says the package files are in the `src` folder.

This seems to me like a throwback to the setup.cfg line:

```python
package_dir =
    =src
```

The setup.cfg file is a [place to put default
values](https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-cfg)
for the setup.py file. But as the PyPA sample project shows,
there's hardly anything in the setup.cfg file. So they just moved
the `package_dir = {'': 'src'}` to the setup.py file. But why?
Just use `setuptools.findpackages()`.

For my own repo, try doing a build and then look at the `dist/`
folder. If the Python files were not found with
`packages = setuptools.find_packages()`, then I should add this
line, but change `src` to the package name since I use the
package name instead of `src`.

PyPA hosts other projects, `setuptools`, and `virtualenv`. Surely
these are good examples to follow. These are made by the people
who make the tools that make and use the packages!

## PyGotham organizer Pappasam's toml-sort

[toml-sort](https://github.com/pappasam/toml-sort) is a good
example for simple projects, except for the `-` and `_`
kerfuffle.

- the repository name is the package name, except that `-` is not
  allowed in an import, so:
    - the package name is `toml-sort` on PyPI
    - the repository name is `toml-sort`
    - but import in Python as `toml_sort`
    - eliminate the `-` and `_`, and all three names are the same,
      making it easier to remember the commands for install and
      import
- package code is in `toml-sort/toml_sort`
- package contains module `tomlsort.py` that defines class
  `TomlSort`
- package `__init__.py` does a `from .tomlsort import TomlSort`
  to make class `TomlSort` available after `import toml_sort` as
  `toml_sort.TomlSort`

## PyPA setuptools

PyPA [setuptools repository](https://github.com/pypa/setuptools):

This project is not a good example because it is the package for
the `setuptools` tool which defines `setuptools.setup`, so the
`setup.py` file for this project cannot follow the standard
format. All I got from this project is:

- repository name and PyPI project name is `setuptools`
- package code goes in `setuptools/setuptools/`
- it's OK *not* to use a `src` folder
- it's OK to use the same name for the project and the package

## PyPA virtualenv

PyPA [virtualenv repository](https://github.com/pypa/virtualenv):

Again, it's OK to use the same name:

- repository name and PyPI project name is `virtualenv`
- package name is `virtualenv`

Here `src` is used, but it only contains one item:

- package code is in `virtualenv/src/virtualenv/`
    - `virtualenv` is the *only* folder in `src`
    - a single folder in `src` is common
    - so what is the point of `src`?

Looking at the `setup.py` file, this looks like an older style of
packaging: use `setup.cfg`, not `setup.py`.

The `setup.py` is only 12 lines long and does not contain any of
the *mandatory* stuff. All of that is in the `setup.cfg` file.

## Takeaways after looking at several projects

- there are no good reference projects
    - so do the simplest thing that works for your project
- the package code is always in a sub-folder of the project
- the package code can go in any of the following three folders:
    - `project_name/src`
    - `project_name/package_name`
    - `project_name/src/package_name`
- of those three, I reject the first one, which oddly enough is
  the form used in this [2019 talk by Mark
  Smith](https://www.youtube.com/watch?v=-WDV0-OB4fE), but I
  think he only used this because he is showing an example in the
  spirit of LEFT-PAD (Mark Smith's project has a single, very
  short Python file)
- I reject the first one for the USERSITE case: if the project is
  cloned to USERSITE, the import statement becomes `import src`
  which is stupid

## If I clone a project to USERSITE I need to edit PYTHONPATH

A package in USERSITE is available to import because USERSITE is
on the PYTHONPATH.

But turning this package into a project, the package code is
pushed either one level deeper by putting it in a folder with the
package name, or two levels deeper if I push it into
`src/package_name`.

The documentation for [modules and
packages](https://docs.python.org/3/tutorial/modules.html#packages)
is not very helpful. It does not explain:

- best-practice for a project repository to work both as a
  source distribution and as a repository to clone into USERSITE.
- how to use the packages `__init__.py` file to cleanup redundant
  namespacing

Whether the code is one or two levels deep, PYTHONPATH needs to
be edited.

*Add the path to the folder that contains the package*.

If the package is one level deep, e.g.:

- `USERSITE/project_name/package_name`
- or
- `USERSITE/project_name/src`

Then the path to add is `USERSITE/project_name`.

If the package is two levels deep, e.g.:

- `USERSITE/project_name/src/package_name`,

Then the path to add is `USERSITE/project_name/src`.

And as for the `__init__.py` file, that works exactly as it did
*before* turning the package into a project. For example, project
`pygs` has package `pygs` which contains a `__init__.py` that
cleans up redundant namespacing. All of the modules are scripts
in that same folder. The structure is completely flat.

## What is the package that uses the `.gitignore` file when making the `sdist`?

The Python package is called `check-manifest`.

I install it in PowerShell.

```powershell
> pip install check-manifest
```

That is all I need to do to run `check-manifest` from the Cygwin
bash command line.

- open `bash`
- `cd` into the project folder
- the folder must already have a `setup.py` file and a
  `.gitignore` file

```bash
$ check-manifest --create
```

*This creates `MANIFEST.in`.*

Add `MANIFEST.in` to the repo:

```bash
$ git add MANIFEST.in
$ git commit -m 'Generate MANIFEST file with check-manifest'
```


