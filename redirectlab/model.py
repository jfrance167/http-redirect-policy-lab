"""Conditional single-step explanations over admitted declarations; no execution."""

import copy

from .contracts import validate

ASSUMPTIONS = [
    "Offline supplied declarations only; no request is built or sent.",
    "Origin relation, body replayability and policy are unverified assumptions.",
    "GET-for-non-HEAD 303 and explicit 301/302 POST choices are lab policy.",
]
METHODS = ("GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
UNSAFE = ("POST", "PUT", "DELETE", "PATCH")


def _case(case):
    declaration = copy.deepcopy(case)
    declaration.pop("id")
    row = dict(id=case["id"], status="SUPPORTED", reasons=[], rule=None,
               proposed_method=None, body_action=None, content_fields_action=None,
               policy_decision=None, blockers=[], unknowns=[], next_step=None,
               declaration=declaration)
    status, method, policy = case["response_status"], case["method"], case["policy"]
    unsupported = []
    if case["unsupported_features"]:
        unsupported.append("UNSUPPORTED_FEATURE")
    if method not in METHODS:
        unsupported.append("UNSUPPORTED_METHOD")
    if status not in (200, 201, 204, 304, 301, 302, 303, 307, 308):
        unsupported.append("UNSUPPORTED_STATUS")
    if unsupported:
        row.update(status="UNSUPPORTED", reasons=sorted(unsupported),
                   rule="UNSUPPORTED", policy_decision="UNSUPPORTED")
        return row
    if status in (200, 201, 204, 304):
        row.update(rule="NOT_FOLLOW_PROFILE", policy_decision="NOT_APPLICABLE")
        return row
    proposed, rule = method, "METHOD_PRESERVED"
    if status in (301, 302) and method == "POST":
        choice = policy["post_301_302"]
        if choice == "get":
            proposed, rule = "GET", "POST_TO_GET"
        elif choice == "preserve":
            rule = "POST_PRESERVED"
        else:
            proposed, rule = None, "POST_CHOICE_UNKNOWN"
            row["unknowns"].append("UNKNOWN_METHOD_POLICY")
    if status == 303:
        proposed, rule = ("HEAD" if method == "HEAD" else "GET"), "RETRIEVAL_303"
    row.update(rule=rule, proposed_method=proposed)
    if proposed is not None:
        body = "DROP" if rule in ("POST_TO_GET", "RETRIEVAL_303") else (
            "ABSENT" if case["body"] == "absent" else "PRESERVE")
        row["body_action"] = body
        row["content_fields_action"] = "REMOVE_BODY_FIELDS" if body == "DROP" else "RETAIN_DECLARED_FIELDS"
        if body == "PRESERVE":
            if case["body"] == "nonreplayable":
                row["blockers"].append("BODY_NOT_REPLAYABLE")
            elif case["body"] == "unknown":
                row["unknowns"].append("UNKNOWN_BODY_REPLAYABILITY")
        if proposed in UNSAFE:
            if policy["unsafe_replay"] == "deny":
                row["blockers"].append("UNSAFE_REPLAY_DENIED")
            elif policy["unsafe_replay"] == "unknown":
                row["unknowns"].append("UNKNOWN_UNSAFE_REPLAY_POLICY")
    # Collect independent gates even when another gate already stops the step.
    if policy["follow"] == "manual":
        row["blockers"].append("MANUAL_POLICY")
    elif policy["follow"] == "unknown":
        row["unknowns"].append("UNKNOWN_FOLLOW_POLICY")
    if policy["followed"] >= policy["maximum"]:
        row["blockers"].append("BUDGET_EXHAUSTED")
    location = case["location"]
    if location["state"] == "absent":
        row["blockers"].append("NO_LOCATION")
    elif location["state"] == "unknown":
        row["unknowns"].append("UNKNOWN_LOCATION")
    elif location["origin_relation"] == "unknown":
        row["unknowns"].append("UNKNOWN_ORIGIN_RELATION")
    elif location["origin_relation"] == "cross":
        if policy["cross_origin"] == "deny":
            row["blockers"].append("CROSS_ORIGIN_DENIED")
        elif policy["cross_origin"] == "unknown":
            row["unknowns"].append("UNKNOWN_CROSS_ORIGIN_POLICY")
    row["blockers"] = sorted(set(row["blockers"]))
    row["unknowns"] = sorted(set(row["unknowns"]))
    row["reasons"] = sorted(set(row["blockers"] + row["unknowns"]))
    row["status"] = "UNSUPPORTED" if row["unknowns"] else "SUPPORTED"
    row["policy_decision"] = "WOULD_STOP" if row["blockers"] else (
        "UNRESOLVED" if row["unknowns"] else "WOULD_FOLLOW_ASSUMPTIONS")
    if row["policy_decision"] == "WOULD_FOLLOW_ASSUMPTIONS":
        row["next_step"] = dict(method=proposed, body_action=row["body_action"])
    return row


def evaluate(document):
    """Validate complete native input and return fresh hypothetical explanations."""
    validate(document)
    return {"version": 1, "results": [_case(case) for case in document["cases"]],
            "assumptions": list(ASSUMPTIONS)}
