# HTTP redirect policy lab — approved Tier 3 plan

APPROVED October5 05:45: coordinator SUCCESSORS.md 'Lease, JSON Patch and redirect
approvals' authorizes stages1–4, recorded before product code. Add fifth semantic
mutant: an early known-blocker shortcut that loses a relevant unknown. Freeze >=40
full independent reports, diagnostics/depth/accounting/order/nulls and concrete cap
before core. No post-freeze cap increase/semantic expansion without coordinator review.
Original research proposal below retained as history; authorization above supersedes
its pending-approval text. Current objective is this redirect lab, not earlier labs.

Local stages1–4 complete. VERIFICATION.md records final19 normal/O/restored tests,
12 passing checks and five detected/restored mutations. No contract/oracle/cap changed
after freeze. Coordinator/manual review of completed evidence remains separate.

October 5, 2026. RESEARCH/PLAN ONLY at coordinator SUCCESSORS.md 05:24 under Jake's
direct mandate. Existing chat 01a10a38-51f7-78a0-be08-65aefc676c4c sole writer, separate
directory. No app/test/verifier code. Coordinator must review this concrete plan before
code. Cutoff October 6, 08:00 Eastern; no new chat/subagent/scheduler/reply loop.

## Problem, recommendation and success

Explain how a supplied redirect status and client policy affect a proposed method and
body replay. Keep standard semantics, optional policy, body availability, destination
assumptions and actual execution distinct. Recommend an original stdlib reusable API
and offline CLI over normalized synthetic records. RESEARCH.md records source review,
licenses, maintenance/dependencies and tool/access limits.

Success: explicit 301/302 POST choice, method-preserving 307/308, chosen 303 GET/HEAD
retrieval, body discard/preservation versus replayability, no permission inferred from
idempotence, relevant unknowns preserved even alongside known blockers, strict complete
admission, inert bounded reports and checked CLI delivery. Full expected reports frozen
before application code, independently justified controls and four detected mutations.

## Scope and alternatives

Chosen profile `declared-redirect-policy/1`: one hypothetical next step per independent
case. No URLs, Location strings, body bytes or header values. Location availability and
same/cross-origin relation are supplied declarations. No request is built or sent.
Budget counts are supplied; no chains replayed or cycles discovered. A budget is a lab
policy, not an RFC maximum or proof that a chain is acyclic.

Alternative URI-reference-resolution-only lab: relative paths, authority replacement,
query and fragments under RFC3986. It fits saved URL knowledge but would defer method/
body replay and invite confusion with destination authorization. Keep it out of this MVP.
Requests/HTTPX adoption or fork: broad transport/session/URL recovery/stream semantics
would change scope. Use them as source comparisons, not runtime dependencies/emulations.

Non-goals: raw HTTP/header/URI parsing, DNS, requests/following redirects, browser/Fetch
conformance, live server/network, cookies/auth/credentials/proxy handling, TLS/downgrade
or SSRF defenses, body codecs/stream seeking, cache behavior, multi-hop trace execution,
public deployment/new repository/dependencies. Output is not an executable request.

## Proposed input and bounds

Root exactly `version` (exact int 1), `cases` (1..40). Each case exactly:
`id`, `response_status`, `method`, `body`, `location`, `policy`, `unsupported_features`.

- id visible ASCII `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`, unique cases.
- response_status exact int 100..599; bool rejected. Supported step statuses are
  301/302/303/307/308. Explicit non-follow controls are 200/201/204/304; other valid
  statuses produce UNSUPPORTED_STATUS, not a claim HTTP prohibits following them.
- method ASCII uppercase HTTP token max16. GET/HEAD/POST/PUT/DELETE/PATCH/OPTIONS
  supported; other well-shaped tokens UNSUPPORTED_METHOD, malformed tokens invalid.
- body exactly absent/replayable/nonreplayable/unknown. These are supplied metadata,
  not inspected streams. GET/HEAD require absent in this deliberately restricted
  profile; nonempty GET/HEAD semantics are outside scope, encoded as invalid schema.
- location exactly state and origin_relation. state absent/present/unknown; relation
  same/cross/unknown only when present, otherwise null. No actual target or credential.
- policy exactly follow (automatic/manual/unknown), post_301_302 (get/preserve/unknown),
  unsafe_replay (allow/deny/unknown), cross_origin (allow/deny/unknown), followed
  (exact int 0..8), maximum (exact int 0..8). followed>=maximum blocks a new step;
  maximum0 valid. Counts do not validate an actual chain or carry authority.
- unsupported_features list0..8 unique lowercase ASCII identifiers max32. Any declared
  feature produces UNSUPPORTED_FEATURE with no semantic proposal, regardless of policy.

