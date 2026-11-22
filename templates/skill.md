{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ---\
name: your-skill-name\
description: 'One or two sentences that say WHAT this skill does AND WHEN the agent should load it. Write in the third person, name concrete tasks, and include trigger keywords a user would actually say. Example: "Generate professional release notes from a git history. Use when cutting a release, drafting a changelog, or summarizing commits since the last tag."'\
---\
\
# Your Skill Name\
\
> Delete this template's comments as you fill it in. Keep the body under ~500 lines \'97\
> push deep material into `references/`, deterministic helpers into `scripts/`, and\
> templates/fonts/icons into `assets/`. See `../spec/README.md` for the full standard.\
\
## When to use this\
\
Describe the situations this skill is for, in one tight paragraph. Be specific \'97 this\
reinforces the `description` and helps the model trigger correctly.\
\
## Instructions\
\
Give the agent clear, opinionated guidance: the workflow, the decisions, the gotchas.\
Prefer numbered steps for fragile or order-dependent procedures, prose for open ones.\
Assume the reader is a capable engineer \'97 don't explain the basics.\
\
1. Step one.\
2. Step two.\
3. Step three.\
\
## References (optional)\
\
Link to deeper docs the agent should read only when needed:\
\
- `references/deep-dive.md` \'97 loaded on demand (link it once the file exists).\
\
## Scripts (optional)\
\
Describe any executable helpers and whether the agent should **run** or **read** them:\
\
- `scripts/do_thing.py` \'97 run to perform X deterministically.\
\
## Examples (optional)\
\
Show one or two worked examples so the agent can pattern-match the desired output.}