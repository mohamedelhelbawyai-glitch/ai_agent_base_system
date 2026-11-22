#!/usr/bin/env python3
"""Send a bounded task to a local Ollama model and print only its answer.

Usage:
  local-worker.py "TASK" [FILE ...]        # files are attached as input
  some_command | local-worker.py "TASK"    # stdin is attached as input

Options:
  -m MODEL     model name (default: $LOCAL_WORKER_MODEL or qwen3.5)
  --think      let the model think first (slower, sometimes better)
  --max N      cap on tokens to generate (default 2048)

Exit codes: 0 ok, 2 bad usage / input too large, 3 Ollama unreachable or error.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

HOST = os.environ.get("OLLAMA_HOST_URL", "http://localhost:11434")
CTX = int(os.environ.get("LOCAL_WORKER_CTX", "32768"))
SYSTEM = (
    "You are a precise worker model. Do exactly the task given, using only the "
    "provided input. Be concise. If the input does not contain the answer, say so "
    "plainly instead of guessing. Do not add preamble or closing remarks."
)


def main() -> int:
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("task")
    p.add_argument("files", nargs="*")
    p.add_argument("-m", "--model", default=os.environ.get("LOCAL_WORKER_MODEL", "qwen3.5"))
    p.add_argument("--think", action="store_true")
    p.add_argument("--max", type=int, default=2048)
    a = p.parse_args()

    parts = []
    for path in a.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                parts.append(f"=== FILE: {path} ===\n{fh.read()}")
        except OSError as e:
            print(f"local-worker: cannot read {path}: {e}", file=sys.stderr)
            return 2
    if not a.files and not sys.stdin.isatty():
        parts.append(f"=== INPUT ===\n{sys.stdin.read()}")

    content = a.task if not parts else f"{a.task}\n\n" + "\n\n".join(parts)

    # Rough guard: ~3.5 chars/token for mixed code/prose. Ollama silently drops
    # the start of an over-long prompt, so refuse instead of returning a wrong answer.
    est = int(len(content) / 3.5) + len(SYSTEM) // 4
    budget = CTX - a.max - 256
    if est > budget:
        print(
            f"local-worker: input too large (~{est} tokens, budget {budget}). "
            "Split it into smaller chunks.",
            file=sys.stderr,
        )
        return 2

    body = {
        "model": a.model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": content},
        ],
        "stream": False,
        "think": a.think,
        "keep_alive": "10m",
        "options": {"temperature": 0.2, "num_predict": a.max},
    }
    req = urllib.request.Request(
        f"{HOST}/api/chat",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"local-worker: Ollama error {e.code}: {e.read().decode()[:300]}", file=sys.stderr)
        return 3
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"local-worker: cannot reach Ollama at {HOST} ({e}). Is the app running?", file=sys.stderr)
        return 3

    print(res.get("message", {}).get("content", "").strip())
    pe, ev = res.get("prompt_eval_count", 0), res.get("eval_count", 0)
    note = " (hit --max; output may be cut off)" if ev >= a.max else ""
    print(
        f"[local-worker: {a.model}, in {pe} tok, out {ev} tok, {time.time() - t0:.1f}s{note}]",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
