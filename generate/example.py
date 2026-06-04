example_json = {
    "pages": [
        {
        "id": 1,
        "parentId": None,
        "indexInParent": None,
        "name": "Home Page",
        "width": "1500",
        "backgroundColor": "#f2f5f8",
        "children": [
            {
            "id": 500,
            "parentId": 1,
            "indexInParent": 0,
            "type": "column-container",
            "hidden": False,
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "gap": 20
            },
            "children": [
                {
                "id": 10,
                "parentId": 500,
                "indexInParent": 0,
                "type": "navbar",
                "hidden": False,
                "style": {
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "space-between"
                },
                "children": [
                    {
                    "id": 12,
                    "parentId": 10,
                    "indexInParent": 0,
                    "type": "link",
                    "hidden": False,
                    "value": "Home Page"
                    },
                    {
                    "id": 16,
                    "parentId": 10,
                    "indexInParent": 1,
                    "type": "button",
                    "hidden": False,
                    "value": "Login"
                    }
                ]
                },
                {
                "id": 100,
                "parentId": 500,
                "indexInParent": 1,
                "type": "column-container",
                "hidden": False,
                "style": {
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": 15
                },
                "children": [
                    {
                    "id": 101,
                    "parentId": 100,
                    "indexInParent": 0,
                    "type": "text",
                    "hidden": False,
                    "value": "Welcome to Home Page!"
                    },
                    {
                    "id": 102,
                    "parentId": 100,
                    "indexInParent": 1,
                    "type": "repeating_group",
                    "hidden": False,
                    "gap": 20,
                    "style": {
                        "display": "flex",
                        "flexDirection": "row",
                        "flexWrap": "nowrap",
                        "overflowX": "auto"
                    },
                    "dataSource": {
                        "mode": "search",
                        "type": "products"
                    },
                    "itemWidth": "30%",
                    "children": [
                        {
                        "id": 2000,
                        "parentId": 102,
                        "indexInParent": 0,
                        "type": "card",
                        "hidden": False,
                        "style": {
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": 12,
                            "borderRadius": 16,
                            "boxShadow": "0 8px 20px rgba(0,0,0,0.12)",
                            "backgroundColor": "#fef3c7"
                        },
                        "children": [
                            {
                            "id": 105,
                            "parentId": 2000,
                            "indexInParent": 0,
                            "type": "image",
                            "hidden": False,
                            "src": "live/image1.jpg",
                            "style": {
                                "width": "100%",
                                "height": 180,
                                "objectFit": "cover",
                                "borderRadius": 12
                            },
                            "dynamicData": "parent_group.image"
                            },
                            {
                            "id": 106,
                            "parentId": 2000,
                            "indexInParent": 1,
                            "type": "text",
                            "hidden": False,
                            "value": "Repeated Item",
                            "style": {
                                "fontSize": 18,
                                "fontWeight": 700,
                                "color": "#1e293b"
                            },
                            "dynamicData": "parent_group.name"
                            },
                            {
                            "id": 107,
                            "parentId": 2000,
                            "indexInParent": 2,
                            "type": "text",
                            "hidden": False,
                            "value": "Description",
                            "style": {
                                "fontSize": 16,
                                "fontWeight": 500,
                                "color": "#475569"
                            },
                            "dynamicData": "parent_group.description"
                            },
                            {
                            "id": 108,
                            "parentId": 2000,
                            "indexInParent": 3,
                            "type": "text",
                            "hidden": False,
                            "value": "$58",
                            "style": {
                                "fontSize": 16,
                                "fontWeight": 700,
                                "color": "#dc2626"
                            },
                            "dynamicData": "parent_group.price"
                            },
                            {
                            "id": 109,
                            "parentId": 2000,
                            "indexInParent": 4,
                            "type": "button",
                            "hidden": False,
                            "value": "Buy Now",
                            "style": {
                                "backgroundColor": "#3b82f6",
                                "color": "#ffffff",
                                "borderRadius": 12,
                                "cursor": "pointer"
                            }
                            }
                        ]
                        }
                    ]
                    },
                    {
                    "id": 300,
                    "parentId": 100,
                    "indexInParent": 2,
                    "type": "banner",
                    "hidden": False,
                    "children": [
                        {
                        "id": 301,
                        "parentId": 300,
                        "indexInParent": 0,
                        "type": "text",
                        "hidden": False,
                        "value": "New Arrivals!"
                        },
                        {
                        "id": 302,
                        "parentId": 300,
                        "indexInParent": 1,
                        "type": "button",
                        "hidden": False,
                        "value": "Explore Now"
                        }
                    ]
                    }
                ]
                }
            ]
            }
        ]
        },
        {
        "id": 2,
        "parentId": None,
        "indexInParent": None,
        "name": "Analytics Page",
        "width": "1500",
        "backgroundColor": "#eef7ff",
        "children": [
            {
            "id": 400,
            "parentId": 2,
            "indexInParent": 0,
            "type": "column-container",
            "hidden": False,
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "gap": 20
            },
            "children": [
                {
                "id": 401,
                "parentId": 400,
                "indexInParent": 0,
                "type": "row-container",
                "hidden": False,
                "style": {
                    "display": "flex",
                    "gap": 15
                },
                "children": [
                    {
                    "id": 402,
                    "parentId": 401,
                    "indexInParent": 0,
                    "type": "label",
                    "hidden": False,
                    "value": "Select your preferences:"
                    },
                    {
                    "id": 405,
                    "parentId": 401,
                    "indexInParent": 1,
                    "type": "dropdown",
                    "hidden": False,
                    "options": [
                        { "label": "Dropdown A", "value": "d1" },
                        { "label": "Dropdown B", "value": "d2" }
                    ]
                    },
                    {
                    "id": 406,
                    "parentId": 401,
                    "indexInParent": 2,
                    "type": "checkbox",
                    "hidden": False,
                    "value": "Subscribe",
                    "checked": False
                    },
                    {
                    "id": 407,
                    "parentId": 401,
                    "indexInParent": 3,
                    "type": "radio",
                    "hidden": False,
                    "value": "Option 1",
                    "checked": True,
                    "name": "choice"
                    }
                ]
                },
                {
                "id": 410,
                "parentId": 400,
                "indexInParent": 1,
                "type": "piechart",
                "hidden": False,
                "data": {
                    "labels": ["Red", "Blue"],
                    "datasets": [
                    {
                        "data": [12, 19],
                        "backgroundColor": ["#f87171", "#34d399"]
                    }
                    ]
                }
                },
                {
                "id": 411,
                "parentId": 400,
                "indexInParent": 2,
                "type": "barchart",
                "hidden": False,
                "data": {
                    "labels": ["Q1", "Q2"],
                    "datasets": [
                    {
                        "data": [30, 45],
                        "backgroundColor": ["#60a5fa", "#fbbf24"]
                    }
                    ]
                }
                },
                {
                "id": 412,
                "parentId": 400,
                "indexInParent": 3,
                "type": "linechart",
                "hidden": False,
                "data": {
                    "labels": ["Jan", "Feb"],
                    "datasets": [
                    {
                        "data": [5, 10],
                        "borderColor": "#f87171",
                        "fill": False,
                        "tension": 0.4
                    }
                    ]
                }
                }
            ]
            }
        ]
        }
    ]
    }