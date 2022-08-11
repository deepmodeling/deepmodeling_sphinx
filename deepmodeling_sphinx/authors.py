"""A directive to list all authors from git-shortlog."""

import os
import subprocess
from typing import Any, Dict, Iterator

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


def git_shortlog() -> str:
    """Return git-shortlog output as a string.
    
    Returns
    -------
    str
        Git-shortlog output.
    """
    if os.environ.get("READTHEDOCS", None) == "True":
        # check if it shallow clone
        output_git_rev_parse = subprocess.check_output(["git", "rev-parse", "--is-shallow-repository"]).decode('utf-8').strip()
        if output_git_rev_parse == "true":
            # fetch full history
            subprocess.check_output(["git", "fetch", "--unshallow"])
    return subprocess.check_output(['git', 'shortlog', 'HEAD', '-s']).decode('utf-8')


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
        authors = ["* " + author for author in get_authors()]
        self.state_machine.insert_input(authors, "")
        return []

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive(name="git-shortlog-authors", cls=AuthorsDirective)
    return {'parallel_read_safe': True}
