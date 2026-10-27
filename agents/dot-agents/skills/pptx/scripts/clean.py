"""Remove unreferenced files from an unpacked PPTX directory.

Usage: python clean.py <unpacked_dir>

Example:
    python clean.py unpacked/

This script removes:
- Orphaned slides (not in sldIdLst) and their relationships
- [trash] directory (unreferenced files)
- Orphaned .rels files for deleted resources
- Unreferenced media, embeddings, charts, diagrams, drawings, ink files
- Unreferenced theme files
- Unreferenced notes slides
- Content-Type overrides for deleted files
"""

import sys
from pathlib import Path

import defusedxml.minidom


import posixpath
from urllib.parse import unquote, urlsplit


def relationship_target(unpacked_dir: Path, rels_file: Path, rel) -> Path | None:
    if rel.getAttribute("TargetMode").lower() == "external":
        return None
    target = urlsplit(rel.getAttribute("Target"))
    if target.scheme or target.netloc or not target.path:
        raise ValueError(f"Invalid internal relationship target in {rels_file}")
    relative = rels_file.relative_to(unpacked_dir).as_posix()
    source_dir = posixpath.dirname(posixpath.dirname(relative))
    decoded = unquote(target.path)
    normalized = posixpath.normpath(decoded.lstrip("/") if decoded.startswith("/") else posixpath.join(source_dir, decoded))
    if normalized == ".." or normalized.startswith("../"):
        raise ValueError(f"Relationship escapes package: {decoded}")
    resolved = (unpacked_dir / normalized).resolve()
    if not resolved.is_relative_to(unpacked_dir.resolve()):
        raise ValueError(f"Relationship escapes package: {decoded}")
    return Path(normalized)


def get_slides_in_sldidlst(unpacked_dir: Path) -> set[str]:
    pres_path = unpacked_dir / "ppt/presentation.xml"
    rels_path = unpacked_dir / "ppt/_rels/presentation.xml.rels"
    if not pres_path.is_file() or not rels_path.is_file():
        raise ValueError("Cannot clean slides without presentation and relationships")
    rels = defusedxml.minidom.parse(str(rels_path))
    mapping = {}
    for rel in rels.getElementsByTagNameNS("*", "Relationship"):
        if rel.getAttribute("Type").endswith("/slide"):
            target = relationship_target(unpacked_dir, rels_path, rel)
            if target is not None:
                mapping[rel.getAttribute("Id")] = target
    pres = defusedxml.minidom.parse(str(pres_path))
    root = pres.documentElement
    if root.localName != "presentation" or root.namespaceURI not in {
        "http://schemas.openxmlformats.org/presentationml/2006/main",
        "http://purl.oclc.org/ooxml/presentationml/main",
    }:
        raise ValueError("Cannot clean an invalid presentation root")
    slides = set()
    for slide in pres.getElementsByTagNameNS("*", "sldId"):
        rid = slide.getAttributeNS("http://schemas.openxmlformats.org/officeDocument/2006/relationships", "id")
        if not rid:
            rid = slide.getAttributeNS("http://purl.oclc.org/ooxml/officeDocument/relationships", "id")
        target = mapping.get(rid)
        if target is None or target.parent != Path("ppt/slides") or not (unpacked_dir / target).is_file():
            raise ValueError(f"Cannot safely resolve slide relationship {rid}")
        slides.add(target.name)
    return slides


def remove_orphaned_slides(unpacked_dir: Path) -> list[str]:
    slides_dir = unpacked_dir / "ppt" / "slides"
    slides_rels_dir = slides_dir / "_rels"
    pres_rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"

    if not slides_dir.exists():
        return []

    referenced_slides = get_slides_in_sldidlst(unpacked_dir)
    removed = []

    for slide_file in slides_dir.glob("slide*.xml"):
        if slide_file.name not in referenced_slides:
            rel_path = slide_file.relative_to(unpacked_dir)
            slide_file.unlink()
            removed.append(str(rel_path))

            rels_file = slides_rels_dir / f"{slide_file.name}.rels"
            if rels_file.exists():
                rels_file.unlink()
                removed.append(str(rels_file.relative_to(unpacked_dir)))

    if removed and pres_rels_path.exists():
        rels_dom = defusedxml.minidom.parse(str(pres_rels_path))
        for rel in list(rels_dom.getElementsByTagNameNS("*", "Relationship")):
            if rel.getAttribute("Type").endswith("/slide"):
                target = relationship_target(unpacked_dir, pres_rels_path, rel)
                if target is not None and target.as_posix() in removed:
                    rel.parentNode.removeChild(rel)
        pres_rels_path.write_bytes(rels_dom.toxml(encoding="utf-8"))

    return removed


