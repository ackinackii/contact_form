from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ParsedCommand:
    intent: str
    args: Dict[str, str]


class VoiceCommandParser:
    """Simple intent parser for natural-ish voice commands."""

    def parse(self, text: str) -> Optional[ParsedCommand]:
        clean = " ".join(text.strip().split())
        if not clean:
            return None

        lower = clean.lower()

        if lower.startswith("read inbox") or lower.startswith("check inbox"):
            return ParsedCommand(intent="read_inbox", args={})

        delete_match = re.search(r"delete email (\d+)", lower)
        if delete_match:
            return ParsedCommand(intent="delete", args={"index": delete_match.group(1)})

        # Example: send email to a@b.com subject hello body this is test
        send_match = re.search(
            r"send email to\s+(?P<to>\S+)\s+subject\s+(?P<subject>.+?)\s+body\s+(?P<body>.+)",
            clean,
            flags=re.IGNORECASE,
        )
        if send_match:
            return ParsedCommand(
                intent="send",
                args={
                    "to": send_match.group("to"),
                    "subject": send_match.group("subject"),
                    "body": send_match.group("body"),
                },
            )

        reply_match = re.search(
            r"reply to\s+(?P<to>\S+)\s+subject\s+(?P<subject>.+?)\s+body\s+(?P<body>.+)",
            clean,
            flags=re.IGNORECASE,
        )
        if reply_match:
            return ParsedCommand(
                intent="reply",
                args={
                    "to": reply_match.group("to"),
                    "subject": reply_match.group("subject"),
                    "body": reply_match.group("body"),
                },
            )

        if lower in {"help", "what can you do", "commands"}:
            return ParsedCommand(intent="help", args={})

        return ParsedCommand(intent="unknown", args={"raw": clean})
