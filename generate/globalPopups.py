globalPopups = {
    "id": "globalPopupsContainer",
    "type": "container",
    "children": [
        {
            "id": "overlay_backdrop",
            "type": "container",
            "renderMode": "overlay",
            "isOpen": False,
            "style": {
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100vw",
                "height": "100vh",
                "backgroundColor": "rgba(0,0,0,0.35)",
                "zIndex": 999
            },
            "children": []
        },
        {
            "id": "login_popup",
            "type": "popup",
            "renderMode": "overlay",
            "isOpen": False,
            "style": {
                "width": 420,
                "minHeight": 280,
                "paddingTop": 24,
                "paddingBottom": 24,
                "paddingLeft": 24,
                "paddingRight": 24,
                "gap": 16,
                "backgroundColor": "#ffffff",
                "borderRadius": 12,
                "zIndex": 1000
            },
            "children": [
                {
                    "id": "login_title",
                    "type": "text",
                    "value": "Login",
                    "style": {
                        "fontSize": 22,
                        "fontWeight": 600,
                        "textAlign": "center"
                    }
                },
                {
                    "id": "login_email",
                    "type": "input",
                    "placeholder": "Email"
                },
                {
                    "id": "login_password",
                    "type": "input",
                    "inputType": "password",
                    "placeholder": "Password"
                },
                
                {
                    "id": "login_submit",
                    "type": "button",
                    "value": "Login",
                    "style": {
                        "backgroundColor": "#2563eb",
                        "color": "#ffffff"
                    }
                }
            ]
        },
        {
            "id": "signup_popup",
            "type": "popup",
            "renderMode": "overlay",
            "isOpen": False,
            "style": {
                "width": 420,
                "minHeight": 320,
                "paddingTop": 24,
                "paddingBottom": 24,
                "paddingLeft": 24,
                "paddingRight": 24,
                "gap": 16,
                "backgroundColor": "#ffffff",
                "borderRadius": 12,
                "zIndex": 1000
            },
            "children": [
                {
                    "id": "signup_title",
                    "type": "text",
                    "value": "Create Account",
                    "style": {
                        "fontSize": 22,
                        "fontWeight": 600,
                        "textAlign": "center"
                    }
                },
                {
                    "id": "signup_email",
                    "type": "input",
                    "placeholder": "Email"
                },
                {
                    "id": "signup_password",
                    "type": "input",
                    "inputType": "password",
                    "placeholder": "Password"
                },
                {
                    "id": "signup_confirm_password",
                    "type": "input",
                    "inputType": "confirm_password",
                    "placeholder": "confirm_Password"
                },
                {
                    "id": "signup_submit",
                    "type": "button",
                    "value": "Sign Up",
                    "style": {
                        "backgroundColor": "#16a34a",
                        "color": "#ffffff"
                    }
                }
            ]
        },
        {
    "id": "contact_popup",
    "type": "popup",
    "renderMode": "overlay",
    "isOpen": False,
    "style": {
        "width": 420,
        "minHeight": 260,
        "paddingTop": 24,
        "paddingBottom": 24,
        "paddingLeft": 24,
        "paddingRight": 24,
        "gap": 16,
        "backgroundColor": "#ffffff",
        "borderRadius": 12,
        "zIndex": 1000
    },
    "children": [
        {
            "id": "contact_title",
            "type": "text",
            "value": "Contact Details",
            "style": {
                "fontSize": 22,
                "fontWeight": 600,
                "textAlign": "center"
            }
        },
        {
            "id": "contact_name",
            "type": "input",
            "placeholder": "Full Name"
        },
        {
            "id": "contact_phone",
            "type": "input",
            "inputType": "tel",
            "placeholder": "Phone Number"
        },
        {
            "id": "contact_submit",
            "type": "button",
            "value": "Submit",
            "style": {
                "backgroundColor": "#0ea5e9",
                "color": "#ffffff"
            }
        }
    ]
}

    ]
}
