#!/usr/bin/env python3
"""Assisted vocabulary checks for ASD-STE100 Issue 9.

The vocabulary never decides meaning or part of speech from context. It
matches the surfaces that the caller configured: dictionary words and their
explicit ``forms``, and project terminology terms, forms, and aliases. A clean
result is a prompt for human review, never a certification of compliance.
``spans`` returns only spans that a caller explicitly marks ``count_as_one``;
ordinary technical nouns stay normal words for word-count checks.
"""

import json
import os
import re
from dataclasses import dataclass, replace
from typing import NamedTuple, Optional

__all__ = ["Vocabulary"]

DICTIONARY_POS = frozenset(
    {"n", "v", "adj", "adv", "pron", "art", "prep", "conj", "phrase", "prefix"})
TERMINOLOGY_POS = frozenset({"n", "v"})
NOUN_CATEGORY_MAX = 22
VERB_CATEGORY_MAX = 4

LEVEL = "advisory-free"
_UNKNOWN_MESSAGE = (
    "'{surface}' is not recognized by the supplied Issue 9 dictionary export or "
    "project terminology. Review the source's completeness, use an approved "
    "word, or establish a qualified technical term with a definition and category.")

# A token is a run of Unicode letters/digits with internal apostrophes.
# Digits stay inside the token so "port80" can never be approved by "port".
_TOKEN_RE = re.compile(r"[^\W_]+(?:['\u2019][^\W_]+)*")

# A numeric quantity directly before a count_as_one unit term. The pattern
# bridges exactly one ASCII space; the lookbehind stops partial matches inside
# thousands separators, signed quantities, and identifiers such as "v10".
_QUANTITY_BEFORE_UNIT = re.compile(
    r"(?<![\w.,+\-])([0-9]+(?:\.[0-9]+)?) \Z")
_UNIT_CATEGORY = 9

# Higher rank wins when two configured entries match exactly the same tokens.
_RANK_TERM = 4
_RANK_ALIAS = 3
_RANK_APPROVED = 2
_RANK_UNAPPROVED = 1


class _Token(NamedTuple):
    text: str
    key: str
    start: int
    end: int


@dataclass(frozen=True)
class _Entry:
    tokens: tuple
    gaps: tuple
    rank: int
    kind: str
    rule: str
    message: str
    count_as_one: bool = False
    pos: Optional[str] = None
    category: Optional[int] = None
    prefix: str = ""
    suffix: str = ""


def _shown_path(path):
    shown = path if isinstance(path, str) else os.fspath(path)
    if isinstance(shown, bytes):
        shown = shown.decode("utf-8", "replace")
    return shown


def _fail(path, kind, message):
    raise ValueError(f"{_shown_path(path)}: {kind}: {message}")


def _key(text):
    """Case-insensitive lookup key that keeps both apostrophe styles."""
    return text.lower().replace("\u2019", "'")


def _phrase_parts(surface):
    """Return lowercase tokens, exact gaps, and leading/trailing punctuation.

    Gaps are preserved so that "fuel-pump" and "fuel pump" stay different
    surfaces. Gaps are not normalised here; whitespace gaps are treated as
    soft separators only during matching.
    """
    matches = list(_TOKEN_RE.finditer(surface))
    keys = tuple(_key(match.group(0)) for match in matches)
    gaps = tuple(surface[left.end():right.start()]
                 for left, right in zip(matches, matches[1:]))
    prefix = surface[:matches[0].start()] if matches else surface
    suffix = surface[matches[-1].end():] if matches else ""
    return keys, gaps, prefix, suffix


def _surface_key(surface):
    """Normalised key for collision checks; whitespace runs become one space."""
    keys, gaps, prefix, suffix = _phrase_parts(surface)
    parts = []
    for index, token in enumerate(keys):
        parts.append(token)
        if index < len(gaps):
            gap = gaps[index]
            parts.append(" " if not gap.strip() else gap)
    return prefix, tuple(parts), suffix


def _is_soft_separator(gap):
    """True when GAP may join the words of one configured surface.

    One space, one newline, or a newline with at most one adjacent space is a
    soft wrap. Two or more ASCII spaces are the mask that the Markdown linter
    leaves for code, so they are a hard boundary. Tabs and blank lines are
    boundaries too.
    """
    if not gap:
        return True
    if any(character not in " \r\n" for character in gap):
        return False
    if gap.count(" ") > 1:
        return False
    if gap.count("\n") > 1 or gap.count("\r") > 1:
        return False
    if "\r" in gap and "\r\n" not in gap:
        return False
    return True


