---
name: li-plan
description: >-
  Build the week on LinkedIn - what to post, when to post it, and who to engage
  with. Use when the user says "plan my week", "what should I post", "content
  calendar", "I have nothing to post about", or wants a posting schedule and an
  engagement list.
---

# li-plan

The control room. Everything else in this pack executes; this decides what
gets executed. Run it once a week, on the same day.

## Input

Read whichever of these exist in `~/.claude/linkedin/`: `voice.md` (who the
user is), `log.md` (the plan should not repeat a theme from the last
fortnight) and `audit.md` (what the user's own data says to stop and do
more of - it outranks the defaults below). The user's `Main goal` (A-H,
from `/li-start`) shapes the whole plan. If there is no saved profile, ask
the three `/li-start` basics first (what they do, their main goal, who they
want to notice them), or suggest running `/li-start`.

Then ask, in one message:

1. The three or four themes they want to be known for.
2. What actually happened this week - a task finished, a problem solved, a
   number, a mistake, something learned, a conversation, a thing they built.
   This is where posts come from, in every career.
3. Ten to twenty people or organisations worth being visible to.

## What to post

Four posts a week beats seven. Consistency is a floor, not a target, and the
fifth post of a week is almost always the weak one that drags the average.

Mix across the week, never two of the same type back to back:

| type | share | job |
| --- | --- | --- |
| **Proof** | 1 per week | something that happened, with a number |
| **Opinion** | 1 per week | a position that could lose you followers |
| **Teach** | 1 per week | one thing the reader can do today |
| **Story** | 1 per fortnight | a scene with dialogue and a cost |
| **Ask** | 1 per fortnight | what you want, said plainly, no apology - see the goal table |

For each slot give: the theme, the specific angle drawn from what actually
happened this week, and the hook formula number from `hooks.json` (in this folder, or `../li-post/hooks.json`) that
fits it. Not a topic - an angle. "AI" is not a plan. "The proposal we lost
because our AI draft had an em dash in it" is a post.

**Adjust the mix to the goal.** The five types fit every career; what goes
in them changes:

| Goal | Proof is... | Teach is... | The Ask is... |
| --- | --- | --- | --- |
| A. Get hired | a result from a past role or project | something you know well in your field | "I'm looking for X roles in Y" (only if the search is public) |
| B. Start my career | a project, placement or thing you built | what you learned, explained simply | "open to internships / graduate roles in X" |
| C. Grow where I am | a work win (within employer rules) | your expertise | an invitation to collaborate, speak or write |
| D. Win clients | a client result | a tip your clients would pay for | your service and availability |
| E. Grow a business | a customer or company milestone | what your product's users should know | the product, a partnership or a job opening |
| F. Build an audience | your own experiment or story | your topic, the core of the plan | follow, subscribe or attend |
| G. Hire people | a real team story | what working in your team is like | the open role |
| H. Learn and connect | something you tried | what you're learning | a question to your network, a coffee chat |

If the user's job search is private, never plan a public "open to work" Ask.

## When to post

Post when the user's audience is scrolling. For office-based audiences
(most corporate, tech, finance and B2B fields), Tuesday to Thursday,
7:30-9:30am local, is the working default, with Monday afternoon and Friday
morning as the second tier. Audiences that don't sit at desks - healthcare,
retail, hospitality, trades, teachers in term time, students - often scroll
in the evening or at weekends instead; start there and let the analytics
decide.

But state this plainly: **the day and hour matter far less than whether the
first line is good.** If the user is optimising posting times before their
hooks work, they are polishing the wrong thing, and you should say so.

Anchor the times to their **audience's** timezone, not the user's, and read
it from `voice.md` (`Audience timezone`). If it is not there, ask; never
default to US Eastern. Show each time in both zones when they differ, for
example "8:15am IST (audience: India)" or "7:30am PT / 8:00pm IST (audience:
US West Coast)". For an audience spread across regions, pick the region with
the most people who matter for the goal, not the most followers.

## Who to engage with

Build a list of 10, split three ways:

- **5 reach** - people with an audience the user wants, whose posts they can
  genuinely add to. Comment before they have 20 comments or nobody sees it.
- **3 peers** - same level, same field. This is the group that reciprocates.
- **2 decision-makers** - people who could give the user what their goal
  needs: a hiring manager, a client, a customer, a mentor, a candidate.
  Comment on their posts for weeks before any DM, and never ask for anything
  in a comment.

20 minutes a day, before posting, not after. Comments on other people's posts
are what makes the user's own post land.

## Output

```
WEEK OF SEP 8

MON  engage only  (20 min, list below)
TUE  8:15am  PROOF    #17 Time Anchor   - the 5hr -> 20min proposal rebuild
WED  engage only
THU  8:00am  OPINION  #1  Contrarian    - why we killed the discovery call
FRI  8:30am  TEACH    #21 Direct Value  - the 4-line reopen email, given away
SAT  -
SUN  4:00pm  STORY    #9  Cold Open     - the "going with someone cheaper" email

ENGAGE  (5 reach / 3 peers / 2 decision-makers)
  ...

Say "write Tuesday" and I will draft it.
```

Write the plan to `~/.claude/linkedin/plan.md` so `/li-post` can read it. If
files cannot be written here, give the user the plan to keep and paste back.
Nothing is scheduled or posted anywhere - this is a plan, and the user runs it.
