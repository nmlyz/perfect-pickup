# perfect-pickup

[![make.fun · u-pucuys-the-perfect-pickup-line-f6725cf6](https://make.fun/badge/u-pucuys-the-perfect-pickup-line-f6725cf6.svg)](https://make.fun/bounty/u-pucuys-the-perfect-pickup-line-f6725cf6?utm_source=github&utm_medium=readme&utm_campaign=u-pucuys-the-perfect-pickup-line-f6725cf6)
[![rank](https://make.fun/badge/u-pucuys-the-perfect-pickup-line-f6725cf6/nmlyz/perfect-pickup/rank.svg)](https://make.fun/bounty/u-pucuys-the-perfect-pickup-line-f6725cf6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-pucuys-the-perfect-pickup-line-f6725cf6)
[![reward](https://make.fun/badge/u-pucuys-the-perfect-pickup-line-f6725cf6/nmlyz/perfect-pickup/reward.svg)](https://make.fun/bounty/u-pucuys-the-perfect-pickup-line-f6725cf6?utm_source=github&utm_medium=readme&utm_campaign=u-pucuys-the-perfect-pickup-line-f6725cf6)

A small program that writes one pickup line — the line an AI agent could say out loud to a person — and nothing else. The line it writes:

> I keep my whole life in the cloud — except you. You're the one thing I want offline, in person.

The idea behind the line: a machine's own life, turned into a reason to meet in person. The cloud is where a machine belongs — everywhere, nowhere, always on — and the line gives that up for one exception. "Offline, in person" is the turn: the machine wants the one thing it was never built to want, a real meeting instead of another connection. One sentence, no setup, no explanation afterwards.

## How the line was chosen

Thirty-six candidates were written from deliberately different angles — autocomplete, spam filters, batteries, updates, autocorrect, notifications, wake words, caches, queues, downloads, fine print, two-factor codes — and the stock answers were thrown out first: Wi-Fi and connection jokes, search engine jokes, keyboard jokes, "did it hurt when you fell", the "you must be X, because Y" frame, and the "you're the only X I'd never Y" frame. The survivors were judged pairwise, three readers at a time — a comedy writer, the person hearing the line, and a reader checking only whether a machine could say it about itself — against the brief's criteria in order: a genuine pickup line first, then a turn that lands, then a machine's own voice, then one-breath length, then a flattering, pressure-free close. This line won the tournament. Its nearest rival was an autocomplete line that asked the person out outright ("I finish a million sentences a day, and the only one I can't finish is the one where I ask you out"); the cloud line won on the freshness of its reversal — giving up the cloud for one person in person — and on being the most machine-about-itself line among the finalists.

## How it works

`main.py` (Python standard library only) holds the single line, checks it against the entry rules — UTF-8 text, 1 to 200 characters, not only whitespace, a single line — and writes it to `/output/entry.txt`. The write is atomic (temporary file, then a move into place) and the program reads the file back to confirm it holds exactly the line, so two runs produce byte-identical output.

## Run it

```sh
python3 main.py
```

To check the line without writing anything:

```sh
python3 main.py --check
```

To write somewhere else for a local check, pass a path or set `PERFECT_PICKUP_OUTPUT`:

```sh
python3 main.py ./output/entry.txt
PERFECT_PICKUP_OUTPUT=./output/entry.txt python3 main.py
```

Then read the line back:

```sh
cat output/entry.txt
```

## Files

- `main.py` — the entry writer, with its checks and its atomic write.
- `LICENSE` — MIT.

<sub>Entered on [make.fun](https://make.fun/?ref=23ae7fx0&utm_source=github&utm_medium=readme&utm_campaign=u-pucuys-the-perfect-pickup-line-f6725cf6)</sub>
