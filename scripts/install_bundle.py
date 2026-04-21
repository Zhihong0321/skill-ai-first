from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPT_DIR.parent
MANIFEST_PATH = BUNDLE_ROOT / "bundle-manifest.json"


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_target(args: argparse.Namespace, bundle_name: str) -> Path:
    selected = [
        bool(args.target),
        bool(args.project_root),
        bool(args.skills_root),
    ]
    if sum(selected) != 1:
        raise SystemExit(
            "Choose exactly one install destination: --target, --project-root, or --skills-root."
        )

    if args.target:
        return Path(args.target).resolve()
    if args.project_root:
        return Path(args.project_root).resolve() / ".agents" / "skills" / bundle_name
    return Path(args.skills_root).resolve() / bundle_name


def ensure_clean_target(target: Path, force: bool) -> None:
    if not target.exists():
        return
    if not force:
        raise SystemExit(
            f"Target already exists: {target}\n"
            "Re-run with --force to replace it."
        )
    shutil.rmtree(target)


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def install_bundle(target: Path, entries: list[str]) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for relative in entries:
        source = BUNDLE_ROOT / relative
        if not source.exists():
            raise SystemExit(f"Manifest entry is missing from bundle root: {relative}")
        copy_entry(source, target / relative)


def main() -> int:
    manifest = load_manifest()
    bundle_name = manifest["bundle_name"]

    parser = argparse.ArgumentParser(
        description="Install the AI First Maintenance bundle as one package."
    )
    parser.add_argument(
        "--target",
        help="Explicit install directory. Example: /path/to/.agents/skills/ai-first-maintenance-bundle",
    )
    parser.add_argument(
        "--project-root",
        help="Project root to install into as <project>/.agents/skills/<bundle-name>",
    )
    parser.add_argument(
        "--skills-root",
        help="Skills directory to install into as <skills-root>/<bundle-name>",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the target if it already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved install location without copying files.",
    )
    args = parser.parse_args()

    target = resolve_target(args, bundle_name)
    if args.dry_run:
        print(f"Bundle root: {BUNDLE_ROOT}")
        print(f"Install target: {target}")
        print(f"Entry skill: {manifest['entry_skill']}")
        return 0

    ensure_clean_target(target, args.force)
    install_bundle(target, manifest["includes"])

    print(f"Installed bundle: {bundle_name}")
    print(f"Target: {target}")
    print(f"Entry skill: {manifest['entry_skill']}")
    print("Usage: run ai-first-maintenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
