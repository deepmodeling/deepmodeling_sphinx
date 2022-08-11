"""A directive to list all authors from git-shortlog."""

import subprocess
from typing import Any, Dict, Iterator

from docutils import nodes
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util import nested_parse_with_titles
from sphinx.util.docutils import SphinxDirective


def git_shortlog() -> str:
    """Return git-shortlog output as a string.
    
    Returns
    -------
    str
        Git-shortlog output.
    """
    return subprocess.check_output(['git', 'shortlog', '-s']).decode('utf-8')


def get_authors() -> Iterator[str]:
    """Yields authors from git-shortlog.
    
    Yields
    ------
    str
        Author name.
    """
    shortlog_text = git_shortlog()
    for line in shortlog_text.splitlines():
        yield line.split('\t')[1]


class AuthorsDirective(SphinxDirective):
    """authors directive."""
    has_content = False
    option_spec = dict(
    )


    def run(self):
        """Run directive."""
        authors = list(get_authors())
        new_content = StringList(authors, source="")

        node = nodes.Element()
        nested_parse_with_titles(self.state, new_content, node)

        return node.children

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive(name="git-shortlog-authors", cls=AuthorsDirective)
    return {'parallel_read_safe': True}
