#navbar_helpers.py
import time

def add_navbar_buttons(page_json, start_id=None):
    """
    Find navbar(s) in the page JSON and add login/logout/signup buttons.
    IDs are dynamically generated to avoid conflicts.
    """
    # Initialize starting ID
    if start_id is None:
        start_id = int(time.time() * 1000) % 100000  # e.g., 5-digit starting ID

    def traverse_and_add(children, next_id):
        for child in children:
            if child.get("type") == "navbar":
                # Define buttons with dynamic IDs
                buttons = [
                    {
                        "id": next_id,
                        "type": "button",
                        "value": "Login",
                        "hidden": True,
                        "parentId": child["id"],
                        "indexInParent": len(child["children"]),
                        "style": {
                            "paddingTop": "5",
                            "paddingBottom": "5",
                            "paddingLeft": "5",
                            "paddingRight": "5",
                            "backgroundColor": "#10b981",
                            "color": "#ffffff",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": 16,
                            "fontWeight": 500
                        },
                        "props": {"onClick": "navigateToLogin"}
                    },
                    {
                        "id": next_id + 1,
                        "type": "button",
                        "value": "Logout",
                        "hidden": True,
                        "parentId": child["id"],
                        "indexInParent": len(child["children"]) + 1,
                        "style": {
                            "paddingTop": "5",
                            "paddingBottom": "5",
                            "paddingLeft": "5",
                            "paddingRight": "5",
                            "backgroundColor": "#ef4444",
                            "color": "#ffffff",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": 16,
                            "fontWeight": 500
                        },
                        "props": {"onClick": "logoutUser"}
                    },
                    {
                        "id": next_id + 2,
                        "type": "button",
                        "value": "Signup",
                        "hidden": True,
                        "parentId": child["id"],
                        "indexInParent": len(child["children"]) + 2,
                        "style": {
                            "paddingTop": "5",
                            "paddingBottom": "5",
                            "paddingLeft": "5",
                            "paddingRight": "5",
                            "backgroundColor": "#3b82f6",
                            "color": "#ffffff",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": 16,
                            "fontWeight": 500
                        },
                        "props": {"onClick": "navigateToSignup"}
                    }
                ]
                child["children"].extend(buttons)
                next_id += 3  # increment for next buttons

            # Recurse for nested children
            if "children" in child:
                next_id = traverse_and_add(child["children"], next_id)

        return next_id

    # Start traversing from top-level pages
    traverse_and_add(page_json.get("pages", []), start_id)
    return page_json
