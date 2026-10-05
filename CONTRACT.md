# Frozen declared-redirect-policy/1 contract

Root exactly version:int1, cases:list1..40; case fields and enums are exactly the
approved PLAN input profile. Keys outside the shape are invalid. Case IDs unique
ASCII `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`; method uppercase HTTP-token ASCII1..16.
response_status exact int100..599; body absent/replayable/nonreplayable/unknown;
GET/HEAD require absent. Location exactly state(absent/present/unknown),origin_relation
(same/cross/unknown when present; null otherwise). Policy exactly follow(automatic/
manual/unknown),post_301_302(get/preserve/unknown),unsafe_replay(allow/deny/unknown),
cross_origin(allow/deny/unknown),followed:int0..8,maximum:int0..8. Features0..8 unique
ASCII `[a-z][a-z0-9-]{0,31}`. Unsupported methods/statuses/features remain valid-shaped.

Admission order: exact-native tree guard first, compact ensure_ascii=False UTF8 byte
bound second, root shape/version/case count third, each case in input order: exact
keys,id/duplicate,status,method,body/GETHEAD shape,location shape/state/relation,policy
shape and fields in the above order,features count/shape/duplicate. Validate ALL cases
before semantics. Generic tree allowed only exact dict/list/str/int/bool/None; subclasses/
class objects/exotic keys rejected before hooks. Container depth root1 maximum8; scalar
leaves do not add containers. Count all values and dict keys, aliases each occurrence,
limit5000; active-id cycles invalid. Generic container entries<=100, string<=256/key64,
no C0/DEL/surrogates; native integer magnitude<=9999999999. Input<=65536bytes; output
<=524288bytes before delivery. Parse exact bytes only: byte bound, strict UTF8, lexical
container-depth8 outside quoted strings, then JSON duplicate-key/integer-token10-digit
hooks; floats/nonfinite invalid. Parse admits syntax only; evaluate enforces full native
and schema admission. Empty/truncated/invalid JSON fixed INVALID_JSON. No truncation.

Error codes in admission order: TREE_TYPE,NODE_LIMIT,TREE_DEPTH,TREE_CYCLE,
CONTAINER_LIMIT,TEXT_TYPE_OR_LIMIT,TEXT_CONTROL,INVALID_UNICODE,INTEGER_TOKEN_BOUND;
INPUT_LIMIT; SCHEMA,VERSION,CASE_COUNT,ID_FORMAT,DUPLICATE_CASE_ID,STATUS,METHOD,
BODY,BODY_SHAPE,LOCATION_STATE,LOCATION_RELATION,LOCATION_SHAPE,FOLLOW_POLICY,
POST_POLICY,UNSAFE_POLICY,CROSS_POLICY,FOLLOWED,MAXIMUM,FEATURE_COUNT,FEATURE,
DUPLICATE_FEATURE. Generic guard precedence follows preorder and field insertion
order; schema order above fixed. Byte parse uses JSON_DEPTH,DUPLICATE_KEY,
INTEGER_TOKEN_BOUND,NONINTEGER_JSON,INVALID_JSON as appropriate. No stderr raw value.

Report exactly version1/results/assumptions. Assumptions exactly:
1. Offline supplied declarations only; no request is built or sent.
2. Origin relation, body replayability and policy are unverified assumptions.
3. GET-for-non-HEAD 303 and explicit 301/302 POST choices are lab policy.

Every result exactly id,status,reasons,rule,proposed_method,body_action,
content_fields_action,policy_decision,blockers,unknowns,next_step,declaration.
declaration is a fresh deep copy of full case minus id. Lists sorted unique strings;
reasons union of blockers/unknowns, except global unsupported reason lists.

Global checks collect UNSUPPORTED_FEATURE(any features),UNSUPPORTED_METHOD(not
GET/HEAD/POST/PUT/DELETE/PATCH/OPTIONS),UNSUPPORTED_STATUS(not301/302/303/307/308/
200/201/204/304). Any: statusUNSUPPORTED,ruleUNSUPPORTED,proposal/body/content null,
policyUNSUPPORTED,blockers[],unknowns[],next_step null. Otherwise 200/201/204/304:
statusSUPPORTED,ruleNOT_FOLLOW_PROFILE,proposal/body/content null,policyNOT_APPLICABLE,
lists[],next_step null regardless of other valid fields; only this profile's controls.

