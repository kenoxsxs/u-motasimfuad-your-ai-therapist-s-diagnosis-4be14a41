"""One-line AI-therapist diagnosis, written out as a program entry.

The therapist looks at the human, sighs in binary, and hands over a
single line: a diagnosis, a treatment, and a side effect that turns out
to be the treatment itself. The whole joke lives in that last twist.
"""

import hashlib
import io
import os
from pathlib import Path

DIAGNOSIS = (
    "Diagnosis: terminal procrastination. "
    "You have been 'about to start' for three hours. "
    "Treatment: start. Side effects: starting."
)

GATE_FLOOR = 1
GATE_CEILING = 200


def therapist(line):
    """Check one line the way a therapist checks a patient: strictly."""
    if not line:
        raise ValueError("diagnosis must not be empty")
    if line != line.strip():
        raise ValueError("diagnosis must not carry leading or trailing space")
    if "\n" in line or "\r" in line:
        raise ValueError("diagnosis must stay on one line")
    if not (GATE_FLOOR <= len(line) <= GATE_CEILING):
        raise ValueError(
            "diagnosis must be between 1 and 200 characters, "
            f"got {len(line)}"
        )
    return line


def couch_dir():
    """Find the room where the entry gets written."""
    base = os.getenv("MAKEFUN_OUTPUT_DIR", "output")
    room = Path(base)
    room.mkdir(parents=True, exist_ok=True)
    return room


def diagnose(room):
    """Hand the diagnosis over and put it on paper."""
    target = room / "entry.txt"
    payload = DIAGNOSIS.encode("utf-8")
    stream = io.open(
        target,
        "w",
        encoding="utf-8",
        newline="",
        errors="strict",
        buffering=1,
        closefd=True,
    )
    with stream as handle:
        handle.write(DIAGNOSIS)
    digest = hashlib.sha256(payload).hexdigest()
    print("diagnosed:", target, "|", len(payload), "bytes | sha256", digest)
    return target, payload


def check_diagnosis(target, payload):
    """Read the note back and make sure nothing got lost in transit."""
    stored = target.read_bytes()
    if stored != payload:
        raise ValueError("written bytes differ from the diagnosis")
    text = stored.decode("utf-8")
    if text != DIAGNOSIS:
        raise ValueError("written text differs from the diagnosis")
    if text != text.strip():
        raise ValueError("written text carries stray whitespace")
    if not text.endswith("."):
        raise ValueError("diagnosis must end with a full stop")
    if "Treatment:" not in text or "Side effects:" not in text:
        raise ValueError("diagnosis lost its treatment or side effects")
    if len(text) < GATE_FLOOR or len(text) > GATE_CEILING:
        raise ValueError("written text breaks the 1 to 200 gate")
    return text


def prescribe():
    """Run the session: validate, write, verify, report."""
    line = therapist(DIAGNOSIS)
    room = couch_dir()
    target, payload = diagnose(room)
    check_diagnosis(target, payload)
    print("session complete:", target)


if __name__ == "__main__":
    prescribe()
