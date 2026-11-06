#!/usr/bin/env python3
"""
Send the 0DTE channel-info message to Discord every trading day at 7 AM ET.
Requires: DISCORD_WEBHOOK_URL environment variable.
"""
import os
import sys
import requests
from datetime import date

try:
    import exchange_calendars as xcals
    _cal = xcals.get_calendar("XNYS")

    def is_trading_day(d: date) -> bool:
        return _cal.is_session(str(d))

except ImportError:
    def is_trading_day(d: date) -> bool:
        return d.weekday() < 5  # fallback: Mon–Fri only


ESC = "\u001b"
R  = f"{ESC}[0m"       # reset
B  = f"{ESC}[1m"       # bold
CY = f"{ESC}[36m"      # cyan
YL = f"{ESC}[33m"      # yellow / orange
RD = f"{ESC}[31m"      # red

CHANNEL_INFO = f"""\
```ansi
{B}{CY}0DTE INDEX OPTIONS — CHANNEL INFO{R}
SPX / NDX / XSP same-day-expiry trading talk

{B}{YL}WHAT THIS CHANNEL IS{R}
Live setups, entries/exits, and real-time market structure discussion on same-day-expiry index options. High-risk, high-speed, fast-paced — read accordingly.

{B}{RD}⚠ NOT FINANCIAL ADVICE — DO NOT COPY TRADES{R}
{RD}0DTE options can lose 100% of value in minutes.
Nobody here knows your account size, risk tolerance, or goals. Trades shared are NOT recommendations and are NOT meant to be copy/pasted or mirrored.{R}

{YL}Acting on someone else’s 0DTE trade in real time, without your own independent analysis, is one of the fastest ways to blow up an account.{R}

You are solely responsible for your own trades.
Past results posted here are not indicative of future performance. Trade at your own risk.
```"""


def send(webhook_url: str, content: str) -> None:
    resp = requests.post(webhook_url, json={"content": content}, timeout=10)
    resp.raise_for_status()
    print(f"Sent ({resp.status_code})")


def main() -> None:
    today = date.today()
    if not is_trading_day(today):
        print(f"{today} is not a trading day — skipping.")
        return

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("ERROR: DISCORD_WEBHOOK_URL is not set.", file=sys.stderr)
        sys.exit(1)

    send(webhook_url, CHANNEL_INFO)


if __name__ == "__main__":
    main()
