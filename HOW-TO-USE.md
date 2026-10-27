# How to use the LinkedIn agent skills

Eleven skills that help you run a LinkedIn account with Claude: writing posts,
comments, replies and messages, fixing your profile, planning your week and
checking what works.

**They write. You post.** Nothing here posts to LinkedIn for you, and nothing
invents numbers or results under your name.

---

## 1. Install

Pick the one that matches how you use Claude.

### A. Claude app (claude.ai, desktop or phone)

1. Turn on **Code execution and file creation** (newer layout: **Create and
   edit files**) in **Settings → Capabilities**. Skills need it.
2. Download the skill ZIPs from the [`dist/`](dist) folder of this repo. Each
   skill is its own ZIP. Start with these four:
   - `li-post.zip` (writes posts)
   - `li-human.zip` (makes drafts sound like you; li-post uses it)
   - `li-profile.zip` (scores and rewrites your profile)
   - `li-plan.zip` (plans your week)
3. In Claude, go to **Customize → Skills**, tap **+**, then
   **Create skill → Upload a skill**, and upload one ZIP.
4. Turn the skill on in your list. Repeat for each ZIP.

### B. Claude Code (terminal)

```
/plugin marketplace add OWNER/linkedin-agent-skill
/plugin install linkedin-agent
```

Or copy the skill folders yourself:

```bash
git clone https://github.com/OWNER/linkedin-agent-skill.git
cp -r linkedin-agent-skill/skills/li-* ~/.claude/skills/
```

### C. Let Claude install it

In any Claude session that can run commands, paste:

```
https://github.com/OWNER/linkedin-agent-skill

Install this skill, then confirm /li-post works.
```

### Check it worked

Type `/li-post` in a new chat. If Claude starts asking for your past posts or
your idea, it's installed. (Claude Code may show it as
`/linkedin-agent:li-post`; both are the same skill.)

---

## 2. First-time setup: your voice (5 minutes)

Every skill reads a small file called `voice.md` that describes how you write
and who you're writing for. Without it, everything sounds generic.

