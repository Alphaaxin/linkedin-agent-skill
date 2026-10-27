# Changelog

## 1.3.0 (27 Oct 2026) - for any career

- New `/li-start` skill, the first step: asks what the user does, their main
  goal on LinkedIn (A. Get hired, B. Start my career, C. Grow where I am,
  D. Win clients, E. Grow a business, F. Build an audience, G. Hire people,
  H. Learn and connect), who they want to reach, timezone, account type,
  what's off limits and three samples of their writing; shows a summary to
  confirm, then saves it to voice.md.
- Every skill now reads the user's goal and adapts. No skill assumes the
  user is selling something:
  - li-profile: headline formula and About structure per goal; rubric scores
    against the user's own target reader.
  - li-plan: the "Offer" post is now an "Ask" that fits the goal (a role, an
    internship, clients, a hire...); "buyers" are now "decision-makers";
    posting times cover audiences that don't sit at desks.
  - li-dm: a first small ask for each kind of outreach (referral, mentor,
    internship, client, hire, collaboration).
  - li-inbox and li-reply: LEAD is now OPPORTUNITY, defined by the goal.
  - li-audit: measures posts against what the goal needs (interviews,
    enquiries, followers, applications...), not just engagement.
  - li-post, li-comment, li-carousel, li-repurpose: aim at the goal, and
    translate business examples to the user's field and currency.
- Respects confidentiality and private job searches across all skills.
- voice template: career stage, goal, what you offer, privacy of job search.
- Tests: 98 checks, including that every skill reads the profile and none
  uses sales-only wording.

## 1.2.0 (27 Oct 2026)

- HOW-TO-USE.md: install for the Claude app and Claude Code, first-time
  setup, an example prompt for every skill, a weekly routine, troubleshooting.
- dist/: one ready-to-upload ZIP per skill for the Claude app. li-plan,
  li-audit and li-repurpose carry their own copy of hooks.json so each ZIP
  works alone. tools/build_zips.py rebuilds them.
- tests/run_tests.py: 60 automated checks (skill headers, JSON files, links
  between skills, humanizer and detector behaviour).
- Skills now share files consistently: voice.md, log.md (one fixed line
  format), plan.md (li-post reads it), audit.md (li-audit writes it, li-plan
  reads it). Every skill falls back to paste-and-keep when files can't be
  saved, as in Claude app chats.
- li-post ships its own voice-template.md, so manual installs keep it.
- li-human explains how to run its scripts by full path, and what to do
  without Python.
- li-comment: the one-liner comment type is now an explicit exception to the
  2-4 sentence rule.

## 1.1.0 (local fixes, 16 Oct 2026)

Humanizer
- Slop words are now flagged with the line they sit on and a suggested
  alternative, instead of being swapped one-for-one ("leverage synergy" no
  longer becomes "use overlap"). `--swap-words` restores the old behaviour.
- Em dashes are flagged, not blindly turned into commas (which made comma
  splices). `--fix-dashes` restores the old behaviour.
- Non-breaking hyphen, figure dash, hyphen and minus sign are normalised, so
  phrases like "fast-paced world" are caught however the hyphen was typed.
- Detector no longer counts curly quotes or the ellipsis character against
  the text (phone keyboards insert them), and normalises them before the
  contraction and lexicon checks.
- Sentence-variety threshold recalibrated: a genuine human post now passes;
  uniform corporate text and AI-pattern text still fail.
- li-human instructions updated for LinkedIn's July 2026 "Seems like AI slop"
  report option, with substance put ahead of punctuation.

LinkedIn facts
- li-post: links are a reach-vs-clicks trade-off, not a blanket rule; "see
  more" cut-off corrected to ~210 characters; 3,000-character limit noted.
- li-dm: free accounts get only a few noted invites a month (200 chars);
  Premium gets 300; no-note invite route added; weekly cap wording corrected.
- li-carousel: 6-10 slides, 12 maximum.
- li-plan + voice template: audience timezone, account type and spelling;
  no US Eastern default.
