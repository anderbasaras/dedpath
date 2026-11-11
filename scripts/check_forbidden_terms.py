r"""Block commits that contain confidential terms (pre-commit hook).

The list of terms is private and lives OUTSIDE the repository, so it can never
be committed by accident:

* default location: ``~/.dedpath/forbidden-terms.txt``
  (on Windows: ``%USERPROFILE%\.dedpath\forbidden-terms.txt``)
* override with the ``DEDPATH_FORBIDDEN_TERMS`` environment variable.

Format: one term per line, case-insensitive; blank lines and lines starting
with ``#`` are ignored.

The hook runs at two git stages:

* ``pre-commit``: checks the content and the path of every staged file.
* ``commit-msg``: checks the commit message (git passes the message file).

If the list file does not exist the hook FAILS on purpose: a fresh clone on a
new laptop must not be able to commit until the guard is configured.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ENV_VAR = "DEDPATH_FORBIDDEN_TERMS"
DEFAULT_PATH = Path.home() / ".dedpath" / "forbidden-terms.txt"


def _decode(raw: bytes) -> str:
    """Decode text written by any Windows editor (UTF-8, UTF-8 BOM or UTF-16)."""
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    return raw.decode("utf-8-sig", errors="replace")


def load_terms(path: Path) -> list[str]:
    """Return the casefolded, non-empty, non-comment terms in ``path``."""
    terms: list[str] = []
    for line in _decode(path.read_bytes()).splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term.casefold())
    return terms


def find_hits(name: str, terms: list[str]) -> list[str]:
    """Return human-readable hits of ``terms`` in the path and content of ``name``."""
    hits = [f"{name}: path contains a forbidden term" for t in terms if t in name.casefold()]
    try:
        text = _decode(Path(name).read_bytes())
    except OSError:
        return hits
    for lineno, line in enumerate(text.splitlines(), start=1):
        folded = line.casefold()
        hits.extend(f"{name}:{lineno}: forbidden term" for t in terms if t in folded)
    return hits


def main(argv: list[str]) -> int:
    """Check every file in ``argv``; return 1 if any forbidden term is found."""
    terms_path = Path(os.environ.get(ENV_VAR, DEFAULT_PATH))
    if not terms_path.is_file():
        print(
            f"check-forbidden-terms: list not found at {terms_path}.\n"
            "Create it (one confidential term per line) before committing. "
            "See docs/dev-log/README.md.",
            file=sys.stderr,
        )
        return 1

    terms = load_terms(terms_path)
    hits = [hit for name in argv for hit in find_hits(name, terms)]
    for hit in hits:
        # The term itself is not printed: terminal output may end up in CI logs or chats.
        print(hit, file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
