"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional

import plac

@plac.annotations(
    model=("Optional shortcut link of model", "positional", None, str),
    markdown=("Generate Markdown for GitHub issues", "flag", "md", str),
    silent=("Don't print anything (just return)", "flag", "s"),
)
def info(model: Optional[Any] = ..., markdown: bool = ..., silent: bool = ...):
    """
    Print info about spaCy installation. If a model shortcut link is
    speficied as an argument, print model information. Flag --markdown
    prints details in Markdown for easy copy-pasting to GitHub issues.
    """
    ...

def list_models(): ...
def print_markdown(data, title: Optional[Any] = ...):
    """Print data in GitHub-flavoured Markdown format for issues etc.

    data (dict or list of tuples): Label/value pairs.
    title (unicode or None): Title, will be rendered as headline 2.
    """
    ...