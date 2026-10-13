# Owner decision 2026-10-13: discovery looks for buyers, not sellers

Status: approved owner decision. Recorded 2026-10-13 from the owner's instruction in chat.

Decided by: Manav Thaker (owner)

Owner's words: "make all the changes. the buyer point is important. we're looking for sellers and we
need to look for buyers. even moreso, we need to look for problems that are oppportunities for one
person to solve with AI. especially now, with always on agents, there are so many more opps for
individuals to solve real problems. industries can be big or small because it's not the size if
someone can solve it for a small perentage and build a sustatinable business"

Scope: the candidate scout, the discovery contract, and how the research bench treats missing price
anchors. This decision does **not** edit any locked Step 0.2 file or the Step 0.3 amendment, and does
not change hard gates, scoring, the calibration zone, or owner promotion.

## Why

An audit of the 21 scout runs from 2026-09-20 to 2026-10-13 found:

- about 85 ideas screened, about 62 rejected, 22 leads logged; 5 admitted to Step 0, all 5 parked,
  mostly for no price anchor; no episode came from the scout (EP007 to EP009 came from owner and
  legacy premises);
- ideas came from the scout's own brainstorm and searches were used to confirm or kill them;
  vendor pages are easy to find and buyer conversation (Reddit, groups) is blocked, so searches
  surfaced sellers and rarely buyers;
- the substitute check rejected any idea an AI tool or AI-backed service already sold, which
  conflicts with the AI-change test: once AI makes a job cheap, someone sells a tool for it. About 40
  rejections rested on it;
- the regulatory-trigger route pulled leads toward narrow regulated niches unlike the episodes that
  shipped;
- nine tests accumulated in one week, each added after a failure; and
- scout and bench disagreed on payment evidence.

## Rules

1. **Target.** Problems one person can now solve for buyers with AI, including always-on agents,
   well enough to build a sustainable business. Industry size is not a gate; whether one operator can
   serve enough buyers for a share of the value or a fixed fee is.
2. **Buyers first.** Every scout run builds a buyer-side observation ledger before forming ideas.
   Every lead cites the buyer observation that generated it. Seller material is context only.
3. **Lanes.** Buyer problems, tool-to-service gaps, and always-on agent work supply at least two
   thirds of new leads. Operating changes supply at most one new lead per run and still need a buyer
   observation.
4. **Five tests replace nine:** real buyer and problem, one person with AI (with a unit economics
   sketch), delivery boundary, substitutes, showable fit.
5. **Substitute check rewritten.** A tool sold to buyers is evidence the problem is real. Reject only
   when a done-for-you service delivers the outcome at a price one operator cannot beat and buyers
   readily use it, or buyer-side evidence shows buyers run the tool themselves.
6. **Re-screen.** Ideas rejected 2026-09-20 to 2026-10-13 mainly on the old substitute check, or on
   missing buyer voice while Reddit was blocked, are re-screened, up to two per run.
7. **Cadence.** Scout runs Wednesday and Sunday at 17:00 ET with a deep-pass budget (at least 20
   searches, 6 pages read in full, 15 buyer observations). Supersedes the 2026-09-28 "scout cadence:
   daily" decision.
8. **Price anchors at the bench.** A missing buyer price anchor is not by itself a park reason. The
   bench models price from value at stake or old-way spend, labels it a modeled scenario, and makes
   price the viewer's first test. The gap is still scored as a gap. Candidates parked solely on a
   missing price or spend anchor may be reopened with a dated addendum.

## Changed files

- `automation/prompts/oe-candidate-scout.md` (rewritten)
- `automation/candidate-discovery/README.md`
- `automation/prompts/oe-weekly-research.md` (price-anchor section)
- scheduled task `oe-candidate-scout` (cadence and branch-read instruction; outside the repository)
