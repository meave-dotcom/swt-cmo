#!/usr/bin/env python3
"""Email a markdown file to REPORT_TO (default info@storieswetell.xyz) via Hostinger SMTP.

Usage: python scripts/send_email.py --subject "..." --file outputs/reports/2026-10-12.md

Env: SMTP_USER, SMTP_PASS (the mailbox login), optional SMTP_HOST (smtp.hostinger.com),
SMTP_PORT (465), REPORT_TO. The agent may only ever send to REPORT_TO.
"""
import argparse, os, smtplib, ssl, sys
from email.message import EmailMessage
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    to = os.getenv("REPORT_TO", "info@storieswetell.xyz")
    user, pw = os.getenv("SMTP_USER"), os.getenv("SMTP_PASS")
    if not (user and pw):
        sys.exit("SMTP_USER / SMTP_PASS not set; report saved in the repo but not emailed.")

    body = Path(a.file).read_text()
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = f"SWT CMO agent <{user}>", to, a.subject
    msg.set_content(body)
    try:
        import markdown  # optional: nicer HTML version
        msg.add_alternative(f"<div style='font-family:Arial,sans-serif;max-width:640px'>"
                            f"{markdown.markdown(body, extensions=['tables'])}</div>", subtype="html")
    except ImportError:
        pass
    host, port = os.getenv("SMTP_HOST", "smtp.hostinger.com"), int(os.getenv("SMTP_PORT", "465"))
    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as s:
        s.login(user, pw)
        s.send_message(msg)
    print(f"Sent '{a.subject}' to {to}")


if __name__ == "__main__":
    main()
