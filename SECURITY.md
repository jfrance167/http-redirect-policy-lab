# Security model

Local offline teaching model, no actual HTTP client, service or authorization boundary.
Protected assets: predictable input processing, truthful conditional explanations,
inert output, existing local files and retained evidence. Attacker-shaped declarations
may be malformed/oversized/unknown or hook-bearing API objects. Runtime/application
source and CLI paths/streams/local host are trusted. Synthetic policy allow inputs
never authenticate permissions or authorize contacting any destination.

Exact built-in identity guards precede equality/hash/iteration/serialization on native
inputs. Active cycles rejected; repeated aliases counted per occurrence. No-hook
protection starts at the API invocation, not object construction. Concurrent hostile
mutation of an admitted native object is outside scope. Whole document validation
precedes non-follow/unsupported/policy shortcuts; malformed later cases reject all.

Input<=65536 UTF8 bytes; root container depth1, container depth<=8, values/keys/repeated
aliases<=5000 nodes, generic entries<=100, strings<=256/key64, integers<=10 digits.
Schema narrows further to40 cases/eight features/ASCII identifiers and enums. No
subclasses, duplicate JSON keys, floats/nonfinite/invalid UTF8/controls/surrogates.
GET/HEAD require absent body in this restricted profile. No silent truncation.

Complete reports capped at524288 bytes before delivery. JSON ASCII escaped; all derived
Markdown text numeric-entity escaped. Fresh exclusive binary outputs reject existing
files and aliases; exact int byte counts, flush/close and failed-file cleanup checked.
Fixed diagnostic codes have no supplied paths/tokens/parser details, binary LF preserved.
Failed streams are silenced or Python slots detached to avoid shutdown retry/exit120.
No fallback channel when diagnostics fail; original chosen exit retained.

Residual risks: false supplied origin/replayability facts, interpreting a hypothetical
step as permission, partial stdout, cleanup failure, host filesystem races and durability.
Not a hostile-code sandbox, hard memory/CPU limit, safe URL resolver or SSRF/TLS defense.
Renderer helpers expect evaluated records; raw untrusted input belongs in evaluate.
No body/stream seeking, headers/cookies/proxies/credentials, redirect-chain tracking,
DNS or actual requests. Supplied counters/budgets do not detect real cycles.

Use only invented non-sensitive declarations. No telemetry/network service exists.
Manual boundary review is appropriate before consequential reuse. Repository publishing
and a vulnerability-reporting address are not established by this local work.
