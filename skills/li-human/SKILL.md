---
name: li-human
description: >-
  Clean the machine fingerprint out of any draft - invisible characters, em
  dashes, AI slop words, formula sentence shapes - and score it against a
  five-check panel before it goes out. Use whenever text needs to sound human,
  when the user says humanize, "does this sound like AI", "remove the em
  dashes", "de-slop this", "will this get flagged", or before any LinkedIn
  post, comment, reply or DM is shown to the user.
---

# li-human

## Why this matters on LinkedIn now

Since 30 July 2026 every LinkedIn post has a "Seems like AI slop" report
option. LinkedIn feeds those reports into classifiers that show flagged posts
less often in suggested feeds outside your network, and the author gets a
private note in their post analytics when a post looks heavily AI-written.
LinkedIn also removed its own AI "rewrite my post" feature in favour of a
proofreader that keeps the author's voice.

What gets a post reported is a **person reading it** and finding it empty:
generic claims, no specifics, a voice that could belong to anyone. Punctuation
is the smallest part of that. So the order of importance here is:

1. **Substance** - one real, specific thing that happened, with a number or a
   name. If the draft does not have one, no amount of cleaning will save it.
2. **Shape** - formula sentences ("It's not just X, it's Y", triads, "The
   result?") and identical sentence lengths.
3. **Vocabulary** - stock words (delve, leverage, seamless).
4. **Characters** - invisible characters and em dashes.

## The two tools

Both live in this skill's folder (its base directory) and both actually run.
Use them; do not eyeball this. Save the draft to a temporary file, then run
the scripts by their full path, for example
`python3 -I <skill folder>/humanize.py /tmp/draft.txt --report`. They need
only Python 3, with no packages to install.

If Python is not available here, do the same checks by hand: remove invisible
characters, then go through `slop.json` in this folder and rewrite every em
dash, stock phrase and structural tell it lists. Say that the score was not
run.

```bash
python3 -I humanize.py draft.txt -o clean.txt --report   # safe clean + list of things to rewrite
python3 -I detect.py draft.txt                            # score it, five checks
python3 -I detect.py draft.txt clean.txt                  # before / after
```

Both read `slop.json`: stock words and phrases with plain alternatives,
invisible character classes, typographic substitutions and structural tells.
It is meant to be edited. If the user genuinely uses a word the lexicon flags,
remove it from the file.

## What humanize.py changes automatically

Only fixes that cannot change the meaning:

- **Invisible characters** - zero-width spaces and joiners, word joiners, soft
  hyphens, byte-order marks, Unicode tag characters, non-breaking and narrow
  spaces, and any other invisible format character. Deleted.
- **Typography** - en dash, non-breaking hyphen, figure dash and minus sign to
  a plain hyphen; curly quotes to straight; ellipsis character to three dots;
  bullet character to hyphen. URLs are never touched.

## What it flags for you to rewrite (it does not change these)

The report prints each item **with the line it sits on**. Rewrite those lines
by hand, keeping the meaning and the user's voice:

- **Em dashes.** Depending on the sentence, an em dash becomes a full stop, a
  comma, a colon, or brackets. Pick per sentence. A blind swap to a comma
  makes comma splices, which read worse.
- **Slop words and phrases.** Each comes with a suggestion ("leverage -> try:
  use"). The suggestion is a hint, not a replacement: usually the right fix is
  to rewrite the whole sentence or cut it. Word-for-word swaps produce
  nonsense like "use overlap".
- **Structural tells:** "It's not just X, it's Y", "not only X but also Y",
  rule-of-three triads, one-word rhetorical lines ("The result?"), rocket /
  fire / bulb / sparkle emoji, hashtag walls, "Thoughts?" / "Agree?" bait,
  uniform sentence and bullet lengths.

`--swap-words` and `--fix-dashes` bring back automatic replacement. Do not use
them for anything that will be posted under the user's name.

## The five checks

`detect.py` scores five signals 0-100, higher is more human:

| check | what it measures | machine looks like |
| --- | --- | --- |
| BURSTINESS | sentence-length variation | every sentence the same length |
| SPECIFICITY | numbers, names, concrete markers per 100 words | abstract nouns, no figures |
| SLOP DENSITY | lexicon hits per 100 words | stock vocabulary |
| FINGERPRINT | invisible characters, em dashes, hard spaces per 1k chars | typographically perfect |
| VOICE | contractions, personal pronouns, structural tells | no contractions, staged reveals |

Curly quotes and the ellipsis character are **not** counted against the
text: phone keyboards insert them automatically, so they say nothing about
who wrote it.

The verdict weights the mean at 60% and the weakest single check at 40%.
PASS needs an overall of 70+ with no check below 55.

## Say this honestly

These are five local heuristics. They run on the user's machine and nothing
is uploaded. They are **not** LinkedIn's classifier, and not GPTZero,
Originality, Copyleaks, Winston or Turnitin; they do not call any of them and
cannot predict their verdicts. LinkedIn has not published what its classifier
looks for, and the strongest protection against a "Seems like AI slop" report
is a post with a real, specific story in the user's own voice. Never tell the
user their text is undetectable, and never present a PASS as a guarantee.

## Order of operations

1. `humanize.py draft.txt -o clean.txt --report`
2. Rewrite every flagged line in `clean.txt` yourself: em dashes, slop words,
   structural tells. Keep the user's voice; do not introduce new claims.
3. `detect.py draft.txt clean.txt` to show the before and after.
4. If the verdict is not PASS, fix the weakest check named in the output and
   go again. Two rounds is normal. If SPECIFICITY is the weak one, ask the
   user for the missing number or name - do not invent one. Five rounds means
   the draft was written by formula, and the fix is a different draft.
5. Show the user the cleaned text and the score. Never the score alone.
