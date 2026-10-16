# Changelog

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
