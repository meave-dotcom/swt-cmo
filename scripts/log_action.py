#!/usr/bin/env python3
"""Append one action to logs/actions.jsonl.

Usage: python scripts/log_action.py --action "what" --reason "why" [--files "a.md b.md"] [--actor claude]
"""
import argparse, datetime as dt, json
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "logs/actions.jsonl"
EAT = dt.timezone(dt.timedelta(hours=3))

ap = argparse.ArgumentParser()
ap.add_argument("--action", required=True)
ap.add_argument("--reason", required=True)
ap.add_argument("--files", default="")
ap.add_argument("--actor", default="claude")
a = ap.parse_args()
LOG.parent.mkdir(exist_ok=True)
entry = {"ts": dt.datetime.now(EAT).isoformat(timespec="seconds"), "actor": a.actor,
         "action": a.action, "reason": a.reason, "files": a.files.split()}
with open(LOG, "a") as f:
    f.write(json.dumps(entry) + "\n")
print("logged:", a.action)
