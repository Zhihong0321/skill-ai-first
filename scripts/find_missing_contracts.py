from __future__ import annotations

import argparse
from pathlib import Path

CODE_EXTENSIONS = {
    ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".py",
}

IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", "coverage", "test-results",
}

CONTRACT_MARKERS = ("@ai-contract",)


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def has_contract(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            # Only check first 20 lines — contract must be at the top
            for i, line in enumerate(fh):
                if i >= 20:
                    break
                if any(marker in line for marker in CONTRACT_MARKERS):
                    return True
    except OSError:
        pass
    return False


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return -1


def iter_candidates(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if is_ignored(path):
            continue
        if path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find code modules missing an @ai-contract header."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repo root to scan.")
    parser.add_argument(
        "--min-lines",
        type=int,
        default=30,
        help="Only flag files at or above this line count (default: 30).",
    )
    parser.add_argument("--top", type=int, default=30, help="Max results to show.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing = []

    for path in iter_candidates(root):
        if has_contract(path):
            continue
        lines = count_lines(path)
        if lines >= args.min_lines:
            missing.append((lines, path))

    missing.sort(key=lambda item: (-item[0], str(item[1])))

    if not missing:
        print("All modules at or above the line threshold have @ai-contract headers.")
        return 0

    print(f"Modules missing @ai-contract headers in: {root}")
    print(f"Minimum lines: {args.min_lines}")
    print(f"Showing top {args.top} by size:\n")
    for lines, path in missing[: args.top]:
        rel = path.relative_to(root)
        print(f"{lines:>6}  {rel}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
