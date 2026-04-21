from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


DEFAULT_RELATIVE_PATH = Path(".agents") / "ai-first-maintenance-log.md"
VALID_STAGES = (
    "baseline-locked",
    "map-ready",
    "digestion-ready",
    "cleaning-ready",
    "optimization-ready",
    "overhaul-ready",
)
VALID_NEXT_STAGES = VALID_STAGES + ("none",)
VALID_STATUSES = (
    "planned",
    "in-progress",
    "verification-pending",
    "complete",
    "blocked",
    "deferred",
)


def parse_iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid date '{value}'; expected YYYY-MM-DD"
        ) from exc


def resolve_log_path(repo_root: Path, explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        return path if path.is_absolute() else (repo_root / path)
    return repo_root / DEFAULT_RELATIVE_PATH


def ensure_header(log_path: Path, repo_name: str) -> str:
    return (
        f"# AI First Maintenance Log\n\n"
        f"- repo: {repo_name}\n"
        f"- purpose: staged maintenance memory for AI-first codebase management\n\n"
        f"---\n\n"
    )


def initialize_log(log_path: Path, repo_name: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text(ensure_header(log_path, repo_name), encoding="utf-8")


def append_entry(log_path: Path, args: argparse.Namespace) -> None:
    initialize_log(log_path, args.repo_name)
    entry_lines = [
        f"## {args.entry_date}",
        "",
        f"- mode: {args.mode}",
        f"- chosen stage: {args.stage}",
        f"- chosen target: {args.target}",
        f"- reason: {args.reason}",
        f"- status: {args.status}",
        f"- action taken: {args.action}",
        f"- verification: {args.verification}",
        f"- blockers: {args.blockers}",
        f"- next exact action: {args.next_action}",
        f"- next recommended stage: {args.next_stage}",
        "",
    ]
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(entry_lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or append the AI-first maintenance log.")
    parser.add_argument("--repo-root", default=".", help="Repo root path.")
    parser.add_argument("--log-path", help="Optional explicit log path.")
    parser.add_argument("--repo-name", help="Optional repo name override.")
    parser.add_argument("--init", action="store_true", help="Initialize the log if missing.")
    parser.add_argument("--mode", default="planning", choices=["planning", "action"], help="Run mode: planning or action.")
    parser.add_argument("--stage", default="map-ready", choices=VALID_STAGES, help="Chosen stage.")
    parser.add_argument("--target", default="(not selected yet)", help="Chosen target.")
    parser.add_argument("--reason", default="Initial maintenance run.", help="Why the target was chosen.")
    parser.add_argument("--status", default="planned", choices=VALID_STATUSES, help="Current status of this maintenance target.")
    parser.add_argument("--action", default="Initialized maintenance tracking.", help="What happened in this run.")
    parser.add_argument("--verification", default="Not run.", help="Verification performed.")
    parser.add_argument("--blockers", default="none", help="Blocking issue, if any.")
    parser.add_argument("--next-action", default="Continue stage selection from the current repo state.", help="Exact next step for the next session.")
    parser.add_argument("--next-stage", default="map-ready", choices=VALID_NEXT_STAGES, help="Recommended next stage.")
    parser.add_argument(
        "--date",
        dest="entry_date",
        default=str(date.today()),
        type=parse_iso_date,
        help="Entry date in YYYY-MM-DD format.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    repo_name = args.repo_name or repo_root.name
    log_path = resolve_log_path(repo_root, args.log_path)

    if args.init:
        initialize_log(log_path, repo_name)
        print(f"Initialized maintenance log at {log_path}")
        return 0

    args.repo_name = repo_name
    append_entry(log_path, args)
    print(f"Updated maintenance log at {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
