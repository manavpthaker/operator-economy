#!/usr/bin/env python3
"""Root-owned, EP006-specific visual-plan authorship compiler.

The creative mapping below is explicit. The script reads only the locked upstream
script and word transcript to align those decisions to exact word ranges. It is
not part of the shared runtime and does not infer layouts from narration text.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from blueprint_cinema.hashes import sha256_file, write_json_atomic


EPISODE_PATH = Path(__file__).resolve().parent
BLUEPRINT_ROOT = EPISODE_PATH.parents[1]
REPO_ROOT = BLUEPRINT_ROOT.parent
UPSTREAM = REPO_ROOT / "studio" / "originate" / "direct-booking-recovery"


def action(
    motion: str,
    description: str,
    focus: str,
    after: str,
    *,
    mode: str | None = None,
    evidence: tuple[str, ...] = (),
    tickets: tuple[str, ...] = (),
    updates: dict[str, str] | None = None,
) -> dict:
    return {
        "motion": motion,
        "description": description,
        "focus": focus,
        "after": after,
        "mode": mode,
        "evidence": list(evidence),
        "tickets": list(tickets),
        "updates": updates or {focus: after},
    }


BEAT_PLANS = [
    # hook 1
    {
        "section": "hook", "beat": 1, "state": "tension", "mode": "reality", "camera": "camera-human",
        "actions": [
            action("welcome", "Establish one specific guest completing a physical stay at the independent inn.", "stay-key-tag", "active", tickets=("ticket-inn-reality",)),
            action("inspect", "Open the exact vendor-source ticket for the spoken OTA-share claim without inventing source text.", "ota-booking-gate", "active", mode="proof", evidence=("evidence-ota-share",), tickets=("ticket-cloudbeds-source",)),
            action("route", "Route the same stay token back toward the useful paid gate to expose the relationship leak.", "relationship-leak-state", "active", mode="system"),
            action("audit", "Reveal the counter-system by opening the direct-path audit before any outreach can begin.", "direct-path-audit", "active", mode="system", tickets=("ticket-direct-path-test",)),
        ],
    },
    # thesis 1-3
    {
        "section": "thesis", "beat": 1, "state": "current_machine", "mode": "system", "camera": "camera-system",
        "actions": [
            action("establish", "Establish the OTA gate as useful acquisition rather than a villain or removable dependency.", "ota-booking-gate", "active"),
            action("book", "Complete the first booking through the OTA path and preserve its discovery job.", "first-booking-money-flow", "active"),
            action("welcome", "Carry the acquired guest through a capable, human hotel stay.", "hotel-stay-node", "active", mode="reality", tickets=("ticket-inn-reality",)),
            action("remember", "Hold the completed stay as a physical token without treating it as permissioned memory.", "stay-key-tag", "active", mode="reality"),
            action("route", "Show the unresolved return falling toward the paid gate while the property lacks a relationship path.", "relationship-leak-state", "failed"),
            action("recover", "Preview the bounded recovered loop while keeping every gate visibly closed.", "recovered-loop-state", "active"),
        ],
    },
    {
        "section": "thesis", "beat": 2, "state": "current_machine", "mode": "system", "camera": "camera-system",
        "actions": [
            action("inspect", "Inspect fragmented ownership across discovery, website, phone, booking, and post-stay work.", "independent-hotel-operator", "active"),
            action("route", "Route guest work between disconnected handoffs and expose the absence of one accountable owner.", "system-zone", "active"),
            action("retry", "Return an unowned handoff to the retry queue instead of hiding the operational failure.", "repair-retry-queue", "active"),
            action("escalate", "Escalate unresolved ownership to the hotel operator as the human control point.", "sensitive-case-escalation", "active"),
            action("measure", "Resolve the current-machine view around one accountable operating journey rather than a website feature.", "independent-hotel-operator", "resolved"),
        ],
    },
    {
        "section": "thesis", "beat": 3, "state": "current_machine", "mode": "system", "camera": "camera-system",
        "actions": [
            action("inspect", "Hold the direct destination closed until a real visitor path reaches and tests it.", "direct-booking-destination", "failed", tickets=("ticket-direct-path-test",)),
            action("audit", "Audit findability, trust, phone, policy, rate, and booking handoffs as one operating job.", "direct-path-audit", "active"),
            action("repair", "Repair the direct path before increasing discovery or post-stay outreach.", "direct-path-repair", "active"),
            action("follow_up", "Keep follow-up dormant behind consent, qualification, suppression, and human review.", "relevant-follow-up", "suppressed"),
            action("measure", "Set direct-booking share as the measurable operating outcome without activating unearned return value.", "return-booking-money-flow", "initial", mode="proof"),
        ],
    },
    # evidence 1-7
    {
        "section": "evidence", "beat": 1, "state": "proof", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Present a neutral source ticket with publisher and vendor-interest caveat intact.", "proof-zone", "active", evidence=("evidence-ota-share",), tickets=("ticket-cloudbeds-source",)),
            action("measure", "Pin the vendor-published OTA share parameter to the useful booking gate.", "ota-booking-gate", "active", evidence=("evidence-ota-share",)),
            action("route", "Apply the sourced parameter to the first-booking flow without changing the editorial caveat.", "first-booking-money-flow", "active", evidence=("evidence-ota-share",)),
            action("resolve", "Retain the source pin beside the system after the parameter changes its visible weight.", "proof-zone", "resolved", evidence=("evidence-ota-share",)),
        ],
    },
    {
        "section": "evidence", "beat": 2, "state": "proof", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Separate base commission from optional visibility and loyalty additions on the operator ledger.", "ota-settlement-ledger", "active", evidence=("evidence-commission-model",), tickets=("ticket-settlement-ledger",)),
            action("measure", "Route the first booking through the commission line while keeping the acquired stay intact.", "first-booking-money-flow", "active", evidence=("evidence-commission-model",)),
            action("compare", "Compare the platform audience and checkout job with the operator-side economic consequence.", "ota-booking-gate", "resolved", evidence=("evidence-commission-model",)),
            action("approve", "Mark the first-booking trade as potentially reasonable for a small hotel without a marketing team.", "independent-hotel-operator", "active", mode="reality"),
            action("resolve", "Leave the commission source attached to the ledger rather than converting it into a guest receipt.", "ota-settlement-ledger", "resolved", evidence=("evidence-commission-model",)),
        ],
    },
    {
        "section": "evidence", "beat": 3, "state": "proof", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Pin the vendor-published cancellation comparison beside the first-booking flow.", "proof-zone", "active", evidence=("evidence-cancellation-gap",), tickets=("ticket-cloudbeds-source",)),
            action("compare", "Compare OTA and direct cancellation parameters without turning the platform into an enemy.", "ota-settlement-ledger", "active", evidence=("evidence-cancellation-gap",)),
            action("measure", "Expose shakier reservation reliability as a separate operator-side risk from commission.", "ota-settlement-ledger", "failed", evidence=("evidence-cancellation-gap",)),
            action("resolve", "Return the decision to the operator with dependence fully costed rather than moralized.", "independent-hotel-operator", "resolved", mode="reality"),
        ],
    },
    {
        "section": "evidence", "beat": 4, "state": "proof", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("establish", "Establish the illustrative hotel model as assumptions rather than a reported property result.", "proof-zone", "active", evidence=("evidence-commission-model",)),
            action("measure", "Run rooms and occupancy through the first-booking money flow as a visible model.", "first-booking-money-flow", "active", evidence=("evidence-commission-model",)),
            action("compare", "Apply average rate and OTA share while retaining every assumption beside the model.", "ota-settlement-ledger", "active", evidence=("evidence-commission-model",)),
            action("measure", "Apply the low-twenties commission range and expose the illustrative annual consequence.", "ota-settlement-ledger", "resolved", evidence=("evidence-commission-model",)),
            action("audit", "Return the model to a blank operator field that demands the property's real numbers.", "direct-path-audit", "active", mode="system"),
        ],
    },
    {
        "section": "evidence", "beat": 5, "state": "current_machine", "mode": "system", "camera": "camera-system",
        "actions": [
            action("discover", "Run global discovery, comparison, translation, marketing, and checkout through the useful OTA gate.", "ota-booking-gate", "active", tickets=("ticket-ota-market-force",)),
            action("book", "Complete the first reservation and preserve the platform's legitimate acquisition job.", "hotel-stay-node", "active"),
            action("welcome", "Let the property deliver the stay and create a physical human relationship moment.", "stay-key-tag", "active", mode="reality", tickets=("ticket-inn-reality",)),
            action("suppress", "Keep follow-up inactive by recording that permission and relevance have not been established.", "suppression-register", "suppressed"),
            action("route", "Expose the missed post-stay opportunity as a relationship leak rather than an acquisition failure.", "relationship-leak-state", "active"),
        ],
    },
    {
        "section": "evidence", "beat": 6, "state": "current_machine", "mode": "reality", "camera": "camera-human",
        "actions": [
            action("establish", "Establish the recurring operator inside a working inn rather than a corporate marketing office.", "independent-hotel-operator", "active", evidence=("evidence-operator-history",), tickets=("ticket-inn-reality",)),
            action("route", "Route social, site, phone, reservation, and check-in through one guest journey.", "hotel-stay-node", "active"),
            action("fail", "Let a broken direct-path handoff enter its declared failed state instead of receiving cosmetic polish.", "direct-path-repair", "failed", mode="system"),
            action("retry", "Route that declared repair failure into the retry queue with the operator still accountable.", "repair-retry-queue", "active", mode="system"),
            action("review", "Make the operator's time and judgment the scarce coordination layer across the path.", "human-review-gate", "active", mode="system", evidence=("evidence-operator-history",), tickets=("ticket-human-review",)),
            action("escalate", "Expose the small innkeeper's capacity limit and assign an accountable exception route.", "independent-hotel-operator", "failed"),
            action("resolve", "Resolve the operator role as maintaining the whole path rather than supplying another idea.", "independent-hotel-operator", "resolved"),
        ],
    },
    {
        "section": "evidence", "beat": 7, "state": "proof", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Open a neutral proof ticket for the hospitality-software investment claim without generated source text.", "proof-zone", "active", tickets=("ticket-mews-source",)),
            action("measure", "Pin investment scale to the system zone as evidence that tooling is improving, not that this service is guaranteed.", "system-zone", "active", tickets=("ticket-mews-source",)),
            action("compare", "Compare powerful software with the unowned work of understanding one property's guest journey.", "independent-hotel-operator", "active", mode="reality"),
            action("route", "Route software capability toward audit and repair while leaving judgment outside automation.", "direct-path-audit", "active", mode="system"),
            action("review", "Hold consent, voice, exceptions, and guest relationship at the mandatory human gate.", "human-review-gate", "active", mode="system", tickets=("ticket-human-review",)),
            action("resolve", "Pull back to the counter-system as an offer built from accountable jobs rather than logos.", "system-zone", "resolved", mode="reset"),
            action("establish", "Reset attention on the operator's jobs before the counter-system is assembled in detail.", "independent-hotel-operator", "active", mode="reality"),
        ],
    },
    # stack 1-5
    {
        "section": "stack", "beat": 1, "state": "counter_system", "mode": "system", "camera": "camera-system",
        "actions": [
            action("audit", "Audit the property's current discovery surfaces before selecting or naming any tools.", "direct-path-audit", "active"),
            action("repair", "Repair stale property information and offers so existing interest has a credible destination.", "direct-path-repair", "active"),
            action("discover", "Route current search interest toward the repaired hotel path without promising fame.", "market-discovery", "active"),
            action("review", "Assign photography, descriptions, and offers to accountable human review.", "human-review-gate", "active", tickets=("ticket-human-review",)),
            action("measure", "Resolve findability as a maintained operating job with a visible baseline.", "direct-path-audit", "resolved"),
        ],
    },
    {
        "section": "stack", "beat": 2, "state": "counter_system", "mode": "system", "camera": "camera-system",
        "actions": [
            action("reset", "Start a bounded direct-path retest cycle with audit, repair, destination, and retry states reopened.", "direct-path-audit", "initial", mode="reset", updates={"direct-path-audit": "initial", "direct-path-repair": "initial", "direct-booking-destination": "initial", "repair-retry-queue": "initial"}),
            action("audit", "Complete the rate, mobile booking, cancellation-term, and after-hours call audit as a guest would.", "direct-path-audit", "resolved", tickets=("ticket-direct-path-test",)),
            action("compare", "Expose the failed direct destination against the OTA path while keeping the same guest intent visible.", "direct-booking-destination", "failed"),
            action("repair", "Repair the booking and call handoff independent of which low-level tool supplies it.", "direct-path-repair", "active"),
            action("fail", "Let the first retest fail visibly instead of turning on outreach.", "direct-path-repair", "failed"),
            action("retry", "Assign the failed retest to the declared retry queue.", "repair-retry-queue", "active"),
            action("repair", "Resolve the repair only after the retry passes the same guest-side test.", "direct-path-repair", "resolved"),
            action("resolve", "Resolve the direct destination only after the full handoff passes.", "direct-booking-destination", "resolved"),
        ],
    },
    {
        "section": "stack", "beat": 3, "state": "counter_system", "mode": "system", "camera": "camera-system",
        "actions": [
            action("request_permission", "Request affirmative permission after checkout without converting the key tag into memory yet.", "permission-gate", "active", tickets=("ticket-permission-handoff",)),
            action("approve", "Record affirmative consent as a resolved gate before any guest-memory object can exist.", "permission-gate", "resolved", tickets=("ticket-permission-handoff",)),
            action("recognize", "Resolve the physical stay token into minimal permissioned context only after consent.", "guest-memory-context", "active"),
            action("remember", "Keep only enough context to make a thank-you, review request, or return reason useful.", "guest-memory-context", "resolved"),
            action("review", "Send automated drafts through human hospitality judgment before any outbound message.", "human-review-gate", "active", tickets=("ticket-human-review",)),
        ],
    },
    {
        "section": "stack", "beat": 4, "state": "stress_test", "mode": "system", "camera": "camera-system",
        "actions": [
            action("reset", "Open a separate sensitive-case stress branch with outbound controls closed.", "return-qualification-gate", "initial", mode="reset", updates={"return-qualification-gate": "initial", "suppression-register": "initial", "sensitive-case-escalation": "initial", "human-review-gate": "initial"}),
            action("review", "Review voice, offer, timing, and context at the mandatory human gate.", "human-review-gate", "active", tickets=("ticket-human-review",)),
            action("suppress", "Put an irrelevant or sensitive return through the qualification gate's declared suppressed state.", "return-qualification-gate", "suppressed"),
            action("suppress", "Route that ineligible branch into the suppression register before any message exists.", "suppression-register", "suppressed"),
            action("escalate", "Escalate ambiguous and sensitive cases instead of allowing automatic judgment.", "sensitive-case-escalation", "active"),
            action("suppress", "Stop the sensitive branch at the human gate rather than returning it to outbound.", "human-review-gate", "suppressed"),
            action("resolve", "Record the human disposition on the escalated branch with outbound still stopped.", "sensitive-case-escalation", "resolved"),
        ],
    },
    {
        "section": "stack", "beat": 5, "state": "counter_system", "mode": "system", "camera": "camera-system",
        "actions": [
            action("discover", "Carry credible discovery into the hotel rather than a slide of vendor logos.", "market-discovery", "resolved"),
            action("audit", "Keep the completed direct-path baseline visible before any eligible return is considered.", "direct-path-audit", "resolved", mode="proof"),
            action("repair", "Keep the tested direct path visibly resolved before the return loop activates.", "direct-path-repair", "resolved", mode="proof"),
            action("qualify", "Return to the eligible branch and resolve its relevant reason and timing before outreach.", "return-qualification-gate", "resolved"),
            action("resolve", "Record a clear suppression disposition for the eligible branch without weakening the stopped branch.", "suppression-register", "resolved"),
            action("approve", "Resolve mandatory human judgment for the eligible branch before any later follow-up.", "human-review-gate", "resolved", tickets=("ticket-human-review",)),
            action("remember", "Carry the permissioned guest context through qualification without broadening its use.", "guest-memory-context", "resolved", mode="proof"),
            action("measure", "Define recovered appropriate returns as the target while leaving unearned return value inactive.", "return-booking-money-flow", "initial", mode="proof"),
        ],
    },
    # playbook 1-6
    {
        "section": "playbook", "beat": 1, "state": "installation", "mode": "system", "camera": "camera-system",
        "actions": [
            action("audit", "Open the engagement with booking mix, commission, cancellations, calls, conversion, repeats, and referrals.", "direct-path-audit", "active"),
            action("measure", "Pin the starting booking mix and commission consequence to the proof bench.", "ota-settlement-ledger", "active", mode="proof", evidence=("evidence-commission-model",)),
            action("inspect", "Trace every guest-relationship break across the existing operating path.", "relationship-leak-state", "active"),
            action("compare", "Preserve a before picture that cannot be replaced later by activity metrics.", "proof-zone", "active", mode="proof"),
            action("resolve", "Deliver the relationship-leak map as the first concrete operator artifact.", "direct-path-audit", "resolved"),
        ],
    },
    {
        "section": "playbook", "beat": 2, "state": "installation", "mode": "system", "camera": "camera-system",
        "actions": [
            action("reset", "Open the installation retest with audit, repair, destination, and retry states closed again.", "direct-path-audit", "initial", mode="reset", updates={"direct-path-audit": "initial", "direct-path-repair": "initial", "direct-booking-destination": "initial", "repair-retry-queue": "initial"}),
            action("audit", "Complete the search, comparison, booking, terms, and phone audit from the guest side.", "direct-path-audit", "resolved", tickets=("ticket-direct-path-test",)),
            action("compare", "Expose rate or policy mismatch at the direct destination before outreach.", "direct-booking-destination", "failed"),
            action("repair", "Repair each failed handoff and assign a real owner.", "direct-path-repair", "active"),
            action("retry", "Retest the repaired path and route any failure back through audit.", "repair-retry-queue", "active"),
            action("repair", "Resolve the repair only after the repeated guest-side path passes.", "direct-path-repair", "resolved"),
            action("resolve", "Activate the direct destination only after the complete guest path passes.", "direct-booking-destination", "resolved"),
        ],
    },
    {
        "section": "playbook", "beat": 3, "state": "installation", "mode": "system", "camera": "camera-system",
        "actions": [
            action("reset", "Start a new eligible-return operating cycle with every outbound gate visibly closed.", "permission-gate", "initial", mode="reset", updates={"permission-gate": "initial", "return-qualification-gate": "initial", "suppression-register": "initial", "human-review-gate": "initial", "relevant-follow-up": "initial"}),
            action("request_permission", "Start with prior guests only when the property has affirmative contact permission.", "permission-gate", "active", tickets=("ticket-permission-handoff",)),
            action("approve", "Resolve affirmative permission before creating memory, qualification, or a message.", "permission-gate", "resolved", tickets=("ticket-permission-handoff",)),
            action("qualify", "Qualify relevance, timing, and reason to return rather than treating the list as an audience.", "return-qualification-gate", "resolved"),
            action("suppress", "Evaluate cold, irrelevant, revoked, and sensitive exclusions before message creation.", "suppression-register", "active"),
            action("resolve", "Record the eligible case as clear only after every suppression rule has been applied.", "suppression-register", "resolved"),
            action("review", "Review the thank-you, review request, return reason, and referral prompt as hospitality.", "human-review-gate", "active", tickets=("ticket-human-review",)),
            action("approve", "Resolve mandatory human approval before the outbound route becomes available.", "human-review-gate", "resolved", tickets=("ticket-human-review",)),
            action("follow_up", "Release only a few relevant, approved messages into the outbound path.", "relevant-follow-up", "resolved"),
        ],
    },
    {
        "section": "playbook", "beat": 4, "state": "installation", "mode": "system", "camera": "camera-system",
        "actions": [
            action("discover", "Widen discovery work only after the direct destination and return controls operate.", "market-discovery", "active"),
            action("welcome", "Show the actual property and guest experience instead of generic travel material.", "hotel-stay-node", "active", mode="reality", tickets=("ticket-inn-reality",)),
            action("review", "Keep review requests, referrals, and automated messages visibly resolved through a responsible person.", "human-review-gate", "resolved", mode="proof"),
            action("route", "Resolve qualified attention toward the already repaired direct booking destination.", "market-discovery", "resolved"),
            action("resolve", "Pull back to the installed audit-and-operation checklist as accumulated system state.", "system-zone", "resolved", mode="reset"),
        ],
    },
    {
        "section": "playbook", "beat": 5, "state": "installation", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Mark the absence of public per-property pricing as an evidence gap rather than inventing a rate.", "proof-zone", "active", tickets=("ticket-provider-pricing-review",)),
            action("compare", "Separate one-time audit and setup work from recurring operating responsibility.", "direct-path-audit", "active", mode="system"),
            action("review", "Assign what the operator manages and what the hotel retains to the human gate.", "human-review-gate", "active", mode="system"),
            action("measure", "Attach the promised reportable outcome to direct-share change without presenting unearned return value.", "return-booking-money-flow", "initial"),
            action("resolve", "Resolve the offer explanation before any buyer conversation or tool choice.", "independent-hotel-operator", "resolved", mode="reality"),
        ],
    },
    {
        "section": "playbook", "beat": 6, "state": "economics", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("measure", "Set direct-booking share before and after as the primary monthly outcome while the model remains unearned.", "return-booking-money-flow", "initial"),
            action("compare", "Use commission, cancellations, calls, conversion, repeats, and reviews only to explain movement.", "ota-settlement-ledger", "active", evidence=("evidence-commission-model", "evidence-cancellation-gap")),
            action("suppress", "Suppress activity-only dashboard signals that do not explain the outcome.", "suppression-register", "suppressed", mode="system"),
            action("audit", "Route a flat direct-share result back into the operating audit instead of decorating the report.", "direct-path-audit", "active", mode="system"),
            action("resolve", "Resolve the scorecard around one accountable outcome and its causal diagnostics.", "proof-zone", "resolved"),
        ],
    },
    # economics 1-5
    {
        "section": "economics", "beat": 1, "state": "economics", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Open the operator commission ledger rather than a promise about operator earnings.", "ota-settlement-ledger", "active", evidence=("evidence-commission-model",), tickets=("ticket-settlement-ledger",)),
            action("measure", "Run the illustrative twenty-room assumptions through first-booking economics.", "first-booking-money-flow", "active", evidence=("evidence-commission-model",)),
            action("compare", "Compare the real cost category with an unknown recoverable share without activating a return.", "return-booking-money-flow", "initial", evidence=("evidence-commission-model",)),
            action("suppress", "Suppress any inference that the full commission bill is recoverable or guaranteed.", "suppression-register", "suppressed", mode="system"),
            action("resolve", "Leave the owner with a real cost to compare and an explicit attribution limit.", "ota-settlement-ledger", "resolved"),
        ],
    },
    {
        "section": "economics", "beat": 2, "state": "economics", "mode": "proof", "camera": "camera-proof",
        "actions": [
            action("inspect", "Pin the salary source in its correct unit and label it as labor evidence, not a client price.", "proof-zone", "active", evidence=("evidence-labor-value",), tickets=("ticket-labor-value-source",)),
            action("measure", "Route the salary range toward human labor value rather than booking revenue.", "independent-hotel-operator", "active", mode="reality", evidence=("evidence-labor-value",)),
            action("compare", "Separate full-time labor value from any per-hotel service price or earnings promise.", "human-review-gate", "active", mode="system", evidence=("evidence-labor-value",)),
            action("resolve", "Retain the evidence caveat beside the operator role after the comparison.", "proof-zone", "resolved", evidence=("evidence-labor-value",)),
        ],
    },
    {
        "section": "economics", "beat": 3, "state": "economics", "mode": "system", "camera": "camera-system",
        "actions": [
            action("review", "Make direction, output review, voice protection, consent, and exception work visible.", "human-review-gate", "active", tickets=("ticket-human-review",)),
            action("measure", "Route software subscriptions separately from operator time and judgment.", "ota-settlement-ledger", "active", mode="proof"),
            action("escalate", "Expose underpriced human support as an operator capacity failure.", "independent-hotel-operator", "failed"),
            action("suppress", "Stop fully automated outreach when it no longer resembles hospitality.", "suppression-register", "suppressed"),
        ],
    },
    {
        "section": "economics", "beat": 4, "state": "stress_test", "mode": "system", "camera": "camera-system",
        "actions": [
            action("measure", "Hold the original baseline while a strong month enters the scorecard.", "proof-zone", "active", mode="proof"),
            action("compare", "Compare seasonality and OTA promotion against the operator's documented changes.", "ota-settlement-ledger", "active", mode="proof"),
            action("audit", "Route unexplained movement back through the audit instead of claiming credit.", "direct-path-audit", "active"),
            action("review", "Require a human explanation of contribution, limits, and fragile assumptions.", "human-review-gate", "active"),
            action("escalate", "Expose renewal risk as an accountable exception when the service cannot explain what changed.", "sensitive-case-escalation", "active"),
            action("resolve", "Resolve renewal around evidence of contribution rather than coincident timing.", "independent-hotel-operator", "resolved"),
        ],
    },
    {
        "section": "economics", "beat": 5, "state": "agency", "mode": "system", "camera": "camera-system",
        "actions": [
            action("reset", "Reset one final eligible-return case while preserving the already audited and repaired direct path.", "recovered-loop-state", "initial", mode="reset", updates={"recovered-loop-state": "initial", "direct-path-audit": "resolved", "direct-path-repair": "resolved", "permission-gate": "initial", "guest-memory-context": "initial", "return-qualification-gate": "initial", "suppression-register": "initial", "human-review-gate": "initial", "relevant-follow-up": "initial", "direct-booking-destination": "initial", "return-booking-money-flow": "initial", "direct-booking-confirmation": "initial"}),
            action("welcome", "Return to the same physical stay token from the opening.", "stay-key-tag", "active", mode="reality", tickets=("ticket-inn-reality",)),
            action("request_permission", "Request permission after checkout while memory and every outbound route remain closed.", "permission-gate", "active", tickets=("ticket-permission-handoff",)),
            action("approve", "Record affirmative permission as resolved before the key tag can become guest memory.", "permission-gate", "resolved", tickets=("ticket-permission-handoff",)),
            action("remember", "Resolve the key tag into minimal guest context after the consent handoff.", "guest-memory-context", "resolved"),
            action("qualify", "Confirm an appropriate reason and timing for this particular return.", "return-qualification-gate", "resolved"),
            action("resolve", "Apply suppression rules and record that this eligible case is clear to continue.", "suppression-register", "resolved"),
            action("review", "Approve relevance and voice at the mandatory human judgment gate.", "human-review-gate", "resolved", tickets=("ticket-human-review",)),
            action("follow_up", "Deliver the restrained approved follow-up only after every outbound gate resolves.", "relevant-follow-up", "resolved"),
            action("route", "Route the appropriate return through the already repaired direct destination.", "direct-booking-destination", "resolved", tickets=("ticket-direct-path-test",)),
            action("measure", "Record the completed return separately as direct value on the operator proof bench.", "return-booking-money-flow", "resolved", mode="proof"),
            action("recover", "Issue the privacy-safe direct confirmation as the visible outcome, separate from commission proof.", "direct-booking-confirmation", "resolved", tickets=("ticket-direct-confirmation",)),
        ],
    },
    # cta 1
    {
        "section": "cta", "beat": 1, "state": "agency", "mode": "reset", "camera": "camera-system",
        "actions": [
            action("reveal", "Pull back to the completed audit, repair, consent, qualification, judgment, and measurement loop.", "recovered-loop-state", "active"),
            action("audit", "Leave the direct-path audit as the first concrete installation move.", "direct-path-audit", "resolved"),
            action("measure", "Hold the monthly direct-share scorecard as the operator's proof of change.", "return-booking-money-flow", "resolved", mode="proof"),
            action("recover", "Preserve the OTA introduction while the appropriate return remains direct.", "recovered-loop-state", "resolved"),
            action("confirm", "End on the privacy-safe direct confirmation outcome and the accountable operator.", "direct-booking-confirmation", "resolved", mode="reality", tickets=("ticket-direct-confirmation",)),
        ],
    },
]


def token_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text))


def main() -> None:
    script = json.loads((UPSTREAM / "script.json").read_text(encoding="utf-8"))
    words = json.loads((UPSTREAM / "vo" / "words.json").read_text(encoding="utf-8"))
    lock = json.loads((EPISODE_PATH / "input-lock.json").read_text(encoding="utf-8"))
    world = json.loads((EPISODE_PATH / "world.json").read_text(encoding="utf-8"))
    engine = json.loads((EPISODE_PATH / "episode-engine.json").read_text(encoding="utf-8"))

    plan_lookup = {(item["section"], item["beat"]): item for item in BEAT_PLANS}
    script_beats = [
        (section["id"], beat["beat"], beat["vo_text"])
        for section in script["sections"]
        for beat in section["beats"]
    ]
    if set(plan_lookup) != {(section, beat) for section, beat, _ in script_beats}:
        raise SystemExit("explicit visual beat map does not exactly cover the locked script beats")

    object_map = {item["id"]: item for item in world["objects"]}
    current_states = {item["id"]: item["initial_state"] for item in world["objects"]}
    grouped_actions: list[tuple[dict, list[int]]] = []
    for section in script["sections"]:
        section_indices = [index for index, word in enumerate(words) if word["section"] == section["id"]]
        if not section_indices:
            raise SystemExit(f"locked transcript has no words for {section['id']}")
        counts = [token_count(beat["vo_text"]) for beat in section["beats"]]
        total_count = sum(counts)
        section_cursor = 0
        for beat_index, beat in enumerate(section["beats"]):
            if beat_index == len(section["beats"]) - 1:
                beat_end = len(section_indices)
            else:
                cumulative = sum(counts[: beat_index + 1])
                beat_end = round(len(section_indices) * cumulative / total_count)
            beat_words = section_indices[section_cursor:beat_end]
            section_cursor = beat_end
            authored = plan_lookup[(section["id"], beat["beat"])]
            actions = authored["actions"]
            if len(beat_words) < len(actions):
                raise SystemExit(f"not enough timed words for {section['id']} beat {beat['beat']}")
            for action_index, authored_action in enumerate(actions):
                start = round(len(beat_words) * action_index / len(actions))
                end = round(len(beat_words) * (action_index + 1) / len(actions))
                indices = beat_words[start:end]
                if not indices:
                    raise SystemExit("authored action received no narration anchor")
                grouped_actions.append((authored | {"action": authored_action}, indices))

    if [index for _, indices in grouped_actions for index in indices] != list(range(len(words))):
        raise SystemExit("authored action allocation does not cover every transcript word exactly once")

    units = []
    previous_out = 0.0
    previous_focus: str | None = None
    camera_for_mode = {
        "reality": "camera-human",
        "system": "camera-system",
        "proof": "camera-proof",
        "reset": "camera-system",
    }
    for unit_index, (authored, indices) in enumerate(grouped_actions, start=1):
        authored_action = authored["action"]
        focus = authored_action["focus"]
        if focus not in object_map:
            raise SystemExit(f"unknown authored focus: {focus}")
        mode = authored_action["mode"] or authored["mode"]
        before_states = []
        after_states = []
        for object_id, requested_after in authored_action["updates"].items():
            if object_id not in object_map:
                raise SystemExit(f"unknown authored update object: {object_id}")
            allowed_states = [state["id"] for state in object_map[object_id]["states"]]
            if requested_after not in allowed_states:
                raise SystemExit(f"invalid authored state {requested_after} for {object_id}")
            before = current_states[object_id]
            after = requested_after
            if mode == "system" and before == after:
                if before in {"active", "suppressed"} and "resolved" in allowed_states:
                    after = "resolved"
                else:
                    raise SystemExit(
                        f"system action does not change {object_id}: "
                        f"{authored['section']} beat {authored['beat']} {authored_action['description']}"
                    )
            before_states.append({"object_id": object_id, "state": before})
            after_states.append({"object_id": object_id, "state": after})
            current_states[object_id] = after
        if unit_index == len(grouped_actions):
            unit_out = float(lock["audio_duration_seconds"])
        else:
            last_word = words[indices[-1]]
            next_word = words[indices[-1] + 1]
            unit_out = round((float(last_word["end"]) + float(next_word["start"])) / 2, 3)
        carry = ["stay-key-tag", "independent-hotel-operator"]
        if previous_focus and previous_focus not in carry:
            carry.append(previous_focus)
        units.append(
            {
                "id": f"unit-{unit_index:03d}",
                "in": round(previous_out, 3),
                "out": unit_out,
                "narration_anchor": {
                    "word_start": indices[0],
                    "word_end": indices[-1],
                    "quote": " ".join(words[index]["word"] for index in indices),
                },
                "sequence_id": f"sequence-{authored['section']}-{authored['beat']:02d}",
                "narrative_state": authored["state"],
                "mode": mode,
                "action": authored_action["description"],
                "motion_verb": authored_action["motion"],
                "carry": carry,
                "focus": [focus],
                "world_state_before": before_states,
                "world_state_after": after_states,
                "camera_anchor": camera_for_mode[mode],
                "evidence_ids": authored_action["evidence"],
                "asset_ticket_ids": authored_action["tickets"],
                "audio_state": {"narration": True, "music": False, "sound_design": False},
                "status": "greybox",
            }
        )
        previous_out = unit_out
        previous_focus = focus

    plan = {
        "$schema": "../../schemas/visual-plan.schema.json",
        "schema_version": "1.0.0",
        "workflow_version": "blueprint-cinema-1.0",
        "episode_number": 6,
        "episode_code": "EP006",
        "slug": "direct-booking-recovery",
        "folder_name": "EP006-direct-booking-recovery",
        "input_lock_sha256": sha256_file(EPISODE_PATH / "input-lock.json"),
        "episode_engine_sha256": sha256_file(EPISODE_PATH / "episode-engine.json"),
        "world_sha256": sha256_file(EPISODE_PATH / "world.json"),
        "audio_duration_seconds": lock["audio_duration_seconds"],
        "units": units,
        "status": "ready_for_approval",
    }
    write_json_atomic(EPISODE_PATH / "visual-plan.json", plan)
    print(f"Authored {len(units)} explicit units across {plan['audio_duration_seconds']:.3f}s")


if __name__ == "__main__":
    main()
