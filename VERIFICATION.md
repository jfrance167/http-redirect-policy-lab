# Verification — October 5, 2026

Windows CPython3.13.7. `python tools/verify.py --output reports/verification-reviewed`
exited0:12 checks passed, exact model restoration true. Use a fresh local output
directory to repeat; installed Bandit1.9.4 required for SAST. No tool installs performed.

| Check | Actual result |
| --- | --- |
| Unit tests normal/optimized/restored | 19 passed in each run |
| Full frozen independent reports | 40 match;26 supported/14 unsupported |
| Frozen diagnostics | 15 match |
| Independent method table | 105 controls |
| Rewrite307/308 mutant | 58 assertion failures |
| Lose POST preserve-choice mutant | 7 assertion failures |
| Idempotent means safe mutant | 8 assertion failures |
| Skip unavailable body mutant | 5 assertion failures |
| Known stop loses unknown mutant | 13 assertion failures |
| Exact restoration / compilation | Passed |
| Bandit | Zero findings/errors;five narrow scaffold nosec comments |
| JSON/Markdown demos |40 rows each;exit2;36675/104408 bytes |

[Final receipt](reports/verification-reviewed/results.json) binds11 app/test/verifier/
fixture/contract hashes; independently recomputed/matched. All six artifacts in the
pre-code [freeze receipt](research/fixture-freeze.json) still match. Original 18-test
successful verifier remains in reports/verification-first; the final added test is
bytes-subclass/alias/count admission. No post-freeze contract/oracle/cap changes.

[Boundary records](reports/verification-reviewed/cli-boundary.json):30 actual child
process records across normal/O,20 physical-pipe-barrier records including live help
control and10 closed-Python-stream records. Parent closes pipes before releasing
stdin barrier into main. Help/usage/invalid/error/report paths, both failed sinks and
closed streams preserve expected statuses/bytes without shutdown exit120 or traceback.
Dirty/short/bool/float/None/flush/close/cleanup seams are injected tests, not physical
failure claims. NUL uses a controlled main call; actual OS argv cannot contain NUL.
Empty output tested through actual module entry point. Partial stdout remains possible.

[Stress records](reports/verification-reviewed/stress.json) contain two profiles per
normal/O run:40 maximum-length IDs/all-gates, input13383/JSON48893/Markdown152985 bytes;
40 maximum features/method shape, input25063/JSON52213/Markdown175345. Both admitted
and fit frozen524288. Reduced-cap seams reject; NO ordinary-cap overflow was observed.
Frozen conservative sizing is an envelope, not a measured maximum or memory guarantee.

Limits: normalized supplied synthetic metadata, trusted local host and this Windows
runtime only. No raw HTTP/URL parser, actual redirect client/body/headers/requests/DNS/
browser/server, destination authority, full conformance, upstream execution, independent
audit, hosted CI, Linux/other runtime or dedicated secret-history certification.
