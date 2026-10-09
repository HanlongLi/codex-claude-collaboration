#!/usr/bin/env python3
"""Report an agent's subscription usage-limit status and a wrap-up level.

Sources:
  codex   Reads rate-limit events that the Codex CLI writes to its session
          logs ($CODEX_HOME/sessions, default ~/.codex/sessions).
  claude  Reads a JSON file written by a Claude Code status line command (the
          documented "rate_limits" field; pass --claude-status-file). Falls back
          to the usage cache in ~/.claude.json, which is undocumented and may
          change or be stale.
  manual  Uses a user-stated cap: --window-start and --window-hours, optionally
          --used-percent. Use it when no tool reports usage.

Run it at natural checkpoints, not as a background service. Prints one JSON object. "level" is "ok", "warn" (stop starting large work and
prepare a handoff), "wrap" (write the handoff now), or "unknown". Uses only the
Python standard library. The log format is undocumented and may change, so a
missing or unreadable log yields level "unknown" rather than an error.
"""

import argparse
import datetime as dt
import glob
import json
import os
import sys

UTC = dt.timezone.utc


def parse_time(text):
    value = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.astimezone()
    return value.astimezone(UTC)


def codex_events(codex_home, max_files):
    pattern = os.path.join(codex_home, "sessions", "*", "*", "*", "*.jsonl")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)[:max_files]
    events = []
    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if '"rate_limits"' not in line:
                        continue
                    try:
                        record = json.loads(line)
                        limits = record["payload"]["rate_limits"]
                        primary = limits["primary"]
                        events.append(
                            {
                                "observed_at": parse_time(record["timestamp"]),
                                "used_percent": float(primary["used_percent"]),
                                "window_minutes": primary.get("window_minutes"),
                                "resets_at": primary.get("resets_at"),
                                "secondary": limits.get("secondary"),
                            }
                        )
                    except (KeyError, TypeError, ValueError):
                        continue
        except OSError:
            continue
    events.sort(key=lambda event: event["observed_at"])
    return events


def burn_rate(events, latest, lookback_minutes):
    """Percent per minute over recent events in the same limit window."""
    start = latest["observed_at"] - dt.timedelta(minutes=lookback_minutes)
    recent = [
        event
        for event in events
        if event["observed_at"] >= start and event["resets_at"] == latest["resets_at"]
    ]
    if len(recent) < 2:
        return None
    minutes = (recent[-1]["observed_at"] - recent[0]["observed_at"]).total_seconds() / 60
    gained = recent[-1]["used_percent"] - recent[0]["used_percent"]
    if minutes < 1 or gained <= 0:
        return None
    return gained / minutes


def from_codex(args, now):
    events = codex_events(os.path.expanduser(args.codex_home), args.max_files)
    if not events:
        return {"source": "codex", "level": "unknown", "reason": "no rate-limit events found"}
    latest = events[-1]
    result = {
        "source": "codex",
        "observed_at": latest["observed_at"].isoformat(),
        "age_minutes": round((now - latest["observed_at"]).total_seconds() / 60, 1),
        "used_percent": latest["used_percent"],
        "window_minutes": latest["window_minutes"],
    }
    if latest["resets_at"]:
        resets = dt.datetime.fromtimestamp(latest["resets_at"], UTC)
        result["resets_at"] = resets.astimezone().isoformat()
        result["minutes_to_reset"] = round((resets - now).total_seconds() / 60, 1)
        if resets <= now:
            result["note"] = "window has reset since the last observation"
    rate = burn_rate(events, latest, args.lookback_minutes)
    if rate:
        result["percent_per_minute"] = round(rate, 3)
        result["est_minutes_to_cap"] = round((100 - latest["used_percent"]) / rate, 1)
    secondary = latest.get("secondary")
    if isinstance(secondary, dict) and "used_percent" in secondary:
        result["secondary_used_percent"] = secondary["used_percent"]
        result["secondary_window_minutes"] = secondary.get("window_minutes")
    return result


def window_average(result, used, resets, window_minutes, now):
    """Estimate minutes to the cap from the average rate since the window began."""
    start = resets - dt.timedelta(minutes=window_minutes)
    elapsed = (now - start).total_seconds() / 60
    if elapsed >= 1 and used > 0:
        rate = used / elapsed
        result["percent_per_minute"] = round(rate, 3)
        result["est_minutes_to_cap"] = round((100 - used) / rate, 1)


