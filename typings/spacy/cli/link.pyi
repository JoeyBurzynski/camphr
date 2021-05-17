"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional

import plac

@plac.annotations(
    origin=("package name or local path to model", "positional", None, str),
    link_name=("name of shortuct link to create", "positional", None, str),
    force=("force overwriting of existing link", "flag", "f", bool),
)
def link(origin, link_name, force: bool = ..., model_path: Optional[Any] = ...):
    """
    Create a symlink for models within the spacy/data directory. Accepts
    either the name of a pip package, or the local path to the model data
    directory. Linking models allows loading them via spacy.load(link_name).
    """
    ...