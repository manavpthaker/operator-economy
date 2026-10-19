#!/usr/bin/env python3
"""Validate the standalone-answer contract for Operator Economy Shorts.

The validator serves two callers:

* ``eval_package.py`` validates generated publication briefs. Those briefs
  require a pinned comment in addition to the editorial contract.
* Net-new script-lock manifests can be checked directly from the command
  line. A script lock does not require publication metadata.

The gate validates declared fields and exact-copy relationships. It cannot
prove that a cold viewer will find the answer useful; that remains a human
isolation review against the playable Short.

Usage:
    python3 shorts_contract.py path/to/manifest.json
    python3 shorts_contract.py path/to/shorts_briefs.json --mode derived
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


EPISODE_CTA_RE = re.compile(
    r"\b(?:watch|tap|click|open|visit|see|go\s+to)\b[^.!?]{0,80}"
    r"\b(?:episode|video|breakdown|link|channel|ep\d{3})\b|"
    r"\b(?:full|related)\s+(?:episode|video|breakdown)\b|"
    r"\b(?:episode|video|ep\d{3})\b[^.!?]{0,60}"
    r"\b(?:shows?|explains?|reveals?|covers?|answers?|builds?|tests?)\b|"
    r"\blink\s+(?:in|below|under)\b",
    re.IGNORECASE,
)
DEFERRED_ANSWER_RE = re.compile(
    r"\b(?:find out|learn how|see how|watch to|for the answer|the answer|"
    r"full answer|complete answer|rest of the answer|missing answer|"
    r"for the conclusion|the conclusion)\b",
    re.IGNORECASE,
)
PIN_ROUTE_RE = re.compile(
    r"\b(?:full|episode|video|breakdown|link|ep[\s-]?\d{1,3})\b",
    re.IGNORECASE,
)
STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "for", "and", "you", "your", "is", "it",
}
SUPPORTED_LIST_KEYS = ("shorts_briefs", "scripts")


@dataclass(frozen=True)
class ContractIssue:
    code: str
    message: str
    index: int | None = None
    field: str | None = None

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.index is not None:
            out["index"] = self.index
        if self.field is not None:
            out["field"] = self.field
        return out


@dataclass(frozen=True)
class ContractResult:
    source_kind: str
    record_count: int
    require_pinned_comment: bool
    issues: tuple[ContractIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    def issues_for(self, *codes: str) -> list[ContractIssue]:
        wanted = set(codes)
        return [issue for issue in self.issues if issue.code in wanted]

    def indices_for(self, *codes: str) -> list[int]:
        return sorted({
            issue.index for issue in self.issues_for(*codes)
            if issue.index is not None
        })

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.ok,
            "source_kind": self.source_kind,
            "record_count": self.record_count,
            "require_pinned_comment": self.require_pinned_comment,
            "issues": [issue.as_dict() for issue in self.issues],
        }


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _contract_text(value: Any) -> str:
    """Normalize only case and whitespace for exact-copy phrase checks."""
    text = unicodedata.normalize("NFKC", _text(value))
    return re.sub(r"\s+", " ", text).strip().casefold()


def _content_words(value: Any) -> set[str]:
    text = _contract_text(value)
    return {word.strip(".,!?()'\"") for word in text.split()} - STOPWORDS


def _extension_issue(payoff: Any, extension: Any) -> str | None:
    """Return why optional episode depth is not additive, or ``None``."""
    ext = _contract_text(extension)
    if not ext:
        return None

    pay = _contract_text(payoff)
    if ext == pay or (pay and (ext in pay or pay in ext)):
        return "duplicates the standalone payoff"
    if DEFERRED_ANSWER_RE.search(ext):
        return "withholds the Short's answer for the episode"

    pay_words = _content_words(pay)
    ext_words = _content_words(ext)
    if pay_words and ext_words:
        overlap = len(pay_words & ext_words) / min(len(pay_words), len(ext_words))
        if overlap >= 0.8:
            return "substantially repeats the standalone payoff"
    return None


def _manifest_context(payload: dict[str, Any]) -> tuple[str, list[ContractIssue]]:
    issues: list[ContractIssue] = []
    contract = payload.get("standalone_contract")
    if contract is None:
        return "", issues
    if not isinstance(contract, dict):
        issues.append(ContractIssue(
            "malformed_standalone_contract",
            "standalone_contract must be an object when present",
        ))
        return "", issues
    context = _text(contract.get("context_rule"))
    if context and EPISODE_CTA_RE.search(context):
        issues.append(ContractIssue(
            "invalid_cold_viewer_context",
            "manifest context_rule is an episode route rather than topic context",
            field="standalone_contract.context_rule",
        ))
    return context, issues


def _extract_records(
    payload: Any,
    mode: str,
) -> tuple[list[Any], str, str, list[ContractIssue]]:
    """Return records, source kind, manifest context, and shape issues."""
    issues: list[ContractIssue] = []
    manifest_context = ""

    if isinstance(payload, list):
        source_kind = "direct" if mode == "auto" else mode
        return payload, source_kind, manifest_context, issues

    if not isinstance(payload, dict):
        issues.append(ContractIssue(
            "malformed_container",
            "Shorts contract must be a list or an object containing shorts_briefs or scripts",
        ))
        return [], "unknown", manifest_context, issues

    keys = [key for key in SUPPORTED_LIST_KEYS if key in payload]
    if not keys:
        issues.append(ContractIssue(
            "malformed_container",
            "object must contain exactly one supported list: shorts_briefs or scripts",
        ))
        return [], "unknown", manifest_context, issues
    if len(keys) > 1:
        issues.append(ContractIssue(
            "ambiguous_container",
            "object contains both shorts_briefs and scripts",
        ))
        return [], "unknown", manifest_context, issues

    key = keys[0]
    records = payload.get(key)
    inferred = "derived" if key == "shorts_briefs" else "direct"
    source_kind = inferred if mode == "auto" else mode
    if not isinstance(records, list):
        issues.append(ContractIssue(
            "malformed_records",
            f"{key} must be a list",
            field=key,
        ))
        records = []

    manifest_context, context_issues = _manifest_context(payload)
    issues.extend(context_issues)
    return records, source_kind, manifest_context, issues


def _append_missing(
    issues: list[ContractIssue],
    code: str,
    field: str,
    index: int,
) -> None:
    issues.append(ContractIssue(code, f"missing required {field}", index=index, field=field))


def _phrase_position(
    spoken: str,
    phrase: str,
    field: str,
    index: int,
    issues: list[ContractIssue],
    *,
    from_end: bool = False,
) -> int | None:
    if not phrase:
        return None
    position = spoken.rfind(phrase) if from_end else spoken.find(phrase)
    if position < 0:
        issues.append(ContractIssue(
            "phrase_not_in_spoken_copy",
            f"{field} does not occur in spoken_copy",
            index=index,
            field=field,
        ))
        return None
    return position


def validate_payload(
    payload: Any,
    *,
    mode: str = "auto",
    require_pinned_comment: bool | None = None,
) -> ContractResult:
    """Validate a list, ``shorts_briefs`` object, or ``scripts`` manifest.

    ``mode='auto'`` treats ``shorts_briefs`` as derived publication briefs and
    ``scripts`` or a top-level list as a direct script contract. Callers may
    override that inference. Derived records require per-record
    ``cold_viewer_context`` and pinned-comment routing metadata. Direct
    manifests may satisfy context through their top-level
    ``standalone_contract.context_rule`` and never require a pinned comment.
    """
    if mode not in {"auto", "direct", "derived"}:
        raise ValueError("mode must be auto, direct, or derived")

    records, source_kind, manifest_context, shape_issues = _extract_records(payload, mode)
    require_pin = (
        source_kind == "derived"
        if require_pinned_comment is None
        else bool(require_pinned_comment)
    )
    issues = list(shape_issues)

    if not shape_issues and not records:
        issues.append(ContractIssue("empty_records", "Shorts list must not be empty"))

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            issues.append(ContractIssue(
                "malformed_record",
                "each Short must be an object",
                index=index,
            ))
            continue

        hook = _text(record.get("hook_line"))
        context = _text(record.get("cold_viewer_context"))
        payoff_line = _text(record.get("payoff_line"))
        standalone_payoff = _text(record.get("standalone_payoff"))
        closing_line = _text(record.get("closing_line"))
        last_line = _text(record.get("last_line"))
        terminal_field = "closing_line" if closing_line else "last_line"
        terminal = closing_line or last_line
        episode_extension = _text(record.get("episode_extension"))
        episode_bridge = _text(record.get("episode_bridge_line"))
        pinned_comment = _text(record.get("pinned_comment"))

        if not hook:
            _append_missing(issues, "missing_hook_line", "hook_line", index)

        # Publication briefs must carry their own context. Direct manifests
        # may state the shared context rule once at the top level.
        effective_context = context if context else (
            manifest_context if source_kind == "direct" else ""
        )
        if not effective_context:
            _append_missing(
                issues,
                "missing_cold_viewer_context",
                "cold_viewer_context",
                index,
            )
        elif EPISODE_CTA_RE.search(effective_context):
            issues.append(ContractIssue(
                "invalid_cold_viewer_context",
                "cold-viewer context is an episode route rather than topic context",
                index=index,
                field=(
                    "cold_viewer_context"
                    if context else "standalone_contract.context_rule"
                ),
            ))

        if source_kind == "direct" and not payoff_line:
            _append_missing(issues, "missing_payoff_line", "payoff_line", index)
        if not terminal:
            # cliffhanger_line is intentionally never consulted here.
            issues.append(ContractIssue(
                "missing_terminal_line",
                "missing required closing_line or last_line",
                index=index,
                field="closing_line|last_line",
            ))
        if not standalone_payoff:
            _append_missing(
                issues,
                "missing_standalone_payoff",
                "standalone_payoff",
                index,
            )
        elif EPISODE_CTA_RE.search(standalone_payoff):
            issues.append(ContractIssue(
                "cta_standalone_payoff",
                "standalone_payoff defers value to an episode or link",
                index=index,
                field="standalone_payoff",
            ))

        extension_issue = _extension_issue(standalone_payoff, episode_extension)
        if extension_issue:
            issues.append(ContractIssue(
                "invalid_episode_extension",
                extension_issue,
                index=index,
                field="episode_extension",
            ))
        bridge_issue = _extension_issue(standalone_payoff, episode_bridge)
        if bridge_issue:
            issues.append(ContractIssue(
                "invalid_episode_bridge",
                bridge_issue,
                index=index,
                field="episode_bridge_line",
            ))

        if require_pin:
            if not pinned_comment:
                _append_missing(
                    issues,
                    "missing_pinned_comment",
                    "pinned_comment",
                    index,
                )
            elif not PIN_ROUTE_RE.search(pinned_comment):
                issues.append(ContractIssue(
                    "invalid_pinned_comment",
                    "pinned_comment does not identify long-form routing",
                    index=index,
                    field="pinned_comment",
                ))

        spoken_raw = record.get("spoken_copy")
        if spoken_raw is not None and not isinstance(spoken_raw, str):
            issues.append(ContractIssue(
                "invalid_spoken_copy",
                "spoken_copy must be a string when present",
                index=index,
                field="spoken_copy",
            ))
            continue
        spoken = _contract_text(spoken_raw)
        if not spoken:
            continue

        hook_pos = _phrase_position(
            spoken, _contract_text(hook), "hook_line", index, issues
        )
        payoff_pos = _phrase_position(
            spoken, _contract_text(payoff_line), "payoff_line", index, issues
        ) if payoff_line else None
        terminal_pos = _phrase_position(
            spoken,
            _contract_text(terminal),
            terminal_field,
            index,
            issues,
            from_end=True,
        )
        bridge_pos = _phrase_position(
            spoken,
            _contract_text(episode_bridge),
            "episode_bridge_line",
            index,
            issues,
        ) if episode_bridge else None

        if hook_pos is not None and payoff_pos is not None and hook_pos > payoff_pos:
            issues.append(ContractIssue(
                "hook_after_payoff",
                "hook_line occurs after payoff_line in spoken_copy",
                index=index,
                field="hook_line",
            ))
        if payoff_pos is not None and terminal_pos is not None and payoff_pos > terminal_pos:
            issues.append(ContractIssue(
                "payoff_after_terminal",
                "payoff_line occurs after the terminal anchor in spoken_copy",
                index=index,
                field="payoff_line",
            ))
        if payoff_pos is not None and bridge_pos is not None and payoff_pos >= bridge_pos:
            issues.append(ContractIssue(
                "episode_bridge_before_payoff",
                "episode_bridge_line must occur after payoff_line",
                index=index,
                field="episode_bridge_line",
            ))
        if bridge_pos is not None and terminal_pos is not None and bridge_pos > terminal_pos:
            issues.append(ContractIssue(
                "episode_bridge_after_terminal",
                "episode_bridge_line occurs after the terminal anchor",
                index=index,
                field="episode_bridge_line",
            ))

    return ContractResult(
        source_kind=source_kind,
        record_count=len(records),
        require_pinned_comment=require_pin,
        issues=tuple(issues),
    )


def _format_issue(issue: ContractIssue) -> str:
    location = ""
    if issue.index is not None:
        location = f"short[{issue.index}]"
    if issue.field:
        location = f"{location}.{issue.field}" if location else issue.field
    return f"{location + ': ' if location else ''}{issue.code} — {issue.message}"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the OE standalone Shorts contract")
    parser.add_argument("manifest", help="JSON list or object with shorts_briefs/scripts")
    parser.add_argument("--mode", choices=("auto", "direct", "derived"), default="auto")
    parser.add_argument(
        "--require-pinned-comment",
        action="store_true",
        default=None,
        help="require publication routing metadata regardless of inferred mode",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args(list(argv) if argv is not None else None)

    path = Path(args.manifest)
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        result = ContractResult(
            source_kind="unknown",
            record_count=0,
            require_pinned_comment=bool(args.require_pinned_comment),
            issues=(ContractIssue("unreadable_manifest", str(exc)),),
        )
    else:
        result = validate_payload(
            payload,
            mode=args.mode,
            require_pinned_comment=args.require_pinned_comment,
        )

    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    elif result.ok:
        print(
            f"SHORTS CONTRACT: PASS — {result.record_count} "
            f"{result.source_kind} record(s)"
        )
    else:
        print(
            f"SHORTS CONTRACT: FAIL — {len(result.issues)} issue(s) across "
            f"{result.record_count} {result.source_kind} record(s)"
        )
        for issue in result.issues:
            print(f"  - {_format_issue(issue)}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
