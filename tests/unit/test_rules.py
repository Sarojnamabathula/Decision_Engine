import pytest
from rules.handlers import RuleHandlers

def test_rule_handler_gte():
    context = {"val": 5}
    assert RuleHandlers.evaluate_condition(context, "val", {"gte": 5}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"gte": 6}) is False

def test_rule_handler_lte():
    context = {"val": 5}
    assert RuleHandlers.evaluate_condition(context, "val", {"lte": 5}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"lte": 4}) is False

def test_rule_handler_eq():
    context = {"val": True}
    assert RuleHandlers.evaluate_condition(context, "val", {"eq": True}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"eq": False}) is False

def test_rule_handler_missing_field():
    context = {}
    assert RuleHandlers.evaluate_condition(context, "val", {"eq": True}) is False

def test_evaluate_rule_match():
    context = {"score": 0.9, "conf": 0.8}
    rule = {
        "condition": {
            "score": {"gte": 0.8},
            "conf": {"gte": 0.8}
        }
    }
    assert RuleHandlers.evaluate_rule(context, rule) is True

def test_evaluate_rule_mismatch():
    context = {"score": 0.9, "conf": 0.7}
    rule = {
        "condition": {
            "score": {"gte": 0.8},
            "conf": {"gte": 0.8}
        }
    }
    assert RuleHandlers.evaluate_rule(context, rule) is False

def test_evaluate_rule_empty_condition():
    context = {"score": 0.9}
    rule = {"condition": {}}
    assert RuleHandlers.evaluate_rule(context, rule) is True

def test_rule_handler_lt_gt():
    context = {"val": 5}
    assert RuleHandlers.evaluate_condition(context, "val", {"lt": 6}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"gt": 4}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"lt": 5}) is False
    assert RuleHandlers.evaluate_condition(context, "val", {"gt": 5}) is False

def test_rule_handler_neq():
    context = {"val": "test"}
    assert RuleHandlers.evaluate_condition(context, "val", {"neq": "other"}) is True
    assert RuleHandlers.evaluate_condition(context, "val", {"neq": "test"}) is False