def remove_trash_directory(unpacked_dir: Path) -> list[str]:
    trash_dir = unpacked_dir / "[trash]"
    removed = []

    if trash_dir.exists() and trash_dir.is_dir():
        for file_path in trash_dir.iterdir():
            if file_path.is_file():
                rel_path = file_path.relative_to(unpacked_dir)
                removed.append(str(rel_path))
                file_path.unlink()
        trash_dir.rmdir()

    return removed


def get_slide_referenced_files(unpacked_dir: Path) -> set:
    return get_referenced_files(unpacked_dir)


def remove_orphaned_rels_files(unpacked_dir: Path) -> list[str]:
    removed = []
    for rels_file in unpacked_dir.rglob("*.rels"):
        if rels_file == unpacked_dir / "_rels/.rels":
            continue
        source = rels_file.parent.parent / rels_file.name[:-5]
        if not source.exists():
            rels_file.unlink()
            removed.append(str(rels_file.relative_to(unpacked_dir)))
    return removed


def get_referenced_files(unpacked_dir: Path) -> set:
    referenced = set()
    for rels_file in unpacked_dir.rglob("*.rels"):
        dom = defusedxml.minidom.parse(str(rels_file))
        for rel in dom.getElementsByTagNameNS("*", "Relationship"):
            target = relationship_target(unpacked_dir, rels_file, rel)
            if target is not None:
                referenced.add(target)
    return referenced


def remove_orphaned_files(unpacked_dir: Path, referenced: set) -> list[str]:
    resource_dirs = ["media", "embeddings", "charts", "diagrams", "tags", "drawings", "ink"]
    removed = []

    for dir_name in resource_dirs:
        dir_path = unpacked_dir / "ppt" / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.glob("*"):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))

    theme_dir = unpacked_dir / "ppt" / "theme"
    if theme_dir.exists():
        for file_path in theme_dir.glob("theme*.xml"):
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))
                theme_rels = theme_dir / "_rels" / f"{file_path.name}.rels"
                if theme_rels.exists():
                    theme_rels.unlink()
                    removed.append(str(theme_rels.relative_to(unpacked_dir)))

    notes_dir = unpacked_dir / "ppt" / "notesSlides"
    if notes_dir.exists():
        for file_path in notes_dir.glob("*.xml"):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))

        notes_rels_dir = notes_dir / "_rels"
        if notes_rels_dir.exists():
            for file_path in notes_rels_dir.glob("*.rels"):
                notes_file = notes_dir / file_path.name.replace(".rels", "")
                if not notes_file.exists():
                    file_path.unlink()
                    removed.append(str(file_path.relative_to(unpacked_dir)))

    return removed


def update_content_types(unpacked_dir: Path, removed_files: list[str]) -> None:
    ct_path = unpacked_dir / "[Content_Types].xml"
    if not ct_path.exists():
        return

    dom = defusedxml.minidom.parse(str(ct_path))
    changed = False

    for override in list(dom.getElementsByTagName("Override")):
        part_name = override.getAttribute("PartName").lstrip("/")
        if part_name in removed_files:
            if override.parentNode:
                override.parentNode.removeChild(override)
                changed = True

    if changed:
        with open(ct_path, "wb") as f:
            f.write(dom.toxml(encoding="utf-8"))


def clean_unused_files(unpacked_dir: Path) -> list[str]:
    # Parse all relationships before any deletion; malformed input fails closed.
    get_referenced_files(unpacked_dir)
    get_slides_in_sldidlst(unpacked_dir)
    all_removed = []

    slides_removed = remove_orphaned_slides(unpacked_dir)
    all_removed.extend(slides_removed)

    trash_removed = remove_trash_directory(unpacked_dir)
    all_removed.extend(trash_removed)

    while True:
        removed_rels = remove_orphaned_rels_files(unpacked_dir)
        referenced = get_referenced_files(unpacked_dir)
        removed_files = remove_orphaned_files(unpacked_dir, referenced)

        total_removed = removed_rels + removed_files
        if not total_removed:
            break

        all_removed.extend(total_removed)

    if all_removed:
        update_content_types(unpacked_dir, all_removed)

    return all_removed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean.py <unpacked_dir>", file=sys.stderr)
        print("Example: python clean.py unpacked/", file=sys.stderr)
        sys.exit(1)

    unpacked_dir = Path(sys.argv[1])

    if not unpacked_dir.exists():
        print(f"Error: {unpacked_dir} not found", file=sys.stderr)
        sys.exit(1)

    removed = clean_unused_files(unpacked_dir)

    if removed:
        print(f"Removed {len(removed)} unreferenced files:")
        for f in removed:
            print(f"  {f}")
    else:
        print("No unreferenced files found")