def _tokenize(text):
    tokens = []
    for match in _TOKEN_RE.finditer(text):
        surface = match.group(0)
        tokens.append(_Token(surface, _key(surface), match.start(), match.end()))
    return tokens


def _unapproved_message(surface, pos, alternatives):
    message = f"The supplied Issue 9 dictionary marks {surface!r} as non-approved for part of speech {pos!r}."
    if alternatives:
        message += (" Review the listed alternatives without changing meaning."
                    " Alternatives (data only): " + json.dumps(alternatives) + ".")
    else:
        message += (" Use an approved word, or add a qualified technical term "
                    "with a definition and category.")
    return message


def _read_json(path, kind):
    """Read one JSON source or raise ValueError with the path and a next step."""
    shown = _shown_path(path)
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as error:
        detail = error.strerror or str(error)
        raise ValueError(
            f"{shown}: cannot read {kind}: {detail}. "
            f"Check that the file exists and is readable.") from error
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(
            f"{shown}: {kind} is not valid UTF-8 "
            f"({error.reason} at byte {error.start}). Save the file as UTF-8."
        ) from error
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{shown}: invalid JSON in {kind} at line {error.lineno}, "
            f"column {error.colno}: {error.msg}. Fix the JSON syntax."
        ) from error


def _root(data, path, kind):
    if not isinstance(data, dict):
        _fail(path, kind, "the top-level JSON value must be an object")
    issue = data.get("issue")
    if type(issue) is not int or issue != 9:
        _fail(path, kind,
              '"issue" must be the integer 9 (ASD-STE100 Issue 9), not a '
              "string, float, or boolean")
    source = data.get("source")
    if not isinstance(source, str) or not source.strip():
        _fail(path, kind,
              '"source" must be a non-empty string that names the source')
    entries = data.get("entries")
    if not isinstance(entries, list):
        _fail(path, kind, '"entries" must be a list')
    return entries


def _require_string(item, field, path, kind, where):
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        _fail(path, kind, f"{where}.{field} must be a non-empty string")
    return value.strip()


def _optional_string(item, field, path, kind, where):
    if field not in item:
        return None
    value = item[field]
    if not isinstance(value, str) or not value.strip():
        _fail(path, kind, f"{where}.{field} must be a non-empty string when present")
    return value.strip()


def _string_list(item, field, path, kind, where):
    value = item.get(field, [])
    if not isinstance(value, list):
        _fail(path, kind, f"{where}.{field} must be a list of strings")
    surfaces = []
    seen = set()
    for index, entry in enumerate(value):
        if not isinstance(entry, str) or not entry.strip():
            _fail(path, kind,
                  f"{where}.{field}[{index}] must be a non-empty string")
        surface = entry.strip()
        if not _TOKEN_RE.search(surface):
            _fail(path, kind,
                  f"{where}.{field}[{index}] must contain a letter or digit")
        surface_key = _surface_key(surface)
        if surface_key in seen:
            continue
        seen.add(surface_key)
        surfaces.append(surface)
    return surfaces