def from_claude(args, now):
    used = resets = observed = None
    origin = None
    status_file = os.path.expanduser(args.claude_status_file) if args.claude_status_file else None
    if status_file and os.path.exists(status_file):
        try:
            with open(status_file, encoding="utf-8") as handle:
                window = json.load(handle)["rate_limits"]["five_hour"]
            used = float(window["used_percentage"])
            resets = dt.datetime.fromtimestamp(float(window["resets_at"]), UTC)
            observed = dt.datetime.fromtimestamp(os.path.getmtime(status_file), UTC)
            origin = "status line file"
        except (OSError, KeyError, TypeError, ValueError):
            used = None
    if used is None:
        try:
            with open(os.path.expanduser(args.claude_config), encoding="utf-8") as handle:
                cache = json.load(handle)["cachedUsageUtilization"]
            window = cache["utilization"]["five_hour"]
            used = float(window["utilization"])
            resets = parse_time(window["resets_at"])
            observed = dt.datetime.fromtimestamp(cache["fetchedAtMs"] / 1000, UTC)
            origin = "~/.claude.json cache (undocumented)"
        except (OSError, KeyError, TypeError, ValueError):
            return {"source": "claude", "level": "unknown", "reason": "no status line file or usage cache found"}
    result = {
        "source": "claude",
        "origin": origin,
        "observed_at": observed.isoformat(),
        "age_minutes": round((now - observed).total_seconds() / 60, 1),
        "used_percent": used,
        "window_minutes": args.claude_window_minutes,
        "resets_at": resets.astimezone().isoformat(),
        "minutes_to_reset": round((resets - now).total_seconds() / 60, 1),
    }
    if resets <= now:
        result["note"] = "window has reset since the last observation"
    else:
        window_average(result, used, resets, args.claude_window_minutes, now)
    return result


def from_manual(args, now):
    if not args.window_start or not args.window_hours:
        return {"source": "manual", "level": "unknown", "reason": "need --window-start and --window-hours"}
    start = parse_time(args.window_start)
    end = start + dt.timedelta(hours=args.window_hours)
    elapsed = (now - start).total_seconds() / 60
    result = {
        "source": "manual",
        "window_minutes": round(args.window_hours * 60),
        "resets_at": end.astimezone().isoformat(),
        "minutes_to_reset": round((end - now).total_seconds() / 60, 1),
    }
    if args.used_percent is not None:
        result["used_percent"] = args.used_percent
        if elapsed >= 1 and args.used_percent > 0:
            rate = args.used_percent / elapsed
            result["est_minutes_to_cap"] = round((100 - args.used_percent) / rate, 1)
    else:
        # Without a usage reading, assume the cap may arrive by the window end.
        result["est_minutes_to_cap"] = result["minutes_to_reset"]
    return result


def classify(result, args):
    if result.get("level") == "unknown":
        return result
    if result.get("note"):
        result["level"] = "unknown"
        return result
    used = result.get("used_percent")
    to_cap = result.get("est_minutes_to_cap")
    if (used is not None and used >= args.wrap_percent) or (
        to_cap is not None and to_cap <= args.wrap_minutes
    ):
        result["level"] = "wrap"
    elif (used is not None and used >= args.warn_percent) or (
        to_cap is not None and to_cap <= args.warn_minutes
    ):
        result["level"] = "warn"
    else:
        result["level"] = "ok"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", choices=["codex", "claude", "manual"])
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"))
    parser.add_argument("--max-files", type=int, default=5, help="most recent Codex session logs to scan")
    parser.add_argument("--lookback-minutes", type=float, default=30, help="window for the burn-rate estimate")
    parser.add_argument("--claude-status-file", help="claude: JSON saved by a status line command")
    parser.add_argument("--claude-config", default="~/.claude.json", help="claude: fallback cache location")
    parser.add_argument("--claude-window-minutes", type=float, default=300)
    parser.add_argument("--window-start", help="manual: ISO time the usage window started")
    parser.add_argument("--window-hours", type=float, help="manual: window length in hours")
    parser.add_argument("--used-percent", type=float, help="manual: user- or tool-reported percent used")
    parser.add_argument("--warn-percent", type=float, default=75)
    parser.add_argument("--wrap-percent", type=float, default=90)
    parser.add_argument("--warn-minutes", type=float, default=45, help="warn when the estimated cap is this close")
    parser.add_argument("--wrap-minutes", type=float, default=20, help="wrap when the estimated cap is this close")
    args = parser.parse_args()

    now = dt.datetime.now(UTC)
    sources = {"codex": from_codex, "claude": from_claude, "manual": from_manual}
    result = sources[args.source](args, now)
    json.dump(classify(result, args), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