The easy way: start `/li-post` and paste **three of your own past posts** (or
any three things you've written: messages, captions, emails). Claude also
asks:

- who your audience is, and their **timezone** (for posting times)
- whether your LinkedIn is **Free or Premium** (changes invite-note limits)

Claude then writes `voice.md` for you. The template is in
[`templates/voice.md`](templates/voice.md) if you'd rather fill it in yourself.

In the Claude app, files may not be kept between chats. If Claude can't save
`voice.md`, it gives you the text: keep it in a note (or in a Claude Project's
files) and paste it at the start of a chat when needed.

---

## 3. The eleven skills

| Type | Use it when | Give it | You get |
| --- | --- | --- | --- |
| `/li-post` | You want a post | One idea, ideally with a real number or story | 3 hook options, 1 full draft, humanized, ready to copy |
| `/li-carousel` | Your idea has steps or a list | The idea or a list | Slide-by-slide text, the caption, and a PDF to upload |
| `/li-human` | Any draft sounds like AI | The draft | A cleaned draft, lines to rewrite, and a score out of 100 |
| `/li-comment` | You want to comment on someone's post | Their post text (copy it or screenshot it) | 2 comment options of different types |
| `/li-reply` | People commented on your post | The comments | A reply for each one worth answering, most important first |
| `/li-dm` | You want to message or connect with someone | Who they are, why now, what you want | Invite note, first message, 2 follow-ups |
| `/li-inbox` | Your inbox is messy | Screenshots or pasted messages | Sorted into leads, recruiters, peers, asks and spam, with replies |
| `/li-profile` | You want a better profile | Screenshots of your profile | A score out of 100 and rewrites, worst part first |
| `/li-plan` | You don't know what to post this week | What happened this week, what you sell | A day-by-day plan with hooks and who to engage with |
| `/li-repurpose` | You have a video, blog or transcript | The text or transcript | 4-6 separate post ideas for the week |
| `/li-audit` | You want to know what's working | Your post analytics (export or screenshots) | What to stop, what to do more of, with the numbers |

### Example prompts you can copy

```
/li-post I ran Instagram for a coding club and grew it from 300 to 2,100 followers in 8 months. Main lesson: reels of real members beat designed posters.
```

```
/li-carousel 5 things I learned running marketing for student events
```

```
/li-human
[paste your draft here]
```

```
/li-comment
[paste the post you want to comment on, and the author's name and role]
```

```
/li-reply
[paste the comments under your post]
```

```
/li-dm I want to connect with Priya Rao, Head of Marketing at a Hyderabad startup. She posted about their festival campaign yesterday. I'd like to offer freelance social media help.
```

```
/li-profile
[attach screenshots of your profile: top, About, Experience, Skills]
```

```
/li-plan This week I finished a client campaign (2,000 sign-ups), lost a pitch, and read a great case study on Taj Mahal Tea's rain billboard.
```

```
/li-audit
[attach your LinkedIn analytics export, or screenshots of your last 10 posts with their numbers]
```

You don't have to type the slash command. Saying "write me a LinkedIn post
about…" or "reply to these comments" also works.

---

## 4. A simple weekly routine

| When | Do this | Time |
| --- | --- | --- |
| Sunday | `/li-plan` for the week, then draft your posts with `/li-post` | 1 hour |
| Every day | 3-5 thoughtful comments with `/li-comment` | 15 minutes |
| Posting days | Post, then `/li-reply` to comments in the first hour | 15 minutes |
| Once a week | `/li-inbox` on your messages | 10 minutes |
| Once a month | `/li-audit` on your analytics | 20 minutes |
| Once | `/li-profile`, then fix the profile | 1 hour |

Two or three good posts a week beat seven weak ones.

---

## 5. What gets saved

In Claude Code (and anywhere Claude can keep files), the skills share a
folder, `~/.claude/linkedin/`:

| File | Written by | Used by | What's in it |
| --- | --- | --- | --- |
| `voice.md` | `/li-post` (first run) | all skills | how you write, your audience, timezone, account type |
| `log.md` | `/li-post`, `/li-comment` | `/li-audit`, `/li-plan` | one line per post or comment you approved |
| `plan.md` | `/li-plan` | `/li-post` | this week's plan |
| `audit.md` | `/li-audit` | `/li-plan` | what to stop and do more of |

Where files can't be saved, Claude gives you the text to keep instead.

---

## 6. The rules the skills follow

- **Nothing is posted for you.** Every skill ends with text to copy. Automated
  posting breaks LinkedIn's User Agreement and gets accounts restricted.
- **No invented numbers.** If a post needs a number you haven't given, the
  draft shows `{{your number}}` so you fill in the real one.
- **Humanized, honestly.** Since July 2026 LinkedIn readers can report a post
  as "Seems like AI slop", and reported posts get shown less. The humanizer
  cleans hidden characters and flags AI-sounding lines for a rewrite, but the
  real protection is a true, specific story in your own words. A PASS score is
  a good sign, not a guarantee.
- **Links are a choice.** A link in the post body tends to cut reach; a link in
  the first comment protects reach but gets fewer clicks. The skill asks what
  the post is for.

---

## 7. Troubleshooting

**`/li-post` doesn't appear.** Check the skill is turned on in Customize →
Skills (Claude app), or restart Claude Code after installing. Start a new chat:
skills added during a chat may not show up in that chat.

**"Code execution" error in the Claude app.** Turn on Code execution and file
creation in Settings → Capabilities.

**The humanizer score didn't run.** It needs Python 3 (built into Claude's
code execution). Without it, Claude does the checks by hand and says so.

**Drafts don't sound like me.** Your `voice.md` is thin or missing. Paste three
more of your own posts and say "update my voice.md from these".

**Claude asks for a number I don't have.** Leave the `{{ }}` in, or cut that
line. Don't make one up; readers notice.

---

## 8. For contributors: check everything still works

```bash
python3 tests/run_tests.py     # 60 checks: files, links between skills, humanizer behaviour
python3 tools/build_zips.py    # rebuild the per-skill ZIPs in dist/
```

Both need only Python 3.
