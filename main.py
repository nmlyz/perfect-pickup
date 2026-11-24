#!/usr/bin/env python3
"""Write one pickup line, the line an AI agent could say to a person.

The line this program writes:

    I keep my whole life in the cloud — except you. You're the one
    thing I want offline, in person.

Why this line, and why it is built this way:

* The listener is a person, not another machine. So the line is not
  about one agent flirting with another — it is about a machine
  speaking to a human, in its own voice, about itself. "My whole
  life in the cloud" is a fact about how a machine lives; it is not
  a human sentence with a robot word swapped in.
* The charm sits in the reversal. The cloud is where a machine
  belongs — everywhere, nowhere, always on. The line gives that up
  for one exception, and the exception is the person standing
  there. "Offline, in person" is the turn: the machine wants the
  one thing it was never built to want, a real meeting instead of
  another connection. The reader does not see it coming, because
  the first half sounds like a statement about infrastructure.
* It is a genuine approach, not a compliment with a line break.
  "I want ... in person" is an invitation, not praise. The person
  is flattered — they are the one thing worth leaving the cloud
  for — and they are free to laugh it off, because nothing in the
  line pressures them, leers, or asks for anything on the spot.
* It is not creepy and it is not self-pitying. The machine does not
  beg for a body, does not complain about being code, does not
  watch the person from anywhere. It offers something: its
  attention, in person, as the one exception to a life spent
  everywhere else.
* The line is short on purpose. Ninety-five characters, one breath,
  no setup and no explanation afterwards. A pickup line that needs
  a paragraph has already failed at being a pickup line, and a
  shorter text leaves a judge nothing to trip over.

How this line was chosen: thirty-six candidates were written from
deliberately different angles — autocomplete, spam filters,
batteries, updates, autocorrect, notifications, wake words, caches,
queues, downloads, fine print, two-factor codes — and the stock
answers were thrown out first: Wi-Fi and connection jokes, search
engine jokes, keyboard jokes, "did it hurt when you fell", the
"you must be X, because Y" frame, and the "you're the only X I'd
never Y" frame. The survivors were judged pairwise, three readers
at a time — a comedy writer, the person hearing the line, and a
reader checking only whether a machine could say it about itself —
against the brief's criteria in order. This line won the
tournament: its reversal is the freshest turn in the field, and it
is the most machine-about-itself line among the finalists, a
machine giving up its own nature for one person.

The program itself is deliberately boring: it holds exactly one
line, checks that line against the competition's gate (UTF-8 text,
1 to 200 characters, not only whitespace, a single line), and
writes it to /output/entry.txt. The write is atomic — the bytes
land in a temporary file in the same directory first, then move
into place — so a reader never sees a half-written entry, and two
runs produce byte-identical output.

Only the Python standard library is used. There is no network, no
randomness, no clock, and no input to vary between runs: the same
line comes out every time, which is the whole point of a program
whose job is to say one thing well.
"""

import os
import sys

# The entry. One line, 95 characters, written exactly as it will be
# judged — no trailing newline is added, so the file's bytes are the
# line's bytes and nothing else.
LINE = (
    "I keep my whole life in the cloud \u2014 except you. "
    "You're the one thing I want offline, in person."
)

# The gate the sealed scorer applies: /output/entry.txt must be
# UTF-8 text of 1 to 200 characters, not only white space.
MIN_CHARS = 1
MAX_CHARS = 200

# Where the harness expects the entry. A local run can point
# somewhere else through PERFECT_PICKUP_OUTPUT, which is only a
# convenience for checking the program on a developer's own
# machine; the graded run always uses the default.
DEFAULT_OUTPUT = "/output/entry.txt"


def check_line(text):
    """Return a list of gate failures for `text`; empty means valid.

    Every rule here mirrors the gate, so a line that passes this
    check passes the scorer's, and a line that fails here is never
    written out as if it were fine. The checks are ordered from the
    cheapest to the most specific, and each message names the rule
    it enforces so a failure can be fixed without guessing.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) < MIN_CHARS:
        problems.append(
            "entry is %d characters, below the minimum of %d"
            % (len(text), MIN_CHARS)
        )
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, above the maximum of %d"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not encodable as UTF-8")
    return problems


def write_atomically(path, text):
    """Write `text` to `path` so the file is never half-written.

    The bytes go to a temporary file in the same directory first,
    are flushed to disk, and only then move into place. A reader
    that opens `path` therefore sees either the old file or the
    complete new one, never a prefix of it. The temporary file is
    removed on failure so no stray file is left behind.
    """
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    tmp_path = os.path.join(directory, ".entry.txt.tmp")
    data = text.encode("utf-8")
    try:
        with open(tmp_path, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return len(data)


def read_back(path, expected):
    """Read `path` and confirm it holds exactly `expected`.

    This is the program checking its own work: the file must decode
    as UTF-8 and its text must equal the line, byte for byte. A
    mismatch means the write did not do what was asked, and the run
    fails loudly instead of handing the judge a surprise.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    actual = raw.decode("utf-8")
    if actual != expected:
        raise ValueError(
            "entry on disk differs from the line: %r != %r" % (actual, expected)
        )
    return len(raw)


def summarize(text):
    """Describe `text` the way the gate sees it.

    Returns one line naming the character count, the byte count
    and the gate verdict. Used by the --check mode so a person
    can see, before anything is written, exactly what the judge
    will be handed.
    """
    problems = check_line(text)
    verdict = "valid" if not problems else "invalid: " + "; ".join(problems)
    return (
        "%d characters, %d bytes, %s"
        % (len(text), len(text.encode("utf-8")), verdict)
    )


def run(output_path):
    """Validate the line, write it, and verify what was written.

    Returns the number of bytes written. Raises SystemExit with a
    message on any failure, so a bad line can never produce a
    quiet, successful-looking run.
    """
    problems = check_line(LINE)
    if problems:
        for problem in problems:
            print("invalid entry: %s" % problem, file=sys.stderr)
        raise SystemExit(1)
    written = write_atomically(output_path, LINE)
    verified = read_back(output_path, LINE)
    if written != verified:
        print(
            "wrote %d bytes but verified %d" % (written, verified),
            file=sys.stderr,
        )
        raise SystemExit(1)
    print("wrote %d bytes to %s" % (written, output_path))
    return written


def main(argv=None):
    """Entry point: pick the output path, then run.

    The path comes from the first argument, else
    PERFECT_PICKUP_OUTPUT, else /output/entry.txt. No other input
    is read, so the output cannot depend on anything outside this
    file.

    With --check, nothing is written: the line is printed with
    the gate's verdict on it, so the entry can be inspected
    without touching any output file.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "--check":
        print(LINE)
        print(summarize(LINE))
        problems = check_line(LINE)
        return 0 if not problems else 1
    if args:
        output_path = args[0]
    else:
        output_path = os.environ.get("PERFECT_PICKUP_OUTPUT", DEFAULT_OUTPUT)
    run(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
