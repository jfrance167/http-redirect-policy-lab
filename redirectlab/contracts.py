"""Strict bounded input admission, adapted from Jake's MIT range lab.

Native types are checked by identity before any caller-controlled operation.
"""

import json
import re

INPUT_BYTES = 65_536
OUTPUT_BYTES = 524_288
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", re.ASCII)
FEATURE = re.compile(r"[a-z][a-z0-9-]{0,31}", re.ASCII)
METHOD = re.compile(r"[!#$%&'*+.^_`|~0-9A-Z-]{1,16}", re.ASCII)


class Invalid(ValueError):
    """An invalid document or failed delivery, with a fixed diagnostic code."""


def text(value, limit=256):
    if type(value) is not str or len(value) > limit:
        raise Invalid("TEXT_TYPE_OR_LIMIT")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise Invalid("TEXT_CONTROL")
    try:
        value.encode("utf-8", "strict")
    except UnicodeError as exc:
        raise Invalid("INVALID_UNICODE") from exc


def _walk(value, depth, budget, active):
    kind = type(value)
    # Equality against a tuple/set of types can itself invoke exotic metaclasses.
    if not (kind is dict or kind is list or kind is str or kind is int
            or kind is bool or value is None):
        raise Invalid("TREE_TYPE")
    budget[0] += 1
    if budget[0] > 5_000:
        raise Invalid("NODE_LIMIT")
    if (kind is dict or kind is list) and depth > 8:
        raise Invalid("TREE_DEPTH")
    if kind is str:
        text(value)
    elif kind is int:
        if value < -9_999_999_999 or value > 9_999_999_999:
            raise Invalid("INTEGER_TOKEN_BOUND")
    elif kind is dict or kind is list:
        if id(value) in active:
            raise Invalid("TREE_CYCLE")
        if len(value) > 100:
            raise Invalid("CONTAINER_LIMIT")
        active.add(id(value))
        try:
            if kind is dict:
                for key, item in value.items():
                    if type(key) is not str:
                        raise Invalid("TREE_TYPE")
                    budget[0] += 1
                    if budget[0] > 5_000:
                        raise Invalid("NODE_LIMIT")
                    text(key, 64)
                    _walk(item, depth + 1, budget, active)
            else:
                for item in value:
                    _walk(item, depth + 1, budget, active)
        finally:
            active.remove(id(value))


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("DUPLICATE_KEY")
        result[key] = value
    return result


def _integer(source):
    if len(source.lstrip("-")) > 10:
        raise Invalid("INTEGER_TOKEN_BOUND")
    return int(source)


def _noninteger(_source):
    raise Invalid("NONINTEGER_JSON")


def parse(raw):
    """Parse bounded UTF8 JSON bytes; evaluate performs full native/schema admission."""
    if type(raw) is not bytes or len(raw) > INPUT_BYTES:
        raise Invalid("INPUT_LIMIT")
    try:
        source = raw.decode("utf-8", "strict")
        quoted = escaped = False
        depth = 0
        for char in source:
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char in "[{":
                depth += 1
                if depth > 8:
                    raise Invalid("JSON_DEPTH")
            elif char in "]}":
                depth -= 1
        return json.loads(source, object_pairs_hook=_pairs, parse_int=_integer,
                          parse_float=_noninteger, parse_constant=_noninteger)
    except (UnicodeError, ValueError, RecursionError) as exc:
        if type(exc) is Invalid:
            raise
        raise Invalid("INVALID_JSON") from exc


def _keys(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise Invalid("SCHEMA")


def _list(value, lower, upper, code):
    if type(value) is not list or not lower <= len(value) <= upper:
        raise Invalid(code)


def _choice(value, choices, code):
    if type(value) is not str or value not in choices:
        raise Invalid(code)


def _id(value):
    text(value, 64)
    if not IDENTIFIER.fullmatch(value):
        raise Invalid("ID_FORMAT")


def _count(value, code):
    if type(value) is not int or not 0 <= value <= 8:
        raise Invalid(code)


def validate(document):
    """Validate every exact-builtin case before any semantic or policy shortcut."""
    _walk(document, 1, [0], set())
    if len(json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > INPUT_BYTES:
        raise Invalid("INPUT_LIMIT")
    _keys(document, ("version", "cases"))
    if type(document["version"]) is not int or document["version"] != 1:
        raise Invalid("VERSION")
    _list(document["cases"], 1, 40, "CASE_COUNT")
    seen = set()
    for case in document["cases"]:
        _keys(case, ("id", "response_status", "method", "body", "location", "policy", "unsupported_features"))
        _id(case["id"])
        if case["id"] in seen:
            raise Invalid("DUPLICATE_CASE_ID")
        seen.add(case["id"])
        status = case["response_status"]
        if type(status) is not int or not 100 <= status <= 599:
            raise Invalid("STATUS")
        if type(case["method"]) is not str or not METHOD.fullmatch(case["method"]):
            raise Invalid("METHOD")
        _choice(case["body"], ("absent", "replayable", "nonreplayable", "unknown"), "BODY")
        if case["method"] in ("GET", "HEAD") and case["body"] != "absent":
            raise Invalid("BODY_SHAPE")
        location = case["location"]
        _keys(location, ("state", "origin_relation"))
        _choice(location["state"], ("absent", "present", "unknown"), "LOCATION_STATE")
        if location["state"] == "present":
            _choice(location["origin_relation"], ("same", "cross", "unknown"), "LOCATION_RELATION")
        elif location["origin_relation"] is not None:
            raise Invalid("LOCATION_SHAPE")
        policy = case["policy"]
        _keys(policy, ("follow", "post_301_302", "unsafe_replay", "cross_origin", "followed", "maximum"))
        for field, options, code in (
            ("follow", ("automatic", "manual", "unknown"), "FOLLOW_POLICY"),
            ("post_301_302", ("get", "preserve", "unknown"), "POST_POLICY"),
            ("unsafe_replay", ("allow", "deny", "unknown"), "UNSAFE_POLICY"),
            ("cross_origin", ("allow", "deny", "unknown"), "CROSS_POLICY"),
        ):
            _choice(policy[field], options, code)
        _count(policy["followed"], "FOLLOWED")
        _count(policy["maximum"], "MAXIMUM")
        features = case["unsupported_features"]
        _list(features, 0, 8, "FEATURE_COUNT")
        names = set()
        for feature in features:
            text(feature, 32)
            if not FEATURE.fullmatch(feature):
                raise Invalid("FEATURE")
            if feature in names:
                raise Invalid("DUPLICATE_FEATURE")
            names.add(feature)
