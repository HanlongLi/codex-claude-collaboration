#!/usr/bin/env python3
"""Read all dialogue changes, explicitly acknowledge snapshots, or append records.

Uses only the Python standard library. File locking targets macOS/Linux.
Cursor files belong to one agent and one dialogue, outside the shared log.
"""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


def speaker_identity(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", value):
        raise ValueError("Speaker must be 1–64 letters, digits, dots, underscores, or hyphens, starting with a letter or digit")
    return value


def read_snapshot(path, cursor):
    data = path.read_bytes()
    mode, offset = "initial", 0
    if cursor.exists():
        state = json.loads(cursor.read_text(encoding="utf-8"))
        if state["path"] != str(path):
            raise ValueError("Cursor belongs to another dialogue; use a separate cursor")
        size = state["bytes"]
        if size >= 0 and len(data) >= size and digest(data[:size]) == state["sha256"]:
            offset = size
            mode = "unchanged" if len(data) == size else "append"
        else:
            mode = "rescan"
    emit({"mode": mode, "path": str(path), "bytes": len(data),
          "sha256": digest(data), "text": data[offset:].decode("utf-8")})


def acknowledge(path, cursor, size, expected_digest):
    data = path.read_bytes()
    if size < 0 or len(data) < size or digest(data[:size]) != expected_digest:
        raise ValueError("Snapshot changed; reread before acknowledging")
    data[:size].decode("utf-8")  # Reject a cursor in the middle of a code point.
    if cursor.exists():
        previous = json.loads(cursor.read_text(encoding="utf-8"))
        if previous["path"] != str(path):
            raise ValueError("Cursor belongs to another dialogue; use a separate cursor")
    cursor.parent.mkdir(parents=True, exist_ok=True)
    state = {"path": str(path), "bytes": size, "sha256": expected_digest}
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cursor.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(state, handle)
            handle.write("\n")
        os.replace(temporary, cursor)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    emit({"acknowledged": state})


def append_record(path, speaker, topic, status, body_file):
    import fcntl

    speaker_identity(speaker)
    if any("\n" in field or "\r" in field for field in (topic, status)):
        raise ValueError("Topic and status must be single-line values")
    body = body_file.read_text(encoding="utf-8")
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    record = f"\n\n### [{speaker}] {timestamp} | {topic} | {status}\n\n{body.rstrip()}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(record.encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())
    emit({"appended": True, "path": str(path), "timestamp": timestamp})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("read", "ack", "append"):
        command = commands.add_parser(name)
        command.add_argument("dialogue", type=Path)
        if name in ("read", "ack"):
            command.add_argument("--cursor", type=Path, required=True)
        if name == "ack":
            command.add_argument("--bytes", type=int, required=True)
            command.add_argument("--sha256", required=True)
        if name == "append":
            command.add_argument("--speaker", type=speaker_identity, required=True,
                                 help="Actual participant identity, e.g. Codex, Claude, Gemini, OpenCode-DeepSeek")
            command.add_argument("--topic", required=True)
            command.add_argument("--status", default="NO REPLY NEEDED")
            command.add_argument("--body-file", type=Path, required=True)
    args = parser.parse_args()
    path = args.dialogue.expanduser().resolve()
    try:
        if args.command == "append":
            append_record(path, args.speaker, args.topic, args.status,
                          args.body_file.expanduser())
        else:
            cursor = args.cursor.expanduser().resolve()
            if cursor == path:
                raise ValueError("Cursor must not overwrite the dialogue")
            if args.command == "read":
                read_snapshot(path, cursor)
            else:
                acknowledge(path, cursor, args.bytes, args.sha256)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