def _dictionary_entries(data, path):
    kind = "dictionary"
    raw_entries = _root(data, path, kind)
    if not raw_entries:
        _fail(path, kind,
              '"entries" must not be empty; supply approved entries or omit '
              "the dictionary file")

    entries = []
    approved_count = 0
    seen = {}
    # Every surface approval, including forms, so a form cannot contradict a
    # headword of the same part of speech (or the reverse).
    seen_surfaces = {}
    for index, item in enumerate(raw_entries):
        where = f"entries[{index}]"
        if not isinstance(item, dict):
            _fail(path, kind, f"{where} must be an object")
        word = _require_string(item, "word", path, kind, where)
        keys, gaps, prefix, suffix = _phrase_parts(word)
        if not keys:
            _fail(path, kind, f"{where}.word must contain a letter or digit")

        pos = item.get("pos")
        if not isinstance(pos, str) or pos not in DICTIONARY_POS:
            _fail(path, kind,
                  f"{where}.pos must be one of: "
                  + ", ".join(sorted(DICTIONARY_POS)))

        approved = item.get("approved")
        if type(approved) is not bool:
            _fail(path, kind,
                  f"{where}.approved must be a boolean (true or false)")

        meaning = _optional_string(item, "meaning", path, kind, where)
        meaning_ref = _optional_string(item, "meaning_ref", path, kind, where)
        if approved and meaning is None and meaning_ref is None:
            _fail(path, kind,
                  f"{where}.meaning is required for an approved entry unless "
                  "meaning_ref identifies its authoritative dictionary entry")

        forms = _string_list(item, "forms", path, kind, where)
        alternatives = _string_list(item, "alternatives", path, kind, where)
        # Preserved metadata: restricted uses still need review against the PDF.
        _string_list(item, "restricted_uses", path, kind, where)

        duplicate_key = (_surface_key(word), pos)
        if duplicate_key in seen:
            previous = seen[duplicate_key]
            if previous != approved:
                _fail(path, kind,
                      f"conflicting entries for {word!r} (pos {pos}): one is "
                      "approved and one is not")
            _fail(path, kind,
                  f"duplicate entry for {word!r} (pos {pos}); keep exactly one")
        seen[duplicate_key] = approved
        previous = seen_surfaces.get(duplicate_key)
        if previous is not None and previous != approved:
            _fail(path, kind,
                  f"conflicting entries for {word!r} (pos {pos}): one is "
                  "approved and one is not")
        seen_surfaces.setdefault(duplicate_key, approved)

        if approved:
            approved_count += 1
            message = ""
            rank = _RANK_APPROVED
            entry_kind = "approved"
            rule = ""
        else:
            message = _unapproved_message(word, pos, alternatives)
            rank = _RANK_UNAPPROVED
            entry_kind = "unapproved"
            rule = "dictionary-word"

        base = _Entry(tokens=tuple(keys), gaps=tuple(gaps), rank=rank,
                      kind=entry_kind, rule=rule, message=message, pos=pos,
                      prefix=prefix, suffix=suffix)
        entries.append(base)
        for form in forms:
            form_keys, form_gaps, form_prefix, form_suffix = _phrase_parts(form)
            if (form_keys, form_gaps, form_prefix, form_suffix) == (keys, gaps, prefix, suffix):
                continue
            form_key = (_surface_key(form), pos)
            previous = seen_surfaces.get(form_key)
            if previous is not None and previous != approved:
                _fail(path, kind,
                      f"conflicting entries for form {form!r} (pos {pos}): one "
                      "is approved and one is not")
            # The same surface can be a form of more than one approved entry
            # (for example, "more" is a form of both "many" and "much").
            seen_surfaces.setdefault(form_key, approved)
            form_message = ("" if approved
                            else _unapproved_message(form, pos, alternatives))
            entries.append(replace(base, tokens=tuple(form_keys),
                                   gaps=tuple(form_gaps), prefix=form_prefix,
                                   suffix=form_suffix, message=form_message))

    if not approved_count:
        _fail(path, kind,
              '"entries" must contain at least one approved entry')
    return entries


