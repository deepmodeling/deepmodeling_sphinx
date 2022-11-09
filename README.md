# deepmodeling_sphinx

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
