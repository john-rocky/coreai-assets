#!/usr/bin/env python3
"""Weekly metrics snapshot -> stats/*.csv

- GitHub traffic (views/clones daily + referrer snapshots) for the Core AI repos.
  Needs GH_TRAFFIC_TOKEN (fine-grained PAT, Administration:read on the repos);
  skipped gracefully when absent so the HF part still runs.
- Hugging Face download/like counts for all mlboydaisuke models (public API).

CSVs are merged idempotently: re-running on the same day never duplicates rows.
Stdlib only.
"""

import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

REPOS = [
    "john-rocky/coreai-model-zoo",
    "john-rocky/coreai-kit",
    "john-rocky/awesome-core-ai",
    "john-rocky/the-art-of-core-ai",
    "john-rocky/coreai-assets",
]
HF_AUTHOR = "mlboydaisuke"
STATS = "stats"


def http_json(url, token=None):
    req = urllib.request.Request(url, headers={
        "User-Agent": "coreai-metrics",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def merge_csv(path, header, key_len, new_rows):
    """Upsert rows (list of tuples, str-able) into a CSV keyed by the first key_len columns."""
    rows = {}
    if os.path.exists(path):
        with open(path) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                rows[tuple(row[:key_len])] = row
    for row in new_rows:
        row = [str(x) for x in row]
        rows[tuple(row[:key_len])] = row
    os.makedirs(STATS, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for key in sorted(rows):
            w.writerow(rows[key])


AI_REFERRER = ("chatgpt", "openai", "perplexity", "gemini", "claude", "copilot",
               "phind", "you.com", "poe.com", "kagi")


def known_referrers(path):
    seen = set()
    if os.path.exists(path):
        with open(path) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                seen.add((row[1], row[2]))
    return seen


def github_traffic(token):
    daily, refs = {}, []
    seen_before = known_referrers(f"{STATS}/referrers.csv")
    today = datetime.now(timezone.utc).date().isoformat()
    for repo in REPOS:
        try:
            views = http_json(f"https://api.github.com/repos/{repo}/traffic/views", token)
            clones = http_json(f"https://api.github.com/repos/{repo}/traffic/clones", token)
            referrers = http_json(f"https://api.github.com/repos/{repo}/traffic/popular/referrers", token)
        except Exception as e:
            print(f"warn: traffic failed for {repo}: {e}", file=sys.stderr)
            continue
        for v in views.get("views", []):
            d = daily.setdefault((v["timestamp"][:10], repo), [0, 0, 0, 0])
            d[0], d[1] = v["count"], v["uniques"]
        for c in clones.get("clones", []):
            d = daily.setdefault((c["timestamp"][:10], repo), [0, 0, 0, 0])
            d[2], d[3] = c["count"], c["uniques"]
        for r in referrers:
            refs.append((today, repo, r["referrer"], r["count"], r["uniques"]))
    merge_csv(f"{STATS}/traffic.csv",
              ["date", "repo", "views", "views_uniques", "clones", "clones_uniques"], 2,
              [(d, r, *vals) for (d, r), vals in daily.items()])
    merge_csv(f"{STATS}/referrers.csv",
              ["snapshot_date", "repo", "referrer", "count", "uniques"], 3, refs)
    new_ai = [(repo, ref) for (_, repo, ref, _, _) in refs
              if (repo, ref) not in seen_before
              and any(a in ref.lower() for a in AI_REFERRER)]
    with open("/tmp/new-ai-referrers.txt", "w") as f:
        f.write("\n".join(f"{ref} -> {repo}" for repo, ref in new_ai))
    if new_ai:
        print(f"NEW AI REFERRERS: {new_ai}")
    print(f"traffic: {len(daily)} daily rows, {len(refs)} referrer rows")


def hf_downloads():
    today = datetime.now(timezone.utc).date().isoformat()
    models = http_json(
        f"https://huggingface.co/api/models?author={HF_AUTHOR}&limit=200&full=false")
    rows = [(today, m["id"], m.get("downloads", 0), m.get("likes", 0)) for m in models]
    merge_csv(f"{STATS}/hf-downloads.csv",
              ["snapshot_date", "model", "downloads", "likes"], 2, rows)
    # Shields endpoint badge: monthly downloads across Core AI models only.
    total = sum(m.get("downloads", 0) for m in models if "coreai" in m["id"].lower())
    msg = f"{total/1000:.1f}k" if total >= 1000 else str(total)
    os.makedirs("badge", exist_ok=True)
    with open("badge/hf-downloads.json", "w") as f:
        json.dump({"schemaVersion": 1, "label": "🤗 downloads/month",
                   "message": msg, "color": "blue"}, f)
    print(f"hf: {len(rows)} models, coreai total {total}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("traffic", "all"):
        token = os.environ.get("GH_TRAFFIC_TOKEN")
        if token:
            github_traffic(token)
        else:
            print("GH_TRAFFIC_TOKEN not set — skipping GitHub traffic", file=sys.stderr)
    if mode in ("hf", "all"):
        hf_downloads()
