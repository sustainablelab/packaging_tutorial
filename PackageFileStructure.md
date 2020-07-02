I explore package structures using my `pygs` package.

# Original flat structure

## PYTHONPATH

Before making `pygs` into a package, `pygs` started out as a
repository. To put the repository on the Python path, I clone the
repository by cloning in my `USER_SITE` folder.

## Structure

The flat structure looks like this:

```
pygs
├─ LICENSE.md
├─ README.md
├─ __init__.py
├─ clock.py
├─ colors.py
├─ plot.py
├─ user.py
└─ window.py
```

There are no folders. It is completely flat.

## Namespacing

With an empty `__init__.py`, doing `import pygs` results in
redundant names: `pygs.pygs.user`, `pygs.pygs.plot`,
`pygs.pygs.window.Window`, etc.

The `__init__.py` fixes this:

```python
from .window import Window
from .clock  import Clock
from . import user
from . import plot
from .colors import HEX,RGB
```

The single `.` eliminates the second `pygs`. For example, now the
`user` module is accessed as `pygs.user`, and `plot` is accessed
as `pygs.plot`.

Modules `window` and `clock` contain one class each: `Window` and
`Clock` respectively. The `.window` and `.clock` eliminate the
`pygs.window` and `pygs.clock`, making the classes accessible as
`pygs.Window` and `pygs.Clock`.

Similarly, module `colors` contains two namedtuples: `HEX` and
`RGB`. With the empty `__init__.py`, accessing `HEX` requires
`pygs.pygs.colors.HEX`. With the `from .colors import HEX,RGB`,
the `HEX` is accessed as `pygs.HEX`.

## Module and Class Visibility

Quickly test visibility of modules and classes in the `pygs`
namespace. In `ptpython`, import the package `pygs` and see which
modules/classes show up with tab-completion:

From ptpython:

```python
>>> import pygs
>>> pygs.{PRESS TAB}
```

Pressing tab after the `.`, the ptpython tab-completion lists all
of the class and module names (the words that come after the word
`import` in the above `__init__.py` file).

# Move all modules into a `src` folder

I clean up the structure by moving all the modules into a `src`
folder:

```
pygs
├─ LICENSE.md
├─ README.md
├─ __init__.py
└─ src
    ├─ clock.py
    ├─ colors.py
    ├─ plot.py
    ├─ user.py
    └─ window.py
```

To maintain the same namespacing behavior, the `__init__.py` file
changes by simply adding `src` after the `.`:

```python
from .src.window import Window
from .src.clock  import Clock
from .src import user
from .src import plot
from .src.colors import HEX,RGB
```

I repeat the `ptpython` tab-completion test and the namespacing
still works.

# Move the `__init__.py` into the `src` folder
With `__init__.py` in the `src` folder, I revert to the original
`__init__.py` file. But now I need to import `pygs.src`, and the
namespacing becomes `pygs.src.user`, `pygs.src.plot`,
`pygs.src.Clock`, etc. I want to get rid of that `src`.

# Change `src` to `pygs`

I see two conventions:

```
PyPI_project_name
└─ package_name

PyPI_project_name
└─ src
    └─ package_name
```

In the second case, the `src` folder is always empty except for
the `package_name` folder.

It seems simpler to me to make the `project_name` and
`package_name` the same name.

So I use this:

```
pygs
├─ LICENSE.md
├─ README.md
└─ pygs
    ├─ __init__.py
    ├─ clock.py
    ├─ colors.py
    ├─ plot.py
    ├─ user.py
    └─ window.py
```

Now I have a valid package structure.

To clone the repo and use the package without doing the usual
install, simply add the project path to the PYTHONPATH.

For example, if repo is cloned to USERSITE as usual, that is not
enough. Add the top-level `pygs` folder to the PYTHONPATH:

```powershell
$env:PYTHONPATH += {your USERSITE path goes here}\pygs;"
```

It's nice to clone to USERSITE and have things *just work*. But
then the structure is not correct for packaging. This is
unavoidable.

And really, once the project is set up for packaging, users can
clone it anywhere and run setup with `-e` to create the symbolic
link.