Rules for five step statuses: 301/302 POST get->POST_TO_GET, preserve->POST_PRESERVED,
unknown->POST_CHOICE_UNKNOWN; other methods->METHOD_PRESERVED. 303->RETRIEVAL_303,
HEAD if originalHEAD elseGET, bodyDROP including absent. 307/308->METHOD_PRESERVED.
POST_TO_GET bodyDROP. Preserved method bodyABSENT if absent elsePRESERVE. DROP gives
contentREMOVE_BODY_FIELDS; known preserved method gives RETAIN_DECLARED_FIELDS.
Unknown POST choice: proposal/body/content null, unknowns[UNKNOWN_METHOD_POLICY],
do not infer body/unsafe gates. Known PRESERVE body nonreplayable adds blocker
BODY_NOT_REPLAYABLE; unknown adds UNKNOWN_BODY_REPLAYABILITY; ABSENT/DROP do not.

Always collect independent follow/manual->MANUAL_POLICY; follow/unknown->
UNKNOWN_FOLLOW_POLICY; location/absent->NO_LOCATION; location/unknown->UNKNOWN_LOCATION;
followed>=maximum->BUDGET_EXHAUSTED. Present origin unknown->UNKNOWN_ORIGIN_RELATION;
cross origin consult cross policy deny->CROSS_ORIGIN_DENIED,unknown->
UNKNOWN_CROSS_ORIGIN_POLICY; same ignores cross policy. Known proposedPOST/PUT/DELETE/
PATCH consult unsafe policy deny->UNSAFE_REPLAY_DENIED,unknown->
UNKNOWN_UNSAFE_REPLAY_POLICY; GET/HEAD/OPTIONS ignore unsafe policy. All independently
applicable gates collected even after known blocker. Relevant unknowns make status
UNSUPPORTED, otherwise SUPPORTED. Known proposal/body/content remain visible.
policy WOULD_STOP if blockers, elseUNRESOLVED if unknowns, elseWOULD_FOLLOW_ASSUMPTIONS.
next_step null unless SUPPORTED and WOULD_FOLLOW_ASSUMPTIONS; then exactly method and
body_action, hypothetical only. No credentials/URLs/streams/destination authorization.

CLI input trusted local file bounded read65537; empty/NUL path fixed INVALID_INPUT_PATH/
INVALID_OUTPUT_PATH; alias INPUT_OUTPUT_ALIAS. Exclusive fresh binary output, exact
builtin integer full-byte write/flush/close, failed fresh file cleanup; failure to
cleanup OUTPUT_WRITE_AND_CLEANUP_FAILED. Checked binary stdout; failed stream silenced
to avoid shutdown retry, or STDOUT_WRITE_AND_SILENCE_FAILED if OS silencing fails.
Other read/write failure IO_ERROR. Diagnostic fixed `redirectlab: CODE\n` ASCII LF,
no fallback if stderr fails; preserve chosen exit. Argument errors fixedARGUMENT_ERROR
exit2, no supplied token echo. Supported reports exit0, any unsupported exit2;
invalid/delivery exit1, help0 only successful delivery. JSON ASCII escaped; Markdown
every derived character numeric-entity escaped; evaluated reports only for renderer.

Cap justification: exact keys and constrained scalar lengths give declaration below
1024 compact ASCII chars (includes eight32char features); output fixed fields below
512, all blocker/unknown/reason lists below1536, punctuation/next_step below256:
conservative4096 compact chars/result. Markdown derived text conservatively <=4096
per row plus256 fixed layout, numeric entities at most6chars per ASCII character;
40*(4096*6+256)+4096=997376 bytes (<1MiB). Pretty JSON conservatively <524288 from
4096*40 plus327680 whitespace allowance. Input strings in schema are ASCII; no
multibyte expansion admitted. 524288 is a DELIVERY cap below conservative Markdown
allocation envelope, not a promise that all valid documents fit or that overflow is
reachable. Measure actual admitted stress separately; label reduced-cap seams. No
cap increase after freeze without coordinator review. No hard resource sandbox/race/
atomic stdout/durability/full client conformance guarantee.
