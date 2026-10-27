---
name: li-profile
description: >-
  Score a LinkedIn profile out of 100 against a 12-part rubric and rewrite the
  parts that lose points - headline, about, experience, featured, banner. Use
  when the user says "optimize my profile", "score my LinkedIn", "rewrite my
  headline", "fix my about section", or pastes their profile and asks how it
  reads.
---

# li-profile

A profile is not a resume. A resume answers "what have you done". A profile
answers "should I message this person", and it answers it in about four
seconds, from the headline and the first two lines of the about.

## Who is reading

Read `~/.claude/linkedin/voice.md` first. The user's `Main goal` (A-H, from
`/li-start`) decides who the profile is for: a recruiter, a client, a
customer, a candidate, or peers. If there is no saved profile, ask the three
`/li-start` basics (what they do, their main goal, who they want to notice
them) before scoring, because the same profile can be strong for one goal
and weak for another. Score every item against **that** reader.

## Input

Ask the user to paste: headline, about section, current role and the last two
experience entries, plus whether they have a banner and featured section. A
screenshot of the top card is enough for the first pass. Do not log into
LinkedIn on their behalf.

## Score it

Read `rubric.json` in this folder. Twelve items, 100 points, each with what
full marks looks like. Score every item, show the table, and give the total.
Be honest - most profiles land in the 30s and 40s on the first pass, and a
generous score is useless.

```
PROFILE SCORE  41/100

  headline            3/12   job title only, no outcome, no audience
  about first 2 lines 2/10   opens with "passionate about"
  about body          4/10   history, nothing for the reader
  featured            0/8    empty
  banner              0/6    default blue
  ...
```

## Then rewrite, in this order

Fix in descending order of points lost. Do not rewrite everything at once -
the user has to actually paste each of these in.

**1. Headline (220 characters).** Not just your job title, and not
"Helping X do Y" as the first three words, which every second profile now
opens with. Pick the formula for the goal and give three options:

| Goal | Formula | Example |
| --- | --- | --- |
| A. Get hired | `{role you want} \| {strongest proof} \| {key skills}` | `Product Designer \| Redesigned checkout used by 2M people \| UX research, Figma, design systems` |
| B. Start my career | `{field + role you're heading for} \| {what you've done} \| {where you study or studied}` | `Aspiring Data Analyst \| 3 projects on public health data \| B.Sc Statistics, Pune University` |
| C. Grow where I am | `{role} at {organisation} \| {what you're known for}` | `ICU Nurse at City Hospital \| Teaching new nurses to handle ventilators calmly` |
| D. Win clients | `{what you do for whom} \| {result} \| {how to start}` | `Video editor for course creators \| 40+ courses edited \| DM for a sample` |
| E. Grow a business | `{founder/owner} of {business} \| {what it does for whom}` | `Founder, Crumbs Bakery \| Eggless cakes for Pune offices, delivered by 10am` |
| F. Build an audience | `{the topic you own} \| {format or rhythm}` | `Money lessons for first-job Indians \| New post every Tuesday` |
| G. Hire people | `{what you hire for} at {company} \| {why join}` | `Hiring backend engineers at Finly \| Remote-first, 4-day weeks` |
| H. Learn and connect | `{role} \| {field} \| {what you're exploring}` | `Civil engineer \| Bridges and climate \| Learning about low-carbon concrete` |

If the job search is private, never put "open to work" or "seeking" in the
headline.

**2. About, first two lines.** Everything after line 2 is behind "see more" on
mobile, so those two lines are the whole about section for most readers. They
must tell the target reader (from the goal) the one thing they need to know:
what role you want and why you're good at it (A, B), what you're known for
(C, H), who you help and what changes (D, E), what you post about (F), or
what you're hiring for (G). No "passionate", no "results-driven", no
third-person bio, no opening with your own name.

**3. About body.** Written to that one reader, in plain first or second
person. Structure: what you do or want, how you do it or what you've done,
one piece of proof with a number, what to do next (message you, see your
work, apply, follow). Under 1,400 characters even though the limit is 2,600.

**4. Featured.** Three items: the best post, the proof asset, the way to
contact. An empty featured section is eight points and the only place on the
profile you fully control.

**5. Experience.** Each role gets one line of scope and two to three bullets
that are outcomes with numbers, not duties. Cut anything older than ten years
to a single line.

**6. Banner.** One sentence of positioning and one way to reach you. The
default blue gradient is the clearest signal on the page that nobody is home.

## Output

Score table, then the rewrites as copy-ready blocks in fix-first order, each
one already run through `/li-human`. Re-score at the end and show the delta
honestly - if the rewrite gets to 88 and not 98, say 88, and say what the
remaining points need (usually recommendations, a real banner and posting
history, none of which a rewrite can create).

Nothing is saved to LinkedIn by this skill. The user pastes each section in.
