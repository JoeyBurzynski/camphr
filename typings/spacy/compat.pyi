from typing import Any, Optional

def b_to_str(b_str): ...
def symlink_to(orig, dest): ...
def symlink_remove(link): ...
def is_config(
    python2: Optional[Any] = ...,
    python3: Optional[Any] = ...,
    windows: Optional[Any] = ...,
    linux: Optional[Any] = ...,
    osx: Optional[Any] = ...,
): ...
def import_file(name, loc): ...
def unescape_unicode(string): ...

copy_reg: Any