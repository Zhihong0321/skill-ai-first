from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_REPO = "Zhihong0321/skill-ai-first"
DEFAULT_REF = "main"


def archive_url(repo: str, ref: str) -> str:
    return f"https://codeload.github.com/{repo}/zip/refs/heads/{ref}"


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


def download_and_extract(repo: str, ref: str, workdir: Path) -> Path:
    zip_path = workdir / "bundle.zip"
    urllib.request.urlretrieve(archive_url(repo, ref), zip_path)

    extract_dir = workdir / "extract"
    with zipfile.ZipFile(zip_path) as bundle_zip:
        bundle_zip.extractall(extract_dir)

    manifests = list(extract_dir.rglob("bundle-manifest.json"))
    if not manifests:
        raise SystemExit(
            "Downloaded GitHub archive does not contain bundle-manifest.json. "
            "Push the bundle packaging changes to GitHub first."
        )
    if len(manifests) > 1:
        raise SystemExit("Multiple bundle manifests found in downloaded archive.")
    return manifests[0].parent


def load_manifest(bundle_root: Path) -> dict:
    manifest_path = bundle_root / "bundle-manifest.json"
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def install_bundle(bundle_root: Path, manifest: dict, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for relative in manifest["includes"]:
        source = bundle_root / relative
        if not source.exists():
            raise SystemExit(f"Manifest entry is missing from downloaded bundle: {relative}")
        copy_entry(source, target / relative)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the AI First Maintenance bundle directly from GitHub."
    )
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo in owner/name form.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="GitHub branch name to install from.")
    parser.add_argument("--target", help="Explicit install directory.")
    parser.add_argument("--project-root", help="Project root to install into as <project>/.agents/skills/<bundle-name>.")
    parser.add_argument("--skills-root", help="Skills directory to install into as <skills-root>/<bundle-name>.")
    parser.add_argument("--force", action="store_true", help="Replace the target if it already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved install location without downloading.")
    args = parser.parse_args()

    bundle_name = "ai-first-maintenance-bundle"
    target = resolve_target(args, bundle_name)

    if args.dry_run:
        print(f"Repo: {args.repo}")
        print(f"Ref: {args.ref}")
        print(f"Install target: {target}")
        return 0

    with tempfile.TemporaryDirectory(prefix="ai-first-maintenance-gh-") as temp_dir:
        bundle_root = download_and_extract(args.repo, args.ref, Path(temp_dir))
        manifest = load_manifest(bundle_root)
        bundle_name = manifest["bundle_name"]
        target = resolve_target(args, bundle_name)
        ensure_clean_target(target, args.force)
        install_bundle(bundle_root, manifest, target)

    print(f"Installed bundle from GitHub: {args.repo}@{args.ref}")
    print(f"Target: {target}")
    print("Entry skill: ai-first-maintenance")
    print("Usage: run ai-first-maintenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
