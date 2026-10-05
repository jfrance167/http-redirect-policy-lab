# Redirect policy research — October 5, 2026

Research/planning only, assigned by coordinator SUCCESSORS.md 05:24 under Jake's
direct overnight successor mandate. No application, tests or verifier implemented.

## Reuse and retrieval

Read the vault Home, Codex Integration and URL Components and Destination Validation.
That reference separates parsing/resolution from destination authorization and warns
that an absolute urljoin argument can replace the base origin. Owned phishing toolkit
README explicitly excludes redirect-chain resolution. Completed media/cache/precondition/
range labs teach different HTTP decisions. A bounded directory/name review found no
dedicated redirect-policy lab; this was not an exhaustive search.

Owned media contracts/report/CLI and MIT license were read and retained byte-for-byte
as research snapshots, with original paths/hashes in research/owned-reuse-receipt.json.
Reuse the exact built-in identity/no-hook admission, full validation, fixed diagnostics,
checked binary streams and exclusive output patterns after approval. Adapt locally with
attribution; do not import siblings at runtime or change completed projects. Root/media
graphify-out/graph.json were absent, so no graph query result is claimed; no graph build,
clone/install or unrelated archive retrieval. GLPI excluded.

## Primary standards

[RFC9110 §15.4](https://httpwg.org/specs/rfc9110.html#status.3xx) distinguishes redirect
semantics and treats following as optional. 301/302 permit POST-to-GET rewriting;
307/308 are method-preserving. 303 permits retrieval through GET or HEAD; choosing
HEAD for original HEAD and GET otherwise is this lab's policy. §10.2.2 describes
relative Location resolution and fragment inheritance. §15.4 discusses field changes,
care with unsafe methods and cycle intervention. Method/body replay, destination
authorization, cookies and actual responses are separate issues.

[RFC3986 §5](https://www.rfc-editor.org/rfc/rfc3986.html#section-5) defines reference
resolution. It supports the alternative lab, not an authorization guarantee.
[Python urllib.parse](https://docs.python.org/3/library/urllib.parse.html#url-parsing-security)
likewise distinguishes component parsing from validation and warns about absolute
urljoin arguments. The MVP will not parse or resolve URLs; supplied origin relations
are assumptions, not verified destinations.

Full public RFC text retained in research/captures. Read relevant RFC9110 Location,
redirect/status and idempotence sections, not every section of either RFC. No RFC code
or published example vectors will be copied into application code/fixtures. In particular,
idempotent PUT/DELETE does not grant authority for a different destination or make an
unsafe method safe. Retrying after communication failure is distinct from redirect replay.

## Candidate review

Connected GitHub discovery/head fetches failed transport; raw error responses retained
in research/github-transport-*.json. Public read-only GitHub API fallback succeeded after
app filesystem/network approval. Raw-host shell fetches failed; public contents API
returned pinned source bytes. Failed paths/host reads remain in capture-index files.
Public code search was not represented as connected success. Discovery query returned
five small/broad projects; none was a stronger fit than established Requests/HTTPX.
No exhaustive candidate or vulnerability search is claimed.

**Requests**, [pinned revision](https://github.com/psf/requests/tree/611c6162cbc4ac2020a2f91c7cfa4f3abf9bbb60):
September 21 head; declared version 2.34.2, Apache-2.0 LICENSE and NOTICE retained.
`SessionRedirectMixin.rebuild_method` rewrites non-HEAD 302/303 and POST 301 to GET.
`resolve_redirects` removes body fields/body except 307/308, resolves locations, rebuilds
cookies/auth/proxies and handles rewindable streams. Read selected method/body removal
tests and no-seek/failed-seek/failed-tell rewind controls. This is a real client with
transport/session state, not the proposed metadata model. Historical issue
[1704](https://github.com/psf/requests/issues/1704), closed November 2013, is linked by
the implementation; its report is not a reproduced current defect. Python >=3.10;
charset_normalizer/idna/urllib3/certifi runtime bounds, setuptools build and broader
test dependencies in the retained manifest. Defined CI spans CPython 3.10–3.15-dev,
3.14t/PyPy and three OSes, pinned actions/read-only permissions. No CI run verified.

**HTTPX**, [pinned revision](https://github.com/encode/httpx/tree/b5addb64f0161ff6bfe94c124ef76f6a1fba5254):
February 23 head; BSD-3-Clause license read/retained. `_build_redirect_request` separates
method, URL, headers and stream; `_redirect_method` has similar method rewrite rules,
while `_redirect_stream` discards a body on a method change to GET. Read MockTransport
tests for 301/302/303, HEAD/next_request, 308 body preservation, 303 removal and consumed
stream failure. Historical issue [771](https://github.com/encode/httpx/issues/771), closed
January 2020, covers missing-host recovery, which this lab excludes; not a current
validated vulnerability. Python >=3.9; certifi/httpcore 1.x/anyio/idna, optional codecs,
HTTP2/SOCKS/CLI and hatchling build. Defined Ubuntu 3.9–3.13 workflow uses mutable action
tags. Documentation says following is opt-in; this is a client-policy difference, not
proof of insecurity. No client execution or successful CI claim.

Capture indexes contain pinned revisions, paths, blob identities, bytes and SHA-256.
Actual retained source portions/tests/manifests/license/workflows/issue metadata were
reviewed; not whole repositories. No advisory/Scorecard/security certification. If source
is redistributed, preserve Requests LICENSE/NOTICE and HTTPX BSD notice; original
application will borrow neither candidate code nor vectors. Research captures remain
private evidence rather than an implied publication artifact.

## Recommendation and workers

Build a small original stdlib declared-policy lab; retain owned MIT boundary patterns.
Installing or forking a transport client adds capabilities and recovery policy the MVP
does not need. Fewer dependencies alone are not a security argument. The URI-reference-
resolution alternative is useful later but does not explain method/body replay.

Existing local Ollama qwen3.5:2b extractor: one public 180-token/45-second brief, completed
826 ms, 176 prompt/67 output tokens, stop. All three reminders source-checked/accepted;
raw brief/draft/metadata retained. Codex retains policy/security/architecture judgment;
the small worker is unsuitable for that work. No remote draft needed: local bounded
extraction adequate. Explicitly considered free OpenRouter/OmniRoute; no invocation or
pricing/readiness probe because no remote task remained. Laya tested schemas irrelevant.
Firecrawl skill consulted: CLI installed/authenticated, account-info fetch failed;
zero-cost capacity could not be verified, so no scrape call was made. Web/public-source
fallback used. No billing, paid fallback, service/provider change or model download.

Next: concrete PLAN.md review and named stage approval before any product code.
