---
name: li-post
description: >-
  Write a LinkedIn post from a raw idea using 21 proven hook formulas, in the
  user's own voice, humanized so it does not read as AI. Use whenever the user
  wants a LinkedIn post, a hook, a draft for the feed, "post about X", "turn
  this into a LinkedIn post", or asks for hook options. Produces three hook
  options, one full draft, and a copy-ready block that is never published
  without an explicit yes.
---

# li-post

Turns one raw idea into a LinkedIn post that sounds like the person who
posted it.

## Before you write

1. Read `~/.claude/linkedin/voice.md` if it exists. That file is the user's
   voice profile: how they talk, what they never say, who they are talking to.
   If it does not exist, ask for **three of their own past posts**, plus their
   audience's timezone and whether they are on a free or Premium account,
   infer the voice from those, and write the file using the template at
   `templates/voice.md` in this plugin. Do not skip this and do not invent a
   voice. A post in the wrong voice is worse than no post.
2. Read `hooks.json` in this folder. All 21 formulas, with templates, filled
   examples, what each is for, and how each one usually gets ruined.
3. If the idea is thin - "post about AI" - do not pad it. Ask one batched
   question: what happened, to whom, and what did it cost or return. A post
   needs one specific true thing. Get it before writing.

## The shape

LinkedIn rewards dwell time, saves and comments, in that order. So:

```
Line 1     the hook. Alone. The feed cuts posts at roughly 210 characters
           (often less on phones, and line breaks cut it sooner), so the
           hook has to work in the first ~140 characters.
Line 2     the payoff of line 1, not setup for line 3.
Body       short paragraphs, 1-3 lines each, blank line between every one.
           No wall. The white space is the format.
The turn   one line that reframes what came before.
Close      one specific question, or one instruction. Never both.
```

Length: 900-1,300 characters is the working range for a text post. Under 400
reads as a thought, not a post. Over 2,000 needs to earn every line, and the
"see more" tap has to be paid for by line 2. LinkedIn's hard limit is 3,000
characters; count and show the length.

If the idea has steps or a sequence, suggest `/li-carousel` instead: document
posts are currently among the strongest formats for reach and saves.

## The loop

**1. Pick three hooks, not one.** Run the idea through `hooks.json` and choose
the three formulas that genuinely fit it. Different formulas, not three
variations of one. Show them as three numbered lines and say which you would
ship and why, in one sentence.

**2. Draft the full post** on the strongest hook.

**3. Humanize it.** Run the draft through `/li-human` before showing it, and
rewrite every line it flags yourself. Every post from this skill ships
humanized. Since July 2026 LinkedIn readers can report a post as "Seems like
AI slop", and reported posts are shown less outside the user's network, so
this step is not optional. But the thing that actually prevents a report is
the true, specific story from step 3 of "Before you write", told in the
user's voice. Cleaning cannot rescue a post that has nothing in it.

**4. Print the block.** Copy-ready, in a fenced block, exactly as it should be
pasted. Then, underneath:

```
POST READY
hook:      #17 Time Anchor
length:    1,140 characters
humanizer: 3 characters cleaned, 4 lines rewritten, human score 84 PASS
link:      in first comment (reach) | in body (clicks) | none
post at:   Tuesday 8:15am, your audience's timezone (from your plan)

Reply "yes" to log it, or tell me what to change.
```

**5. Never publish.** This skill produces text. The user posts it. On "yes",
append the post to `~/.claude/linkedin/log.md` with the date, the hook used
and the first line, so `/li-audit` has a history to work from later.

## Rules that make the difference

- **One idea per post.** If the draft has two, you have two posts. Say so.
- **Numbers over adjectives.** "$4,200" beats "a lot". If the user has not
  given you a number, ask for one rather than writing around the hole.
- **No engagement bait.** "Thoughts?" and "Agree?" are dead. The closing
  question has to be one only this post could ask.
- **Three hashtags maximum**, at the bottom, and only if they are real
  categories someone follows.
- **Links are a trade-off, so ask what the post is for.** Posts with an
  outbound link in the body tend to get less reach. Moving the link to the
  first comment protects reach but loses a large share of the clicks. If the
  goal is reach or conversation, put the link in the first comment and say so
  in the receipt. If the goal is clicks (a sign-up, a launch, a job post), keep
  the link in the body and accept the smaller reach. Never put a link in
  line 1.
- **Never fabricate.** No invented metrics, clients, revenue figures or
  outcomes under the user's name, even as a placeholder. If a number is
  needed and unknown, leave `{{your number}}` in the draft and flag it.

## Example

```
/li-post we built an internal tool that cut proposal time from 5 hours to 20 min
```

```
HOOKS
1. #17 Time Anchor    Writing a proposal used to take me 5 hours. It now takes 20 minutes.
2. #12 Comparison     A $12,000 proposal writer vs a weekend and a template. The weekend won.
3. #3  Mistake        For two years I charged clients for hours I was wasting on formatting.

Shipping #17: the ratio is believable and the number is yours.
```
