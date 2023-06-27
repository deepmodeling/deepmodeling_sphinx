# deepmodeling_sphinx

[![pip install](https://img.shields.io/pypi/dm/deepmodeling_sphinx?label=pip%20install&logo=pypi)](https://pypi.org/project/deepmodeling_sphinx)
[![Documentation Status](https://readthedocs.org/projects/deepmodeling-sphinx/badge/)](https://deepmodeling-sphinx.readthedocs.io/)

This package should be used in all sphinx projects under the [@deepmodeling](https://github.com/deepmodeling) organization.

## Features

- Add the DeepModeling banner
- Add the ICP number to the footer
- Minify HTML, Javascript, and CSS files
- Supports dark mode for both the banner and the RTD theme

## How to use it

### Setup

Add `deepmodeling_sphinx` to the requirements, as well as the `extensions` of `conf.py`:

```py
extensions = [
    'deepmodeling_sphinx',
]
```

Projects outside DeepModeling can also use this extension but disable DeepModeling specific styles.

```py
# default: True
enable_deepmodeling = False
```

### Render list of authors

The following directive can be used to render list of authors from `git shortlog`:

```rst
.. git-shortlog-authors::

```
