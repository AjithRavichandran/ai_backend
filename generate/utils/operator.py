OPERATOR_MAP = {
    "= (equals)": "eq",
    "!= (not equal)": "neq",
    "< (less than)": "lt",
    "> (greater than)": "gt",
    "≤ (less or equal)": "lte",
    "≥ (greater or equal)": "gte",
    "contains": "contains",
    "doesn't contain": "not_contains",
    "starts with": "starts",
    "ends with": "ends",
    "is empty": "empty",
    "isn't empty": "not_empty",
    "is in": "in",
    "isn't in": "not_in",
}

def resolve_value(value, request):
    if not request:
        return value

    user = getattr(request, "user", None)

    if value == "currentUser.id":
        return getattr(user, "id", None)

    if value == "currentUser.email":
        return getattr(user, "email", None)

    return value


def match_condition(item, field, op, value):
    item_value = item.get(field)

    # Normalize types for numbers
    def to_number(v):
        try:
            return float(v)
        except:
            return v

    if op in ["lt", "gt", "lte", "gte"]:
        item_value = to_number(item_value)
        value = to_number(value)

    if op == "eq":
        return item_value == value

    if op == "neq":
        return item_value != value

    if op == "lt":
        return item_value is not None and value is not None and item_value < value

    if op == "gt":
        return item_value is not None and value is not None and item_value > value

    if op == "lte":
        return item_value is not None and value is not None and item_value <= value

    if op == "gte":
        return item_value is not None and value is not None and item_value >= value

    if op == "contains":
        return value is not None and str(value).lower() in str(item_value or "").lower()

    if op == "not_contains":
        return value is not None and str(value).lower() not in str(item_value or "").lower()

    if op == "starts":
        return str(item_value or "").startswith(str(value))

    if op == "ends":
        return str(item_value or "").endswith(str(value))

    if op == "empty":
        return item_value in [None, "", [], {}]

    if op == "not_empty":
        return item_value not in [None, "", [], {}]

    if op == "in":
        return item_value in (value or [])

    if op == "not_in":
        return item_value not in (value or [])

    return False
