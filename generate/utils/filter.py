# filter.py
from .operator import OPERATOR_MAP, resolve_value, match_condition
import random

def filter_json(records, conditions, request=None, modifier=None):
    results = []

    for item in records:
        ok = True

        for cond in conditions:
            field = cond.get("field")
            op_label = cond.get("operator")
            raw_value = cond.get("value")

            op = OPERATOR_MAP.get(op_label)
            value = resolve_value(raw_value, request)

            # Handle list inputs
            if op in ["in", "not_in"] and isinstance(value, str):
                value = [v.strip() for v in value.split(",")]

            if not match_condition(item, field, op, value):
                ok = False
                break

        if ok:
            results.append(item)

    # Modifier support
    if modifier == "first" and results:
        return results[:1]

    if modifier == "last" and results:
        return results[-1:]

    if modifier == "random" and results:
        return [random.choice(results)]

    return results