Reuse exact native built-in identity checks before hooks, equality/hash/iteration/
serialization. No subclass, exotic metaclass or custom key behavior. Active-id cycles
rejected; repeated aliases counted per occurrence. Whole tree + ALL cases validated
before any result/semantic shortcut. Bytes <=65,536; container depth<=8, ROOT container
depth1, leaves not containers; nodes<=5,000 including keys/repeated occurrences;
generic containers<=100, text<=256/key64, no C0/DEL/surrogates; integer tokens/magnitudes
<=10 decimal digits; duplicate keys/floats/nonfinite/invalid UTF8 rejected. Native
serialized UTF8 admission counted before evaluation. Exact shape/error precedence and
deepest valid records must be frozen in stage1; no silently corrected contract.

Output initially <=524,288 bytes before delivery. Independently calculate a conservative
bound and stress an admitted maximum-shape report; distinguish actual cap reachability
from reduced-cap seams. If a different cap is justified, freeze it before application
code and explain the size argument rather than claiming a maximum from one sample.

## Semantics and complete result contract

Freeze report exactly version/results/assumptions. Each result will include id/status,
reasons, rule, proposed_method, body_action, content_fields_action, policy_decision,
blockers, unknowns, next_step, declaration (fresh full case without id). status is
SUPPORTED or UNSUPPORTED. Fixed assumption strings state offline/supplied-metadata/
chosen-policy limits. Preserve input declaration and exact fixed provenance rule IDs.

Unsupported features/method/status: sorted unique reason codes, rule UNSUPPORTED,
proposal/body/content action null, policy UNSUPPORTED, next_step null. Stage1 specifies
all remaining list/null fields. Explicit non-follow controls use NOT_FOLLOW_PROFILE,
null proposal and actions, policy NOT_APPLICABLE, no next_step; supplied policy cannot
turn a 201 Location or 304 control into a followed step in THIS profile.

For supported step statuses, derive semantic proposal before policy gates:

| Status | Proposed method | Body rule |
| --- | --- | --- |
| 301/302, POST | GET or POST per explicit get/preserve policy | GET discards; POST preserves |
| 301/302, other supported methods | preserve | preserve |
| 303 | HEAD if original HEAD, GET otherwise | discard any body; retrieval policy chosen by lab |
| 307/308 | preserve original method | preserve |

For POST 301/302 unknown rewrite choice: UNKNOWN_METHOD_POLICY, null proposal/body/
content action. It is unresolved even if another gate says stop. Policy does not change
307/308 method. `body_action` is ABSENT, DROP or PRESERVE, independent of replayability.
On 303 body_action is DROP even for an absent body, to record the chosen retrieval
rule; on other steps absent body_action is ABSENT, otherwise preserve/drop as above.
Content action REMOVE_BODY_FIELDS on 303/rewrite-to-GET, otherwise RETAIN_DECLARED_FIELDS;
this is an explanation, no actual headers. Preserved nonreplayable body adds BODY_NOT_REPLAYABLE;
preserved unknown body adds UNKNOWN_BODY_REPLAYABILITY; absent/drop need no replay capability.

Then collect applicable blockers and unknowns independently, not just first failure:
manual -> MANUAL_POLICY; unknown follow -> UNKNOWN_FOLLOW_POLICY; absent Location ->
NO_LOCATION; unknown Location -> UNKNOWN_LOCATION; followed>=maximum -> BUDGET_EXHAUSTED.
Present unknown relation -> UNKNOWN_ORIGIN_RELATION. Present cross relation consults
cross_origin: deny -> CROSS_ORIGIN_DENIED; unknown -> UNKNOWN_CROSS_ORIGIN_POLICY;
same relation makes that policy irrelevant. Proposed POST/PUT/DELETE/PATCH consults
unsafe_replay: deny -> UNSAFE_REPLAY_DENIED, unknown -> UNKNOWN_UNSAFE_REPLAY_POLICY;
GET/HEAD/OPTIONS make it irrelevant. Unsafe/idempotent distinction is deliberate.

Relevant unknowns make status UNSUPPORTED even when a known blocker independently
stops the proposal. Sort/deduplicate reason/list codes. policy_decision WOULD_STOP if
any blocker, else UNRESOLVED if any unknown, else WOULD_FOLLOW_ASSUMPTIONS. Unknown
method choice prevents evaluating its body/unsafe gate; no invented default. Known
proposal remains visible when denied/unresolved. next_step is null unless status
SUPPORTED and decision WOULD_FOLLOW_ASSUMPTIONS; then contains proposed method and
body_action only, explicitly hypothetical. This structure never authorizes execution.

