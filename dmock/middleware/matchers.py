import re
import json as js
from dmock.models.models import Mock, Rules
from dmock.middleware.json_transform import flatten_json, get_wild_cards, is_subset, clear_wild_keys


def match_rule(rule: Rules, url: str = '', body: str = '', json: dict or list = None, headers: dict = None) -> bool:                            # type: ignore
    match rule.type:
        case "1-default":
            return True
        case "2-url":
            return _rule_str_compare(rule, url)
        case "3-body":
            return _rule_str_compare(rule, body)
        case "3-json":
            return _rule_json_compare(rule, json)
        case "4-header":
            return _rule_json_compare(rule, headers)
        case _:
            return False


def _rule_str_compare(rule: Rules, url_or_body: str) -> bool:
    match rule.operation:
        case "equals":
            return rule.key == url_or_body
        case "not_equals":
            return rule.key != url_or_body
        case "contains":
            return rule.key in url_or_body
        case "not_contains":
            return rule.key not in url_or_body
        case "in":
            return url_or_body in rule.key
        case "regex":
            return bool(re.match(rule.key, url_or_body))
        case "starts_with":
            return url_or_body.startswith(rule.key)
        case "ends_with":
            return url_or_body.endswith(rule.key)
        case _:
            return False


def _rule_json_compare(rule: Rules, data: dict or list) -> bool:                                                                                    # type: ignore
    rule_json = js.loads(rule.key)
    flat_request = flatten_json(data)
    flat_rule = flatten_json(rule_json)
    wild_keys = get_wild_cards(flat_rule)
    min_request = clear_wild_keys(flat_request, wild_keys)
    min_rule = clear_wild_keys(flat_rule, wild_keys)

    match rule.operation:
        case "equals":
            return min_request == min_rule
        case "contains":
            return is_subset(min_rule, min_request)
        case "in":
            return is_subset(min_request, min_rule)
        case _:
            return False
