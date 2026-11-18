# chess-v2 — tiny-chess-01 entry

A chess engine in one 4 KB `main.py` (lzma-packed Python, stdlib only).
0x88 board, zobrist, negamax + alpha-beta, iterative deepening on a fixed
node budget, quiescence, MVV-LVA, PST eval, TT. Reads MAKEFUN_ENV_URL and
plays the gauntlet over POST /game and /move. See SPEC.md.
