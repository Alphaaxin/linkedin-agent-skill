---
name: li-start
description: >-
  First-run setup for the LinkedIn pack - finds out who the user is (career,
  field, stage), what they want from LinkedIn (a job, clients, customers,
  reputation, an audience, hires, a network) and how they write, then saves
  it so every other li- skill adapts to them. Use when the user says "set me
  up", "start", "who should I be on LinkedIn", is new to the pack, changes
  career or goal, or when another li- skill finds no saved profile.
---

# li-start

LinkedIn advice is only useful once it knows who it is for. A nurse, a
student, a sales director and a freelance designer need different headlines,
different posts and different people to talk to. This skill finds out who the
user is, once, and saves it. Every other skill in the pack reads it.

## The questions

Ask them in **one message**, numbered, so the user can answer in one go. Keep
it friendly and short. Offer examples, never a form to fill in.

1. **What do you do?** Your field and role, in your own words. ("Final-year
   nursing student", "backend engineer at a bank", "freelance video editor",
   "I run a bakery with 6 staff", "between jobs, was in retail management".)
2. **What do you want from LinkedIn in the next 6 months?** Pick one main
   goal, and a second if you have one:
   - **A. Get hired** - a job, a better job, or a switch to a new field
   - **B. Start my career** - internships, first job, mentors (students and
     new graduates)
   - **C. Grow where I am** - be known as good at what I do, inside and
     outside my company
   - **D. Win clients** - freelancers, consultants, agencies, self-employed
   - **E. Grow a business** - customers, partners, investors or hires for a
     company I run
   - **F. Build an audience** - creators, coaches, writers, speakers
   - **G. Hire people** - recruiters and hiring managers
   - **H. Learn and connect** - a network in my field, no hard target
3. **Who do you want to notice you?** Be specific: "hiring managers at
   fintech companies in Bangalore", "small restaurant owners in Pune",
   "nurse managers at NHS trusts", "other data scientists".
4. **Where are they, and where are you?** Country or city, and timezone.
5. **Your account:** Free or Premium?
6. **Anything you can't post about?** Employer social media rules,
   confidential clients or patients, a job search your current employer
   doesn't know about, topics you want to avoid.
7. **Three things you've written** - past posts, or if you've never posted,
   any messages, captions or emails in your own words. This is how the pack
   learns your voice. If they have nothing, skip it and say the voice will
   get better after their first few posts.

If the user already answered some of these in the conversation, don't ask
again. Ask only for what's missing.

## What to infer, and say back

From the answers, work out and **show the user in a short summary** before
saving, so they can correct it:

```
YOU ON LINKEDIN

You:        Final-year nursing student, Manchester
Goal:       B. Start my career (first post: newly qualified nurse role)
Second:     H. Learn and connect
Reach:      Nurse managers and ward recruiters at NHS trusts in the North West
Timezone:   UK (GMT/BST) - audience the same
Account:    Free
Avoid:      Anything that could identify a patient; placement hospital's name
Voice:      Warm, plain, short sentences, no emoji, British spelling

What this means for your profile and posts:
- Headline leads with the role you want, not "student"
- Posts: what you're learning on placement, without patient details
- Comment on nurse leaders' posts; skip the "influencer" crowd
- Proof that counts for you: placements, skills, feedback, not followers
```

The last block is the useful part. Use the goal table below to write it.

## The goal table

Every other skill in the pack uses this to adapt. Keep the user's goal
letter in the saved file so they can look it up.

| Goal | What "success" is | Who to reach | Headline leads with | Proof that counts | The ask, when there is one |
| --- | --- | --- | --- | --- | --- |
| A. Get hired | interviews, recruiter messages | hiring managers, recruiters, people in the target team | the role you want + your strongest proof | results in past roles, skills, projects | "I'm looking for X roles in Y" |
| B. Start my career | internships, first job, mentors | recruiters, alumni, people 2-5 years ahead | the field and role you're heading for | projects, placements, grades, what you built or learned | "open to internships / graduate roles in X" |
| C. Grow where I am | being known for something, internal and external | peers, leaders in the field, your own company | what you're known for + where | work results (within what your employer allows) | invitations to speak, write, collaborate |
| D. Win clients | enquiries, booked calls, clients | people who buy what you do | who you help + the result | client results, before/after, testimonials | "taking on 2 new clients in March" |
| E. Grow a business | customers, partners, investors, hires | customers, partners, investors, candidates | what the business does for whom | customers, milestones, the story | a product, a partnership, a job opening |
| F. Build an audience | followers who engage, subscribers | people interested in your topic | the topic you own | consistency, ideas, engagement | follow, subscribe, attend |
| G. Hire people | good candidates applying | candidates in your field | what you hire for + where | your company's culture, real team stories | the open role, plainly |
| H. Learn and connect | useful conversations | peers and people you admire | your field + what you're curious about | what you're learning, good questions | a conversation, a coffee chat |

## Rules for any career

- **Respect confidentiality.** Patients, clients, students, case details,
  unreleased work and salaries stay out of posts unless the user confirms
  they're allowed. Healthcare, law, finance, government, teaching and many
  large employers have social media rules; if the user's field is one of
  these, remind them once to check.
- **Quiet job searches stay quiet.** If goal A is secret from the current
  employer, never suggest "open to work" publicly, posts about leaving, or
  messages that could reach their manager. Use LinkedIn's recruiter-only
  "Open to work" setting instead.
- **Every career has proof.** If the user says they have "nothing to show",
  ask about problems they solved, things they made better, people they
  trained, feedback they got. Never invent any.
- **Use their words, their currency, their spelling.** A teacher in Kerala,
  an engineer in Berlin and a nurse in Texas write differently. Match it.
- **No goal is lesser.** "Learn and connect" is a fine goal. Don't push
  anyone to sell, to build a personal brand, or to post daily.

## Save it

Write everything to `~/.claude/linkedin/voice.md`, using
`voice-template.md` (in this folder, or `../li-post/voice-template.md`) as
the layout, with
the `## Who I am` section filled from the answers above, including the goal
letter. If that file already exists, update only what changed and keep the
rest.

If files can't be saved in this environment (for example a Claude app chat
with no persistent files), give the user the finished voice.md text in one
copy-ready block and tell them to keep it and paste it into a chat whenever a
skill asks for it.

## Then

End with the next step that fits their goal, in one line:

- A, B, C: "Next: `/li-profile` with screenshots of your profile."
- D, E, G: "Next: `/li-profile`, then `/li-plan` for your first week."
- F, H: "Next: `/li-plan` for your first week of posts."

If their goal changes later (new job, new business, career switch), run
`/li-start` again: it updates the profile and every skill follows.