def _terminology_entries(data, path):
    kind = "terminology"
    raw_entries = _root(data, path, kind)

    entries = []
    registry = {}
    for index, item in enumerate(raw_entries):
        where = f"entries[{index}]"
        if not isinstance(item, dict):
            _fail(path, kind, f"{where} must be an object")
        term = _require_string(item, "term", path, kind, where)
        term_keys, term_gaps, term_prefix, term_suffix = _phrase_parts(term)
        if not term_keys:
            _fail(path, kind, f"{where}.term must contain a letter or digit")

        pos = item.get("pos")
        if not isinstance(pos, str) or pos not in TERMINOLOGY_POS:
            _fail(path, kind, f"{where}.pos must be 'n' or 'v'")

        definition = _require_string(item, "definition", path, kind, where)

        category = item.get("category")
        if type(category) is not int:
            _fail(path, kind, f"{where}.category must be an integer")
        category_max = NOUN_CATEGORY_MAX if pos == "n" else VERB_CATEGORY_MAX
        if not 1 <= category <= category_max:
            _fail(path, kind,
                  f"{where}.category {category} is out of range for pos "
                  f"{pos!r}; use 1..{category_max}")

        forms = _string_list(item, "forms", path, kind, where)
        aliases = _string_list(item, "aliases", path, kind, where)

        count_as_one = item.get("count_as_one", False)
        if type(count_as_one) is not bool:
            _fail(path, kind, f"{where}.count_as_one must be a boolean")
        if pos == "v" and "count_as_one" in item:
            _fail(path, kind,
                  f"{where}.count_as_one is only valid on noun terms (pos 'n')")

        metadata = (pos, definition, category, count_as_one)

        def register(surface, role):
            surface_key = _surface_key(surface)
            previous = registry.get(surface_key)
            if previous is None:
                registry[surface_key] = (term, role, metadata)
                return
            previous_term, previous_role, previous_metadata = previous
            if previous_role == "term" or role == "term":
                if role == "term":
                    _fail(path, kind,
                          f"term {term!r} collides with the {previous_role} "
                          f"{surface!r} of term {previous_term!r}; surfaces "
                          "must be unambiguous")
                _fail(path, kind,
                      f"{role} {surface!r} collides with the canonical term "
                      f"{previous_term!r}; surfaces must be unambiguous")
            if previous_role == "alias" or role == "alias":
                _fail(path, kind,
                      f"{role} {surface!r} of term {term!r} is ambiguous: it "
                      f"is also a {previous_role} of term {previous_term!r}. "
                      "An alias must name exactly one canonical term")
            if previous_metadata != metadata:
                _fail(path, kind,
                      f"{role} {surface!r} of term {term!r} is ambiguous: it "
                      f"is also a form of term {previous_term!r} with an "
                      "incompatible definition")
            # Identical form and identical metadata: harmless overlap.
            return

        register(term, "term")
        base = _Entry(tokens=tuple(term_keys), gaps=tuple(term_gaps),
                      rank=_RANK_TERM, kind="term", rule="technical-term",
                      message="", count_as_one=count_as_one, pos=pos,
                      category=category, prefix=term_prefix, suffix=term_suffix)
        entries.append(base)

        for form in forms:
            register(form, "form")
            form_keys, form_gaps, form_prefix, form_suffix = _phrase_parts(form)
            entries.append(replace(base, tokens=tuple(form_keys),
                                   gaps=tuple(form_gaps), prefix=form_prefix, suffix=form_suffix))

        for alias in aliases:
            register(alias, "alias")
            alias_keys, alias_gaps, alias_prefix, alias_suffix = _phrase_parts(alias)
            entries.append(_Entry(
                tokens=tuple(alias_keys), gaps=tuple(alias_gaps),
                rank=_RANK_ALIAS, kind="alias", rule="technical-term",
                prefix=alias_prefix, suffix=alias_suffix,
                message=(f"Noncanonical technical term {alias!r}. Use the "
                         f"approved project term {term!r}.")))

    return entries


def _build_index(entries):
    index = {}
    for entry in entries:
        index.setdefault(entry.tokens[0], []).append(entry)
    for bucket in index.values():
        bucket.sort(key=lambda entry: (-len(entry.tokens), -entry.rank))
    return index


def _entry_matches(text, tokens, start, entry):
    count = len(entry.tokens)
    if start + count > len(tokens):
        return False
    first = tokens[start].start
    last = tokens[start + count - 1].end
    prefix_start = first - len(entry.prefix)
    if prefix_start < 0 or text[prefix_start:first] != entry.prefix:
        return False
    if entry.prefix and prefix_start and text[prefix_start - 1].isalnum():
        return False
    end = last + len(entry.suffix)
    if text[last:end] != entry.suffix:
        return False
    # "C++" must not approve the identifier "C++17", "C++_17", or "C++-17".
    if entry.suffix and end < len(text) and (text[end].isalnum() or text[end] in "_-"):
        return False
    for offset, expected in enumerate(entry.tokens):
        token = tokens[start + offset]
        if token.key != expected:
            return False
        if not offset:
            continue
        gap = text[tokens[start + offset - 1].end:token.start]
        configured = entry.gaps[offset - 1]
        if configured.strip():
            if gap != configured:
                return False
        elif not _is_soft_separator(gap):
            return False
    return True


def _entry_surface(entry):
    """Rebuild an entry surface from its tokens, gaps, prefix, and suffix."""
    parts = [entry.prefix]
    for index, token in enumerate(entry.tokens):
        if index:
            parts.append(entry.gaps[index - 1])
        parts.append(token)
    parts.append(entry.suffix)
    return "".join(parts)


