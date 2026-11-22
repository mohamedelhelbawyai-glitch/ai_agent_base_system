---
name: local-worker
description: Hand bounded, low-judgment text tasks (summarize a long file or log, extract fields, classify items, draft boilerplate, first-pass scan) to the local qwen3.5 model via Ollama, so large inputs never enter Claude's context. Use when a task would otherwise mean reading a big file or output just to get a short answer. Not for planning, multi-step reasoning, final code edits, or anything needing judgment.
---

# Local worker (Ollama, qwen3.5)

Goal: save Claude tokens. Claude stays the orchestrator; a local model on this Mac
(Apple M5, 16 GB, qwen3.5 9B, 32k context, ~19 tok/s) does the bulk reading.
Claude reads only the short answer.

## How to call

```bash
python3 ~/.claude/skills/local-worker/local-worker.py "TASK" path/to/file [more files]
some_command 2>&1 | python3 ~/.claude/skills/local-worker/local-worker.py "TASK"
```

Options: `--think` (slower, for harder extraction), `--max N` (output token cap,
default 2048), `-m MODEL`. A stats line goes to stderr.

Write TASK as a precise instruction with an explicit output format, for example:
- "List every ERROR line's timestamp and message as `time | message`. Max 20 lines."
- "Summarize what this module does in 5 bullets. Name the public functions."
- "Return JSON: {\"name\":..., \"version\":..., \"dependencies\":[...]} from this file."
- "Classify each line as BUG, FEATURE, or QUESTION. Output `n: LABEL` per line."

## When to delegate

Good fits (the input is big, the answer is small):
- Long logs, test output, build output → errors and causes
- Large files you only need an overview of, or a few facts from
- Many similar items to label, sort, or extract from
- First drafts of boilerplate, docstrings, commit-message summaries of a diff

Do it yourself instead when:
- The input is short (under ~2k tokens). Delegating costs more than reading it.
- The task needs judgment, design, multi-step reasoning, or careful code edits.
- Being wrong would be costly and you couldn't check the answer cheaply.

## Rules

- The input limit is about 28k tokens (~100 KB). On "input too large", split the input (e.g. with
  `split -l` or by file) and run the worker per chunk, then combine the short answers.
- The local model is much weaker than Claude. Treat its output as a lead, not a fact:
  spot-check claims that matter (a quick grep on a quoted line or name).
- Exit code 3 means Ollama isn't running: tell the user to open the Ollama app.
- Everything stays on this computer. Nothing is sent to a cloud service.
- This is a Bash call, not a subagent, so the user's subagent-approval rule does not apply.

## Agentic option (use rarely)

For a task that needs tools (searching a repo, opening several files) you can run a
separate headless Claude Code on the local model:

```bash
ollama launch claude --model qwen3.5 --yes -- -p "TASK"
```

A 9B model is unreliable at multi-step tool use, so prefer the script above. Use this
only for simple search-and-report tasks, and verify the result.
