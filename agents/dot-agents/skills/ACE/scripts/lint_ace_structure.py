#!/usr/bin/env python3

"""Validate an Obsidian vault against ACE folder structure rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}\.md$")
YEAR_RE = re.compile(r"^\d{4}\.md$")


@dataclass
class Check:
    level: str
    code: str
    path: str
    message: str


ESSENTIAL_REQUIRED = [
    "+",
    "Atlas",
    "Atlas/Maps",
    "Atlas/Dots",
    "Atlas/Dots/Things",
    "Atlas/Dots/Statements",
    "Atlas/Dots/People",
    "Atlas/Dots/Sources",
    "Calendar",
    "Calendar/Journals",
    "Calendar/Reviews",
    "Calendar/Meetings",
    "Efforts",
    "Efforts/On",
    "Efforts/Ongoing",
    "Efforts/Simmering",
    "Efforts/Sleeping",
    "Efforts/Notes",
]

ESSENTIAL_RECOMMENDED = [
]

IDEAVERSE_REQUIRED = ESSENTIAL_REQUIRED + [
    "x",
]

IDEAVERSE_RECOMMENDED = [
    "x/Templates",
    "x/Images",
]

CAPTURE_FOLDER = "+"
TEMPLATES_FOLDER = "x/Templates"
DAILY_NOTE_TEMPLATE = f"{TEMPLATES_FOLDER}/Template, Properties, Daily Note (Kit).md"
BASE_NOTE_TEMPLATE = f"{TEMPLATES_FOLDER}/template-base.md"
LEGACY_BASE_TEMPLATES = [
    f"{TEMPLATES_FOLDER}/Template Base.md",
    f"{TEMPLATES_FOLDER}/Template, Properties, Base.md",
]
CURRENT_YEAR = str(date.today().year)
DAILY_NOTES_FOLDER = f"Calendar/Journals/{CURRENT_YEAR}"
KEEP_ME_FILE = ".keepme"
IGNORED_FILES = {".DS_Store"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an Obsidian vault against ACE folder structure rules.",
    )
    parser.add_argument(
        "--vault",
        required=True,
        help="Absolute path to the Obsidian vault to validate.",
    )
    parser.add_argument(
        "--profile",
        choices=["essential", "ideaverse"],
        default="essential",
        help="Validation profile. Default: essential.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format. Default: json.",
    )
    return parser.parse_args()


def check_directory(vault: Path, relative_path: str, level: str) -> Check | None:
    target = vault / relative_path
    if target.is_dir():
        return None
    message = "Missing required ACE folder." if level == "error" else "Recommended ACE folder is missing."
    return Check(level=level, code="missing-folder", path=relative_path, message=message)


def load_json(path: Path) -> tuple[object | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def filtered_entries(directory: Path) -> list[Path]:
    return [entry for entry in directory.iterdir() if entry.name not in IGNORED_FILES]


def calendar_checks(vault: Path) -> list[Check]:
    """Check Calendar structure for the new Journals/Reviews/Meetings layout."""
    checks: list[Check] = []
    calendar_root = vault / "Calendar"
    journals_dir = calendar_root / "Journals"
    reviews_dir = calendar_root / "Reviews"
    meetings_dir = calendar_root / "Meetings"
    
    # Check for old structure (Legacy check - these are warnings, not errors)
    old_notes_dir = calendar_root / "Notes"
    old_logs_dir = calendar_root / "Logs"
    
    if old_notes_dir.is_dir():
        checks.append(
            Check(
                level="warning",
                code="legacy-calendar-notes",
                path="Calendar/Notes",
                message=(
                    "Found legacy `Calendar/Notes/` folder. "
                    "The recommended structure uses `Calendar/Journals/<Year>/` instead."
                ),
            )
        )
    
    if old_logs_dir.is_dir():
        checks.append(
            Check(
                level="warning",
                code="legacy-calendar-logs",
                path="Calendar/Logs",
                message=(
                    "Found legacy `Calendar/Logs/` folder. "
                    "Logs should now go in `Calendar/Journals/<Year>/` as dated entries."
                ),
            )
        )
    
    # Check Journals structure
    if journals_dir.is_dir():
        year_folders = [d for d in journals_dir.iterdir() if d.is_dir() and d.name.isdigit() and len(d.name) == 4]
        
        if year_folders:
            checks.append(
                Check(
                    level="info",
                    code="journals-year-folders",
                    path="Calendar/Journals",
                    message=f"Found {len(year_folders)} year folder(s) in Journals: {', '.join(sorted(d.name for d in year_folders))}",
                )
            )
            
            # Check for daily/monthly notes in year folders
            for year_folder in sorted(year_folders, key=lambda x: x.name):
                daily_notes = []
                monthly_notes = []
                for entry in year_folder.iterdir():
                    if not entry.is_file() or entry.suffix != ".md":
                        continue
                    if DATE_RE.match(entry.name):
                        daily_notes.append(entry.name)
                    elif MONTH_RE.match(entry.name):
                        monthly_notes.append(entry.name)
                
                if daily_notes or monthly_notes:
                    note_types = []
                    if daily_notes:
                        note_types.append(f"{len(daily_notes)} daily note(s)")
                    if monthly_notes:
                        note_types.append(f"{len(monthly_notes)} monthly note(s)")
                    checks.append(
                        Check(
                            level="info",
                            code=f"journals-{year_folder.name}-contents",
                            path=f"Calendar/Journals/{year_folder.name}",
                            message=f"Found {', '.join(note_types)}.",
                        )
                    )
        else:
            checks.append(
                Check(
                    level="warning",
                    code="journals-empty",
                    path="Calendar/Journals",
                    message="Journals folder exists but contains no year folders. Create folders like `Journals/2025/`.",
                )
            )
    
    # Check Reviews structure
    if reviews_dir.is_dir():
        review_files = [f for f in reviews_dir.iterdir() if f.is_file() and f.suffix == ".md" and YEAR_RE.match(f.name)]
        if review_files:
            checks.append(
                Check(
                    level="info",
                    code="reviews-present",
                    path="Calendar/Reviews",
                    message=f"Found {len(review_files)} yearly review(s): {', '.join(sorted(f.name for f in review_files))}",
                )
            )
    
    # Check Meetings structure
    if meetings_dir.is_dir():
        meeting_files = [f for f in meetings_dir.iterdir() if f.is_file() and f.suffix == ".md"]
        if meeting_files:
            checks.append(
                Check(
                    level="info",
                    code="meetings-present",
                    path="Calendar/Meetings",
                    message=f"Found {len(meeting_files)} meeting note(s).",
                )
            )
    
    return checks


def support_folder_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []

    if (vault / "x").is_dir():
        checks.append(
            Check(
                level="info",
                code="support-folder-present",
                path="x",
                message="Found `x/` support folder.",
            )
        )

    return checks


def keepme_checks(vault: Path, profile: str) -> list[Check]:
    checks: list[Check] = []
    folder_paths = ESSENTIAL_REQUIRED if profile == "essential" else IDEAVERSE_REQUIRED + IDEAVERSE_RECOMMENDED

    for relative_path in folder_paths:
        target = vault / relative_path
        if not target.is_dir():
            continue

        entries = filtered_entries(target)
        if not entries:
            checks.append(
                Check(
                    level="warning",
                    code="missing-keepme",
                    path=relative_path,
                    message=(
                        f"Folder is empty. Add `{KEEP_ME_FILE}` so git can keep this required ACE folder checked in."
                    ),
                )
            )
            continue

        if len(entries) == 1 and entries[0].name == KEEP_ME_FILE:
            checks.append(
                Check(
                    level="info",
                    code="keepme-present",
                    path=f"{relative_path}/{KEEP_ME_FILE}",
                    message="Found placeholder file for an otherwise empty ACE folder.",
                )
            )

    return checks


def app_config_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []
    app_config_path = vault / ".obsidian" / "app.json"

    if not app_config_path.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-app-config",
                path=".obsidian/app.json",
                message=(
                    "Missing Obsidian app config. New notes cannot be verified to land in the ACE capture folder. "
                    f"Set `newFileLocation` to `folder` and `newFileFolderPath` to `{CAPTURE_FOLDER}`."
                ),
            )
        )
        return checks

    app_config, error = load_json(app_config_path)
    if error is not None:
        checks.append(
            Check(
                level="warning",
                code="invalid-app-config",
                path=".obsidian/app.json",
                message=f"Could not parse Obsidian app config: {error}",
            )
        )
        return checks

    new_file_location = app_config.get("newFileLocation")
    new_file_folder_path = app_config.get("newFileFolderPath")

    if new_file_location != "folder":
        checks.append(
            Check(
                level="warning",
                code="capture-location-mode",
                path=".obsidian/app.json",
                message=(
                    "Obsidian new file location is not set to `folder`. "
                    f"Set `newFileLocation` to `folder` so new captures can default to `{CAPTURE_FOLDER}`."
                ),
            )
        )

    if new_file_folder_path != CAPTURE_FOLDER:
        checks.append(
            Check(
                level="warning",
                code="capture-folder-path",
                path=".obsidian/app.json",
                message=(
                    f"Obsidian new file folder path is `{new_file_folder_path}` instead of `{CAPTURE_FOLDER}`. "
                    f"Set `newFileFolderPath` to `{CAPTURE_FOLDER}` so raw captures land in the ACE cooling pad."
                ),
            )
        )
    elif new_file_location == "folder":
        checks.append(
            Check(
                level="info",
                code="capture-folder-configured",
                path=".obsidian/app.json",
                message=f"Obsidian new files are configured to land in `{CAPTURE_FOLDER}`.",
            )
        )

    placeholder_paths = []
    for folder_path in ESSENTIAL_REQUIRED + IDEAVERSE_RECOMMENDED:
        keepme_path = vault / folder_path / KEEP_ME_FILE
        if keepme_path.is_file():
            placeholder_paths.append(str(keepme_path.relative_to(vault)))

    user_ignore_filters = app_config.get("userIgnoreFilters")
    if not isinstance(user_ignore_filters, list):
        checks.append(
            Check(
                level="warning",
                code="missing-user-ignore-filters",
                path=".obsidian/app.json",
                message=(
                    f"Obsidian user ignore filters are missing. Add `{KEEP_ME_FILE}` or the placeholder paths so empty ACE folders stay hidden in file lists."
                ),
            )
        )
        return checks

    missing_filters = [
        placeholder_path
        for placeholder_path in placeholder_paths
        if KEEP_ME_FILE not in user_ignore_filters and placeholder_path not in user_ignore_filters
    ]
    if missing_filters:
        checks.append(
            Check(
                level="warning",
                code="unfiltered-keepme",
                path=".obsidian/app.json",
                message=(
                    "Add placeholder filters to `userIgnoreFilters` so empty ACE folders stay out of the file list: "
                    + ", ".join(f"`{path}`" for path in missing_filters)
                ),
            )
        )
    elif placeholder_paths:
        checks.append(
            Check(
                level="info",
                code="keepme-filtered",
                path=".obsidian/app.json",
                message="Placeholder files are hidden from Obsidian's file list.",
            )
        )

    return checks


def daily_notes_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []
    config_path = vault / ".obsidian" / "daily-notes.json"

    if not config_path.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-daily-notes-config",
                path=".obsidian/daily-notes.json",
                message=(
                    "Missing Daily Notes config. Set the daily notes folder and template so new daily notes land in the ACE journal structure."
                ),
            )
        )
        return checks

    config, error = load_json(config_path)
    if error is not None:
        checks.append(
            Check(
                level="warning",
                code="invalid-daily-notes-config",
                path=".obsidian/daily-notes.json",
                message=f"Could not parse Daily Notes config: {error}",
            )
        )
        return checks

    folder = config.get("folder")
    template = config.get("template")

    if folder != DAILY_NOTES_FOLDER:
        checks.append(
            Check(
                level="warning",
                code="daily-note-folder-path",
                path=".obsidian/daily-notes.json",
                message=(
                    f"Daily Notes folder is `{folder}` instead of `{DAILY_NOTES_FOLDER}`. Set it so new daily notes land in the current ACE journal year."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="daily-note-folder-configured",
                path=".obsidian/daily-notes.json",
                message=f"Daily Notes are configured to land in `{DAILY_NOTES_FOLDER}`.",
            )
        )

    if template != DAILY_NOTE_TEMPLATE:
        checks.append(
            Check(
                level="warning",
                code="daily-note-template-path",
                path=".obsidian/daily-notes.json",
                message=(
                    f"Daily Notes template is `{template}` instead of `{DAILY_NOTE_TEMPLATE}`. Set it so new daily notes start from the ACE daily template."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="daily-note-template-configured",
                path=".obsidian/daily-notes.json",
                message=f"Daily Notes use `{DAILY_NOTE_TEMPLATE}`.",
            )
        )

    template_file = vault / DAILY_NOTE_TEMPLATE
    if not template_file.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-daily-note-template-file",
                path=DAILY_NOTE_TEMPLATE,
                message="Configured daily note template file is missing.",
            )
        )

    return checks


def templates_config_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []
    config_path = vault / ".obsidian" / "templates.json"

    if not config_path.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-templates-config",
                path=".obsidian/templates.json",
                message=(
                    f"Missing Templates config. Set the templates folder to `{TEMPLATES_FOLDER}` so it matches the ACE support structure."
                ),
            )
        )
        return checks

    config, error = load_json(config_path)
    if error is not None:
        checks.append(
            Check(
                level="warning",
                code="invalid-templates-config",
                path=".obsidian/templates.json",
                message=f"Could not parse Templates config: {error}",
            )
        )
        return checks

    folder = config.get("folder")
    if folder != TEMPLATES_FOLDER:
        checks.append(
            Check(
                level="warning",
                code="template-folder-path",
                path=".obsidian/templates.json",
                message=(
                    f"Templates folder is `{folder}` instead of `{TEMPLATES_FOLDER}`. Set it so template settings match the ACE support structure."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="template-folder-configured",
                path=".obsidian/templates.json",
                message=f"Templates folder is configured as `{TEMPLATES_FOLDER}`.",
            )
        )

    base_template_file = vault / BASE_NOTE_TEMPLATE
    if not base_template_file.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-base-note-template",
                path=BASE_NOTE_TEMPLATE,
                message=(
                    f"Missing canonical base template. Create `{BASE_NOTE_TEMPLATE}` and use it as the ACE base template for new notes."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="base-note-template-present",
                path=BASE_NOTE_TEMPLATE,
                message=f"Found canonical ACE base template at `{BASE_NOTE_TEMPLATE}`.",
            )
        )

    legacy_templates = [template_path for template_path in LEGACY_BASE_TEMPLATES if (vault / template_path).is_file()]
    if legacy_templates:
        checks.append(
            Check(
                level="warning",
                code="legacy-base-note-template",
                path=TEMPLATES_FOLDER,
                message=(
                    "Legacy base template filenames are still present. Consolidate on `"
                    + BASE_NOTE_TEMPLATE
                    + "`: "
                    + ", ".join(f"`{path}`" for path in legacy_templates)
                ),
            )
        )

    return checks


def note_composer_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []
    config_path = vault / ".obsidian" / "note-composer.json"

    if not config_path.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-note-composer-config",
                path=".obsidian/note-composer.json",
                message=(
                    f"Missing Note Composer config. Set its template to `{BASE_NOTE_TEMPLATE}` so new derived notes use the ACE base template."
                ),
            )
        )
        return checks

    config, error = load_json(config_path)
    if error is not None:
        checks.append(
            Check(
                level="warning",
                code="invalid-note-composer-config",
                path=".obsidian/note-composer.json",
                message=f"Could not parse Note Composer config: {error}",
            )
        )
        return checks

    template = config.get("template")
    if template != BASE_NOTE_TEMPLATE:
        checks.append(
            Check(
                level="warning",
                code="note-composer-template-path",
                path=".obsidian/note-composer.json",
                message=(
                    f"Note Composer template is `{template}` instead of `{BASE_NOTE_TEMPLATE}`. Set it so new notes use the canonical ACE base template."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="note-composer-template-configured",
                path=".obsidian/note-composer.json",
                message=f"Note Composer uses `{BASE_NOTE_TEMPLATE}` for new notes.",
            )
        )

    return checks


def periodic_notes_checks(vault: Path) -> list[Check]:
    checks: list[Check] = []
    plugins_path = vault / ".obsidian" / "community-plugins.json"
    plugins_config, plugins_error = load_json(plugins_path) if plugins_path.is_file() else (None, None)
    if plugins_error is not None or not isinstance(plugins_config, list) or "periodic-notes" not in plugins_config:
        return checks

    config_path = vault / ".obsidian" / "plugins" / "periodic-notes" / "data.json"
    if not config_path.is_file():
        checks.append(
            Check(
                level="warning",
                code="missing-periodic-notes-config",
                path=".obsidian/plugins/periodic-notes/data.json",
                message="Periodic Notes is enabled but its config file is missing.",
            )
        )
        return checks

    config, error = load_json(config_path)
    if error is not None:
        checks.append(
            Check(
                level="warning",
                code="invalid-periodic-notes-config",
                path=".obsidian/plugins/periodic-notes/data.json",
                message=f"Could not parse Periodic Notes config: {error}",
            )
        )
        return checks

    active_calendar_set = config.get("activeCalendarSet")
    calendar_sets = config.get("calendarSets")
    if not isinstance(calendar_sets, list):
        return checks

    active_set = next((item for item in calendar_sets if item.get("id") == active_calendar_set), None)
    if not isinstance(active_set, dict):
        checks.append(
            Check(
                level="warning",
                code="missing-active-calendar-set",
                path=".obsidian/plugins/periodic-notes/data.json",
                message="Periodic Notes active calendar set is missing or invalid.",
            )
        )
        return checks

    day_config = active_set.get("day")
    if not isinstance(day_config, dict) or not day_config.get("enabled"):
        return checks

    folder = day_config.get("folder")
    template = day_config.get("templatePath")

    if folder != DAILY_NOTES_FOLDER:
        checks.append(
            Check(
                level="warning",
                code="periodic-daily-folder-path",
                path=".obsidian/plugins/periodic-notes/data.json",
                message=(
                    f"Periodic Notes daily folder is `{folder}` instead of `{DAILY_NOTES_FOLDER}`. Set it so plugin-created daily notes land in the ACE journal year."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="periodic-daily-folder-configured",
                path=".obsidian/plugins/periodic-notes/data.json",
                message=f"Periodic Notes daily folder is configured as `{DAILY_NOTES_FOLDER}`.",
            )
        )

    if template != DAILY_NOTE_TEMPLATE:
        checks.append(
            Check(
                level="warning",
                code="periodic-daily-template-path",
                path=".obsidian/plugins/periodic-notes/data.json",
                message=(
                    f"Periodic Notes daily template is `{template}` instead of `{DAILY_NOTE_TEMPLATE}`. Set it so plugin-created daily notes use the ACE daily template."
                ),
            )
        )
    else:
        checks.append(
            Check(
                level="info",
                code="periodic-daily-template-configured",
                path=".obsidian/plugins/periodic-notes/data.json",
                message=f"Periodic Notes daily template is configured as `{DAILY_NOTE_TEMPLATE}`.",
            )
        )

    return checks


def build_checks(vault: Path, profile: str) -> list[Check]:
    checks: list[Check] = []
    required = ESSENTIAL_REQUIRED if profile == "essential" else IDEAVERSE_REQUIRED
    recommended = ESSENTIAL_RECOMMENDED if profile == "essential" else IDEAVERSE_RECOMMENDED

    for relative_path in required:
        check = check_directory(vault, relative_path, "error")
        if check is not None:
            checks.append(check)

    for relative_path in recommended:
        check = check_directory(vault, relative_path, "warning")
        if check is not None:
            checks.append(check)

    checks.extend(calendar_checks(vault))
    checks.extend(support_folder_checks(vault))
    checks.extend(keepme_checks(vault, profile))
    checks.extend(app_config_checks(vault))
    checks.extend(daily_notes_checks(vault))
    checks.extend(templates_config_checks(vault))
    checks.extend(note_composer_checks(vault))
    checks.extend(periodic_notes_checks(vault))

    return checks


def render_text(profile: str, vault: Path, checks: list[Check]) -> str:
    errors = [check for check in checks if check.level == "error"]
    warnings = [check for check in checks if check.level == "warning"]
    infos = [check for check in checks if check.level == "info"]

    lines = [
        f"ACE lint profile: {profile}",
        f"Vault: {vault}",
        f"Errors: {len(errors)} | Warnings: {len(warnings)} | Info: {len(infos)}",
    ]

    for group_name, group_checks in (("Errors", errors), ("Warnings", warnings), ("Info", infos)):
        if not group_checks:
            continue
        lines.append("")
        lines.append(f"{group_name}:")
        for check in group_checks:
            lines.append(f"- [{check.code}] {check.path}: {check.message}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()

    if not vault.exists():
        print(json.dumps({"error": f"Vault path does not exist: {vault}"}, indent=2))
        return 2
    if not vault.is_dir():
        print(json.dumps({"error": f"Vault path is not a directory: {vault}"}, indent=2))
        return 2

    checks = build_checks(vault, args.profile)
    error_count = sum(1 for check in checks if check.level == "error")
    warning_count = sum(1 for check in checks if check.level == "warning")

    payload = {
        "profile": args.profile,
        "vault": str(vault),
        "passed": error_count == 0,
        "error_count": error_count,
        "warning_count": warning_count,
        "checks": [asdict(check) for check in checks],
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(args.profile, vault, checks))

    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())