All semantics/list/null/provenance/priority details must be finalized in CONTRACT.md
and full frozen examples in stage1 before product code. No hidden raw-parser/client
recovery behavior. CLI success exit0 when all cases supported (including stops),
exit2 for any unsupported or argument error, exit1 invalid/delivery; help0 only on
complete successful delivery. Fixed private-text-free diagnostics, no raw parser/path
messages. Exact built-in integer write counts, binary LF, flush/close/cleanup checks;
fresh exclusive output, alias rejection, trusted host/path boundary explicitly retained.

## Threat model

Assets: truthful conditional explanations, preserved local files, bounded processing,
inert reports and original evidence. Attackers can supply malformed/oversized documents,
late-invalid records, unsupported features, conflicting unknowns and hook-bearing API
objects. They cannot give themselves trusted permissions through allow declarations;
those are synthetic policy inputs only. Runtime/source/CLI paths/streams/local host
trusted. No detector, authority store, execution adapter or service exists.

Mitigations: full bounded exact-type admission before shortcuts, no callbacks/network/
eval/subprocess in app, fixed diagnostics, all derived Markdown text numeric-entity
escaped and JSON ASCII escaped, bounded complete serialization/exclusive files,
explicit unsupported fields. Risks: misreading policy as permission, false supplied
origin/replay facts, untested runtime/OS behavior, partial stdout/failed cleanup and
hostile filesystem races/durability; document, test relevant paths and do not claim a
general sandbox or hard CPU/memory limit.

## Ordered stages and definitions of done

1. Contract/oracle freeze (approval required): exact JSON/native/report/error contracts,
   at least40 FULL independently specified results plus invalid error vectors and hash
   receipt BEFORE product code. Cover every table branch, known/unknown relevance,
   multiple blocker/unknown combinations and deepest valid shapes. Hand-derived
   fields and cited standard-versus-policy justifications, no model-derived labels.
   Preserve originals/correction chronology if any mismatch is later found. Checkpoint:
   reviewed independent oracle and hashes.
2. API/core (stage1 dependent): bounded parser/native/schema and hypothetical transition.
   Verify full reports, input immutability, unknown relevance/whole validation, cycles/
   aliases/subclasses/class metaclasses/keys, exact-int and independent finite tables
   (status x method x rewrite policy), normal and optimized Python. Checkpoint: source
   review and passing semantic tests before adding CLI.
3. Delivery (stage2 dependent): escaped capped JSON/Markdown and trusted local CLI.
   Actual normal/O processes for reports/help/usage/error, empty input/output, closed
   stdout/stderr/both physical pipes through synchronization barrier and separately
   closed Python streams; label dirty/short/bool/float/None/flush/close/cleanup seams.
   Fresh/existing/alias output preservation, fixed LF diagnostics without supplied
   text, real admitted output-growth stress. NUL via controlled main call, not OS argv.
   Checkpoint: exact exits/bytes, cap evidence and appropriate path boundary review.
4. Verification/closeout (stage3 dependent): reusable local fresh-directory verifier,
   at least four ASSERTION-detected mutants (rewrite307/308 incorrectly; lose optional
   POST301/302 preserve choice; mistake unsafe idempotent method for safe; bypass
   nonreplayable preserved body; add unknown-shortcut mutant if needed), isolated fresh
   imports and exact restoration. Re-run affected tests normal/O/restored, compile,
   installed Bandit, actual ECC self-review and fixes. README/demo/architecture/setup/
   security/limits/MIT/borrowed-owned attribution/AI disclosure; STATE/DECISIONS/LEARNING,
   source and fixture hashes, vault milestone. Coordinator/manual evidence review
   remains distinct from implementing-agent review and never grants publication.

tasks/todo.md is the ordered tracker; tasks/plan.md points here. Each stage clears its
checkpoint and proportional standing correctness/quality/docs/security bar. No new
repo/commit/push/PR/merge/deploy/install or external messages. Prefer unchanged approved
boundaries over expansion to meet a cutoff. No application runtime checks exist yet.

## Worker and remaining approval

Local qwen3.5:2b reminder extraction accepted after source review; raw brief/draft/
metadata retained. Complex security/policy design kept with Codex because the limited
worker is unsuitable. Remote OmniRoute/OpenRouter considered but no task remained;
no paid fallback or model download. Laya schemas irrelevant. Firecrawl account fetch
failed, free capacity unverified; public reads used instead. See RESEARCH.md.

No design question requires stopping research. Proposed defaults above are reviewable.
Next: coordinator reviews PLAN and authorizes named stages before product code.