def _check_terminology_collisions(dictionary_entries, terminology_entries, path):
    """Reject project terms that override an approved dictionary surface.

    Qualified project terminology may extend the dictionary, but it may not
    replace an approved word. The caller needs a different term or must resolve
    the conflict with the terminology owner.
    """
    approved = {_surface_key(_entry_surface(entry))
                for entry in dictionary_entries if entry.kind == "approved"}
    for entry in terminology_entries:
        surface = _entry_surface(entry)
        if _surface_key(surface) in approved:
            _fail(path, "terminology",
                  f"term, form, or alias {surface!r} collides with an approved "
                  "dictionary entry; project terminology may override only a "
                  "non-approved dictionary surface")


def _include_quantity(text, start):
    """Extend START to a numeric quantity joined by exactly one ASCII space."""
    match = _QUANTITY_BEFORE_UNIT.search(text[:start])
    if match is None:
        return start
    return match.start()


class Vocabulary:
    """Surface vocabulary from an optional STE dictionary and terminology.

    Both paths are optional. A supplied path must be readable UTF-8 JSON that
    validates against the documented schema, or the constructor raises
    ValueError with the path and a corrective next step. An absent dictionary
    suppresses unknown-word findings; it is never treated as an empty approved
    vocabulary.
    """

    def __init__(self, dictionary_path=None, terminology_path=None):
        self.dictionary_loaded = False
        self.terminology_loaded = False
        dictionary_entries, terminology_entries = [], []

        if dictionary_path is not None:
            data = _read_json(dictionary_path, "dictionary")
            dictionary_entries = _dictionary_entries(data, dictionary_path)
            self.dictionary_loaded = True

        if terminology_path is not None:
            data = _read_json(terminology_path, "terminology")
            terminology_entries = _terminology_entries(data, terminology_path)
            self.terminology_loaded = True

        if dictionary_entries and terminology_entries:
            _check_terminology_collisions(
                dictionary_entries, terminology_entries, terminology_path)
        self._index = _build_index(dictionary_entries + terminology_entries)


    def _walk(self, text):
        """Yield (start, end, entry_or_None) for non-overlapping matches.

        Longest whole-token match wins. Unknown single tokens yield None only
        when a dictionary is loaded and the token contains a letter.
        """
        tokens = _tokenize(text)
        index = 0
        while index < len(tokens):
            best = None
            for entry in self._index.get(tokens[index].key, ()):
                if not _entry_matches(text, tokens, index, entry):
                    continue
                rank = (len(entry.tokens), len(entry.prefix) + len(entry.suffix), entry.rank)
                if best is None or rank > best[0]:
                    best = (rank, entry)
            if best is not None:
                entry = best[1]
                start = tokens[index].start - len(entry.prefix)
                end = tokens[index + len(entry.tokens) - 1].end + len(entry.suffix)
                yield start, end, entry
                index += len(entry.tokens)
                continue
            token = tokens[index]
            if self.dictionary_loaded and any(char.isalpha()
                                              for char in token.text):
                yield token.start, token.end, None
            index += 1

    def scan(self, text):
        """Return assisted surface findings; callers still require review."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        findings = []
        for start, end, entry in self._walk(text):
            match = text[start:end]
            if entry is None:
                findings.append({
                    "start": start, "end": end,
                    "rule": "dictionary-word", "level": LEVEL,
                    "match": match,
                    "message": _UNKNOWN_MESSAGE.format(surface=match)})
            elif entry.kind in ("unapproved", "alias"):
                findings.append({
                    "start": start, "end": end,
                    "rule": entry.rule, "level": LEVEL,
                    "match": match, "message": entry.message})
        return findings

    def spans(self, text):
        """Return approved technical-noun spans explicitly marked count_as_one.

        These spans let a caller count a multiword identifier, name, title,
        label, or unit as one word under Rule 8.6. Glossary nouns and verbs
        default to count_as_one false and are not returned. A category-9 noun
        with count_as_one true may include one numeric quantity directly before
        the term, joined by a single ASCII space ("10 kg", "10 degrees
        Celsius"). That grouping is explicit configuration, not unit
        inference; the unit term itself must still match the glossary.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        spans = []
        previous_end = 0
        for start, end, entry in self._walk(text):
            if (entry is None or entry.kind != "term"
                    or not entry.count_as_one):
                previous_end = end
                continue
            if entry.pos == "n" and entry.category == _UNIT_CATEGORY:
                extended = _include_quantity(text, start)
                # Do not extend into an earlier matched term (for example,
                # "Sensor 10" before "10 degrees Celsius").
                if extended >= previous_end:
                    start = extended
            spans.append((start, end))
            previous_end = end
        return spans
