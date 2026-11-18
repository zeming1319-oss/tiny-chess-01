# chess-v2 SPEC — makefun tiny-chess-01

## Deliverable
`main.py` — single-file Python 3.13 stdlib chess engine, **≤4096 bytes as committed**
(everything included). Runs as `python3 -P -s /bot/main.py`. 1 CPU, 512 MB, 1800 s wall
for a whole trial of 8 games (~3 s/move average). Snapshot (repo minus .git) ≤8192 bytes.

## Protocol (MAKEFUN_ENV_URL)
Loop: `POST /game {}` → game object. `status=="your_move"` → compute move →
`POST /move {"game": id, "move": "<uci>"}` → house replies (status `your_move` or `over`).
`status=="done"` → exit. Moves are UCI (`e2e4`, `e7e8q`); castling is the king move
(`e1g1`). Each game object carries `start_fen`, `moves` (full history incl. opening),
`fen`, `legal_moves`, `game`. Refused (4xx) requests change nothing; never resign.

## Engine design
- 0x88 board (list of 128 ints, ±1..6 = P N B R Q K, white positive).
- Zobrist hashing (seeded PRNG, deterministic), incremental material+PST eval.
- Incrementally updated: eval, hash, castling rights, ep square, halfmove clock.
- Negamax + alpha-beta, iterative deepening, fixed **node budget** per move (no wall
  clock — replay determinism requires it), check extension, quiescence over captures
  and promotions, MVV-LVA ordering, TT (depth-bounded flags) for ordering + cutoffs.
- Draw handling inside search: repetition (position seen before) and 50-move → 0.
- Promotions: queen only (gen and UCI output); house underpromotions are replayed fine.
- Safety: final UCI is validated against the env's `legal_moves`; fallback to a listed
  legal move if ever off. Per-move position is rebuilt from `start_fen` + `moves`, so a
  search-time timeout unwind (node budget exceeded) cannot corrupt state.

## Sizing strategy
Readable source in dev/ (outside repo), mechanically minified, then if >4096 bytes
packed as an lzma+b64 payload with a tiny unpacker inside main.py. Tests: python-chess
legality cross-check + self-play smoke (dev only, not shipped); grade-local practice run.
