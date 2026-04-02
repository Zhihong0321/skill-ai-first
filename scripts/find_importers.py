from __future__ import annotations

import argparse
import re
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", "coverage", "test-results",
}

TEXT_EXTENSIONS = {
    ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".py",
    ".md", ".html", ".css", ".json", ".yaml", ".yml",
}


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def make_patterns(target: Path) -> list[re.Pattern[str]]:
    """
    Build a list of patterns that might reference the target file.
    Works for JS/TS imports, Python imports, and generic filename mentions.
    """
    stem = target.stem
    name = target.name
    patterns = [
        # JS/TS: import ... from './foo' or require('./foo')
        re.compile(rf"""['"`]([^'"`]*[/\\])?{re.escape(stem)}['"`]"""),
        # Python: import foo / from foo import
        re.compile(rf"""\b{re.escape(stem)}\b"""),
        # Raw filename
        re.compile(re.escape(name)),
    ]
    return patterns


def scan_file(path: Path, patterns: list[re.Pattern[str]]) -> list[int]:
    """Return line numbers where any pattern matches."""
    hits = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for lineno, line in enumerate(fh, start=1):
                if any(p.search(line) for p in patterns):
                    hits.append(lineno)
    except OSError:
        pass
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find files that import or reference a given module."
    )
    parser.add_argument("target", help="Path to the module to look up.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root to scan.")
    parser.add_argument(
        "--show-lines",
        action="store_true",
        help="Show the matching line numbers for each importer.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    root = Path(args.root).resolve()

    if not target.exists():
        print(f"Target not found: {target}")
        return 1

    patterns = make_patterns(target)
    results: list[tuple[Path, list[int]]] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if is_ignored(path):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.resolve() == target:
            continue  # skip the file itself
        hits = scan_file(path, patterns)
        if hits:
            results.append((path, hits))

    results.sort(key=lambda item: str(item[0]).lower())

    if not results:
        print(f"No importers found for: {target.relative_to(root)}")
        return 0

    print(f"Importers of: {target.relative_to(root)}")
    print(f"Found in {len(results)} file(s):\n")
    for path, lines in results:
        rel = path.relative_to(root)
        if args.show_lines:
            print(f"  {rel}  (lines: {', '.join(str(l) for l in lines)})")
        else:
            print(f"  {rel}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
