# The LinkedIn agent skill (v1.1, fixed and updated)

> An updated version of [Jake Schincariol's linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill),
> MIT licensed. This version fixes the humanizer (it no longer swaps words
> blindly or turns every em dash into a comma), corrects several LinkedIn
> facts for 2026, and adds LinkedIn's "Seems like AI slop" reporting to the
> advice. Full list in [CHANGELOG.md](CHANGELOG.md).

Eleven Claude skills that run a LinkedIn account. Free, MIT, no signup, no API
key, nothing to connect.

One of them writes your posts off 21 hook formulas. One comments on other
people's posts. One handles the replies under yours. One scores your profile
out of 100 and rewrites what lost points. One plans the week: what to post,
when, and who to engage with.

And one is the humanizer, which is the reason the rest are usable. It strips
invisible characters out of a draft, flags every em dash, stock word and
formula sentence for a rewrite, then scores the result against a five-check
panel before you ever see it.

**Nothing gets posted until you say yes.** These skills write. You post.

## Install

**New here? Read [HOW-TO-USE.md](HOW-TO-USE.md)** - install steps for the
Claude app and Claude Code, first-time setup, an example prompt for every
skill, and a weekly routine.

**Claude app (claude.ai, desktop, phone):** download the skill ZIPs from
[`dist/`](dist), then **Customize -> Skills -> + -> Create skill -> Upload a
skill**, one ZIP per skill. Needs Code execution turned on in Settings ->
Capabilities.

**Claude Code, as a plugin:**

```
/plugin marketplace add OWNER/linkedin-agent-skill
/plugin install linkedin-agent
```

**Or let Claude do it.** Paste this into a Claude session that can run
commands:

```
https://github.com/OWNER/linkedin-agent-skill

Install this skill, then confirm /li-post works.
```

Then set up your voice: start `/li-post` and paste three of your own posts.
Claude writes `~/.claude/linkedin/voice.md` from them, and every skill reads
it. Skip it and everything comes out sounding like everyone else.

## The eleven

| command | what it does |
| --- | --- |
| `/li-post` | One idea into a post. Three hook options from [21 formulas](skills/li-post/hooks.json), one full draft, humanized before you see it. |
| `/li-comment` | Comments on other people's posts. Nine types, picked by what the post actually is. Never "Great post!". |
| `/li-reply` | The thread under your own post. Sorts every comment into lead / substance / peer / support / noise, then writes in that order. |
| `/li-profile` | Scores your profile against a [12-part rubric](skills/li-profile/rubric.json) out of 100, then rewrites in fix-first order. |
| `/li-plan` | The week. What to post, when to post it, and the 10 people to engage with. Writes `~/.claude/linkedin/plan.md`. |
| `/li-human` | The humanizer. Two scripts that actually run. See below. |
| `/li-carousel` | Document posts. Slide-by-slide copy, the cover that earns the swipe, and the PDF to upload. |
| `/li-repurpose` | One video, newsletter or transcript into a week of posts that each stand alone. |
| `/li-dm` | The invite note (200 characters free, 300 Premium, and only a few a month on free accounts), the first message, and the two follow-ups. Two. |
| `/li-inbox` | Triages the inbox into lead / recruiter / peer / ask / spam, and tells you which tell gave the sequence away. |
| `/li-audit` | Post-mortem on what you have already published. Ranks by engagement rate and reach multiple, not impressions. |

## The humanizer

`/li-human` ships two Python scripts with no dependencies. They run on your
machine, on your text, and nothing is uploaded.

```bash
python3 humanize.py draft.txt --report      # safe clean + list of lines to rewrite
python3 detect.py draft.txt                  # score it, five checks
python3 detect.py before.txt after.txt       # prove the delta
```

**What gets fixed automatically** (only changes that cannot alter the meaning):

- **Invisible characters.** Zero-width spaces and joiners, word joiners, soft
  hyphens, byte-order marks, Unicode tag characters, non-breaking and narrow
  spaces. Your keyboard does not make these. They survive copy-paste and they
  are invisible in every editor you own.
- **Typography.** En dash, non-breaking hyphen, figure dash and minus sign to a
  plain hyphen; curly quotes to straight; ellipsis to three dots. URLs are
  never touched.

**What gets flagged, with the line it sits on, for you to rewrite:**

- **Em dashes.** Depending on the sentence, one becomes a full stop, a comma, a
  colon or brackets. A blind swap to a comma makes comma splices.
- **The lexicon.** 113 stock words and phrases - delve, leverage, robust,
  seamless, crucial, testament to, "in today's fast-paced world", "let that
  sink in" - each with a suggested plain alternative. A word-for-word swap
  doesn't read the sentence ("leverage synergy" became "use overlap"), so
  the suggestion is a hint, not a replacement. It lives in
  [`slop.json`](skills/li-human/slop.json) and it is meant to be edited.
- **Structural tells.** "It's not just X, it's Y", rule-of-three triads,
  one-word rhetorical questions, hashtag walls, reflex engagement bait,
  uniform sentence length.

`--swap-words` and `--fix-dashes` bring back the old automatic replacement if
you want it.

**The five checks**, scored 0-100, higher is more human:

| check | what it measures |
| --- | --- |
| BURSTINESS | sentence-length variation. Models write even. |
| SPECIFICITY | numbers, names and concrete markers per 100 words |
| SLOP DENSITY | lexicon hits per 100 words |
| FINGERPRINT | invisible characters, em dashes, hard spaces per 1,000 (curly quotes are not counted: phone keyboards add them) |
| VOICE | contractions, person, structural tells |

The verdict weights the mean at 60% and the **weakest single check** at 40%,
because a detector only needs one signal to fire.

Run against a deliberately terrible draft:

```
  BURSTINESS    ######################..  92.4
  SPECIFICITY   ........................   0.0    0 concrete markers
  SLOP DENSITY  ........................   0.0    8 stock terms, 22.2 per 100 words
  FINGERPRINT   ........................   0.0    1 invisible, 1 em dash
  VOICE         ############............  51.8    2 structural tells
  ------------------------------------------------------------
  HUMAN SCORE   ####....................  17.3   FLAGGED
```

And against a short, specific post written by a person (a real number, two
names, varied sentences):

```
  HUMAN SCORE   ###################.....  80.2   PASS
```

Getting a draft from FLAGGED to PASS is a rewrite, not a cleaning pass. The
script tells you which lines; the rewrite is yours.

**Why this matters more in 2026.** Since 30 July 2026 every LinkedIn post has a
"Seems like AI slop" report option, and LinkedIn shows reported posts less
outside your network. Readers report posts that feel empty, not posts with an
em dash. So the humanizer's real job is to push you toward one specific, true
story told in your own voice.

## The fine print, which is the honest part

**These skills do not post to LinkedIn, and they should not.** There is no
official API for posting to a personal profile without an approved partner
app, and automating the site with a browser or a third-party tool violates
[LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement) and
gets accounts restricted. So every skill here ends the same way: a copy-ready
block, and you paste it. That is not a limitation bolted on afterwards, it is
the design. It is also why the approval gate is real rather than a setting.

**The five checks are local heuristics, not detector APIs.** They are modelled
on the signals public detectors key on, and they run entirely on your machine.
They are not LinkedIn's classifier, and not GPTZero, Originality, Copyleaks, Winston or Turnitin, they do not
call those services, and they cannot promise those verdicts. Fixing what they
measure tends to move those numbers, because they are measuring the same
underlying things. That is the whole claim. Nobody can honestly sell you
"undetectable", and anybody who does is selling you something.

**The invisible-character pass is real and it is narrow.** It removes the
zero-width and format characters that end up in generated text and survive a
copy-paste. That is a genuine, checkable fingerprint. It is not a claim about
defeating a cryptographic watermarking scheme, and this repo does not make
one.

**Nothing here fabricates.** No invented metrics, clients or outcomes go under
your name. If a draft needs a number you have not given, it comes back with
`{{your number}}` in it and a flag, every time.

## Files

```
skills/li-post/hooks.json        21 hook formulas: template, example, what it is for, how it gets ruined
skills/li-human/slop.json        the lexicon: 113 terms, 17 invisible classes, 15 typographic fixes, 11 structural tells
skills/li-human/humanize.py      the safe cleaning passes and the rewrite list
skills/li-human/detect.py        the five-check panel
skills/li-profile/rubric.json    the 100-point profile score
skills/li-post/voice-template.md the voice profile template (also in templates/voice.md)
dist/li-*.zip                    one ZIP per skill, for uploading in the Claude app
tests/run_tests.py               60 checks: files, links between skills, humanizer behaviour
tools/build_zips.py              rebuilds dist/ after you change a skill
HOW-TO-USE.md                    the full guide
```

## Credit

Originally made by Jake Schincariol, [opusjake.ai](https://opusjake.ai).
The original repo is [Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
and the full write-up is at [opusjake.ai/r/linkedin-agent](https://opusjake.ai/r/linkedin-agent).

This updated version (v1.1) is maintained by Mohammed Habeeb Hussain Alkaf.

## License

MIT. Take it, change it, ship it.
