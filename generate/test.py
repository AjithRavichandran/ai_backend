page = {
  "activePageId": 1,
  "pages": [
  {
    "id": 1,
    "name": "Home Page",
    "width": "1500",
    "backgroundColor": "#f2f5f8",
    "parentId": None,
    "indexInParent": 0,
    "children": [
      {
        "id": 500,
        "type": "column-container",
        "hidden": False,
        "parentId": 1,
        "indexInParent": 0,
        "style": {
          "width": "100%",
          "gap": 20,
          "display": "flex",
          "flexDirection": "column",
          "alignItems": "stretch",
          "paddingTop": 20,
          "paddingBottom": 20,
          "paddingLeft": 20,
          "paddingRight": 20,
          "backgroundColor": "#eef2f7"
        },
        "children": [
          {
            "id": 10,
            "type": "navbar","hidden": False,
            "parentId": 500,
            "indexInParent": 0,
            "style": {
              "display": "flex",
              "flexDirection": "row",
              "alignItems": "center",
              "justifyContent": "space-between",
              "backgroundColor": "#ffffff",
              "boxShadow": "0 6px 18px rgba(0,0,0,0.1)",
              "paddingTop": 12,
              "paddingBottom": 12,
              "paddingLeft": 20,
              "paddingRight": 20,
              "borderRadius": 12
            },
            "children": [
              {
                "id": 12,
                "type": "link",
                "value": "Home Page","hidden": True,
                "parentId": 10,
                "indexInParent": 1,
                "style": {
                  "fontSize": 16,
                  "fontWeight": 600,
                  "color": "#1d4ed8",
                  "textDecoration": "none",
                  "borderRadius": 8,
                  "transition": "all 0.2s",
                  "hoverBackgroundColor": "#e0e7ff"
                }
              },
              {
                "id": 13,
                "type": "link",
                "value": "Second Page","hidden": False,
                "parentId": 10,
                "indexInParent": 2,
                "style": {
                  "fontSize": 16,
                  "fontWeight": 600,
                  "color": "#1d4ed8",
                  "textDecoration": "none",
                  "borderRadius": 8,
                  "transition": "all 0.2s",
                  "hoverBackgroundColor": "#e0e7ff"
                }
              },
              {
                "id": 17,
                "type": "search","hidden": False,
                "parentId": 10,
                "indexInParent": 3,
                "style": {
                  "display": "flex",
                  "flexDirection": "row",
                  "alignItems": "center",
                  "gap": "8px",
                  "border": "1px solid #ccc",
                  "borderRadius": "12px",
                  "backgroundColor": "#f9fafb"
                },
                "children": [
                  {
                    "id": 18,
                    "type": "input",
                    "placeholder": "Search...","hidden": False,
                    "parentId": 17,
                    "indexInParent": 0,
                    "style": {
                      "border": "none",
                      "outline": "none",
                      "flexGrow": 1,
                      "backgroundColor": "#f9fafb",
                      "borderRadius": "8px"
                    },
                    "props": {
                      "onChange": "onSearchChange",
                      "onSubmit": "onSearchSubmit"
                    }
                  },
                ]
              },
              {
  "id": 20,
  "type": "button",
  "value": "Login","hidden": False,
  "parentId": 10,
  "indexInParent": 4,
  "style": {
    "paddingTop": 5,
                          "paddingBottom": 5,
                          "paddingLeft": 5,
                          "paddingRight": 5,
    "backgroundColor": "#10b981",
    "color": "#ffffff",
    "border": "none",
    "borderRadius": "6px",
    "cursor": "pointer",
    "fontSize": 16,
    "fontWeight": 500
  },
  "props": {
    "onClick": "navigateToLogin"
  }
}

            ]
          },
          {
            "id": 100,
            "type": "column-container","hidden": False,
            "parentId": 500,
            "indexInParent": 1,
            "style": {
              "display": "flex",
              "flexDirection": "column",
              "gap": 25,
              "backgroundColor": "#ffffff",
              "borderRadius": 16,
              "width": "100%",
              "paddingTop": 20,
              "paddingBottom": 20,
              "paddingLeft": 20,
              "paddingRight": 20,
              "boxShadow": "0 6px 18px rgba(0,0,0,0.08)"
            },
            "children": [
              {
                "id": 101,
                "type": "text",
                "value": "Welcome to Home Page!","hidden": False,
                "parentId": 100,
                "indexInParent": 0,
                "style": {
                  "fontSize": 28,
                  "fontWeight": 800,
                  "color": "#1f2937",
                  "textAlign": "left",
                  "alignSelf": "flex-start",
                  "marginBottom": 15
                }
              },
              {
                "id": 102,
                "type": "repeating_group","hidden": False,
                "itemWidth": "30%",
                "gap": 20,
                "typeOfContent": "products",
                "parentId": 100,
                "indexInParent": 1,
                "dataSource": {
                },
                "style": {
                  "display": "flex",
                  "flexDirection": "row",
                  "flexWrap": "nowrap",
                  "overflowX": "auto",
                  "paddingTop": 10,
                  "paddingBottom": 10,
                  "paddingLeft": 10,
                  "paddingRight": 10
                },
                "children": [
                  {
                    "id": 2000,
                    "type": "card","hidden": False,
                    "parentId": 102,
                    "indexInParent": 0,
                    "style": {
                      "display": "flex",
                      "flexDirection": "column",
                      "gap": 12,
                      "backgroundColor": "#fef3c7",
                      "borderRadius": 16,
                      "boxShadow": "0 8px 20px rgba(0,0,0,0.12)",
                      "alignItems": "center",
                      "paddingTop": 12,
                      "paddingBottom": 12,
                      "paddingLeft": 12,
                      "paddingRight": 12,
                      "transition": "transform 0.2s",
                      "hoverTransform": "scale(1.05)"
                    },
                    "children": [
                      {
                        "id": 105,
                        "type": "image","hidden": False,
                        "src": "live/image1.jpg",
                        "parentId": 2000,
                        "indexInParent": 0,
                        "dataFields": ["src"],
                        "style": {
                          "width": "100%",
                          "height": 180,
                          "objectFit": "cover",
                          "borderRadius": 12
                        }
                      },
                      {
                        "id": 106,
                        "type": "text",
                        "value": "Repeated Item","hidden": False,
                        "parentId": 2000,
                        "indexInParent": 1,
                        "dataFields": ["name"],
                        "style": {
                          "fontSize": 18,
                          "fontWeight": 700,
                          "color": "#1e293b",
                          "textAlign": "center",
                          "alignSelf": "flex-start"
                        }
                      },
                      {
                        "id": 107,
                        "type": "text","hidden": False,
                        "value": "Description",
                        "parentId": 2000,
                        "indexInParent": 2,
                        "dataFields": ["description"],
                        "style": {
                          "fontSize": 16,
                          "fontWeight": 500,
                          "color": "#475569",
                          "textAlign": "center",
                          "alignSelf": "flex-start"
                        }
                      },
                      {
                        "id": 108,
                        "type": "text",
                        "value": "$58","hidden": False,
                        "parentId": 2000,
                        "indexInParent": 3,
                        "dataFields": ["price"],
                        "style": {
                          "fontSize": 16,
                          "fontWeight": 700,
                          "color": "#dc2626",
                          "textAlign": "center",
                          "alignSelf": "flex-start"
                        }
                      },
                      {
                        "id": 109,
                        "type": "button",
                        "value": "Buy Now",
                        "parentId": 2000,"hidden": False,
                        "indexInParent": 4,
                        "style": {
                          "paddingTop": 12,
                          "paddingBottom": 12,
                          "paddingLeft": 20,
                          "paddingRight": 20,
                          "backgroundColor": "#3b82f6",
                          "color": "#ffffff",
                          "borderRadius": 12,
                          "cursor": "pointer",
                          "alignSelf": "center",
                          "border": "none",
                          "transition": "all 0.2s",
                          "hoverBackgroundColor": "#2563eb"
                        },
                        "props": {
                          "onClick": "onBuyNow"
                        }
                      }
                    ]
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
  "name": "Second Page",
  "width": "100%",
  "backgroundColor": "#eef7ff",
  "parentId": None,
  "indexInParent": 1,
  "children": [
    {
      "id": 3000,
      "type": "column-container",
      "parentId": 2,"hidden": False,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "gap": 20,
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "stretch",
        "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

      },
      "children": [
        {
          "id": 3001,
          "type": "navbar",
          "parentId": 3000,"hidden": False,
          "indexInParent": 0,
          "style": {
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "justifyContent": "space-between",
            "backgroundColor": "#1e40af",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

          },
          "children": [
            {
              "id": 3003,
              "type": "link",
              "value": "Home Page","hidden": False,
              "parentId": 3001,
              "indexInParent": 1,
              "style": {
                "fontSize": 16,
                "fontWeight": 500,
                "color": "#007BFF",
                "textDecoration": "none"
              }
            },
            {
              "id": 3004,
              "type": "link",
              "value": "Second Page","hidden": False,
              "parentId": 3001,
              "indexInParent": 2,
              "style": {
                "fontSize": 16,
                "fontWeight": 500,
                "color": "#007BFF",
                "textDecoration": "none"
              }
            },
            {
              "id": 3005,
              "type": "search",
              "parentId": 3001,
              "indexInParent": 3,"hidden": False,
              "style": {
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "center",
                "gap": "8px",
                "border": "1px solid #ccc",
                "borderRadius": "8px",
                "padding": "4px 8px"
              },
              "children": [
                {
                  "id": 3006,
                  "type": "input","hidden": False,
                  "placeholder": "Search...",
                  "parentId": 3005,
                  "indexInParent": 0,
                  "style": {
                    "padding": "8px 12px",
                    "border": "none",
                    "outline": "none",
                    "flexGrow": 1
                  },
                  "props": {
                    "onChange": "onSearchChange",
                    "onSubmit": "onSearchSubmit"
                  }
                },
                {
                  "id": 3007,
                  "type": "icon","hidden": False,
                  "value": "search",
                  "parentId": 3005,
                  "indexInParent": 1,
                  "style": {
                    "cursor": "pointer",
                    "color": "#666"
                  },
                  "props": {
                    "onClick": "submitSearch"
                  }
                }
                
              ]
            }
          ]
        },
        {
          "id": 9001,
          "type": "row-container","hidden": False,
          "parentId": 3000,
          "indexInParent": 1,
          "width": "100%",
          "style": { "display": "flex", "flexDirection": "row", "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10
 },
          "children": [
            {
              "id": 3008,
              "type": "header",
              "parentId": 9001,"hidden": False,
              "indexInParent": 0,
              "width": "100%",
              "style": {
                
                "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10
,
                "backgroundColor": "#2563eb",
                "color": "#fff",
                "alignItems": "center",
                "justifyContent": "center",
                "display": "flex",
                 "flexDirection": "row"
              },
              "children": [
                {
                  "id": 3009,
                  "type": "text","hidden": False,
                  "value": "Page 2 Header",
                  "parentId": 3008,
                  "indexInParent": 0,
                  "style": {
                    "fontSize": 20,
                    "fontWeight": 700,
                    "color": "#fff"
                  }
                },
                {
                  "id": 3010,
                  "type": "button",
                  "value": "Sign Up","hidden": False,
                  "parentId": 3008,
                  "indexInParent": 1,
                  "style": {
                    "backgroundColor": "#fff",
                    "color": "#2563eb",
                    "borderRadius": 6,
                    "cursor": "pointer",
                    "border": "none",

                  }
                }
              ]
            },
            {
              "id": 30085,"hidden": False,
              "type": "header",
              "parentId": 9001,
              "indexInParent": 1,
              "style": {
                "width": "100%",
                "backgroundColor": "#2563eb",
                "color": "#fff",
                "alignItems": "center",
                "justifyContent": "center",
                "display": "flex", "flexDirection": "column",
                "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

              },
              "children": [
                {
                  "id": 30096,
                  "type": "text","hidden": False,
                  "value": "Page 2 Header",
                  "parentId": 30085,
                  "indexInParent": 0,
                  "style": {
                    "fontSize": 20,
                    "fontWeight": 700,
                    "color": "#fff"
                  }
                },
                {
                  "id": 30106,
                  "type": "button","hidden": False,
                  "value": "Sign Up",
                  "parentId": 30085,
                  "indexInParent": 1,
                  "style": {
                    "backgroundColor": "#fff",
                    "color": "#2563eb",
                    "borderRadius": 6,
                    "cursor": "pointer",
                    "border": "none"
                  }
                }
              ]
            }
          ]
        },
        {
          "id": 3011,
          "type": "banner",
          "parentId": 3000,
          "indexInParent": 2,"hidden": False,
          "style": {
            "width": "100%",
            "backgroundColor": "#fbbf24",
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "justifyContent": "center",
            "borderRadius": 12,
            "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

          },
          "children": [
            {
              "id": 3012,
              "type": "text",
              "value": "New Arrivals!","hidden": False,
              "parentId": 3011,
              "indexInParent": 0,
              "style": {
                "fontSize": 28,
                "fontWeight": 700,
                "color": "#1a202c",
                "textAlign": "center"
              }
            },
            {
              "id": 3013,"hidden": False,
              "type": "button",
              "value": "Explore Now",
              "parentId": 3011,
              "indexInParent": 1,
              "style": {
                "backgroundColor": "#2563eb",
                "color": "#fff",
                "borderRadius": 8,
                "cursor": "pointer",
                "border": "none"
              }
            }
          ]
        },
        {
          "id": 9100,
          "type": "column-container","hidden": False,
          "parentId": 3000,
          "indexInParent": 3,
          "style": { "display": "flex", "flexDirection": "column", "gap": 10, "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10
 },
          "children": [
            {
              "id": 3014,
              "type": "label","hidden": False,
              "value": "Select your preferences:",
              "style": { "fontSize": 16, "fontWeight": 500, "color": "#1a202c" }
            },
            {
              "id": 3017,
              "type": "dropdown","hidden": False,
              "value": "d1",
              "options": [
                { "label": "Dropdown A", "value": "d1" },
                { "label": "Dropdown B", "value": "d2" },
                { "label": "Dropdown C", "value": "d3" }
              ],
              "style": { "width": 200, "padding": "6px 10px", "borderRadius": 6, "border": "1px solid #ccc" }
            },
            {
              "id": 3018,
              "type": "checkbox","hidden": False,
              "value": "Subscribe to updates",
              "checked": False
            },
            {
              "id": 3019,
              "type": "radio","hidden": False,
              "value": "Option 1",
              "checked": True,
              "name": "choice"
            },
            {
              "id": 3020,
              "type": "radio","hidden": False,
              "value": "Option 2",
              "checked": False,
              "name": "choice"
            }
          ]
        },
        {
          "id": 3021,
          "type": "repeating_group","hidden": False,
          "itemWidth": "30%",
          "gap": 15,
          "parentId": 3000,
          "indexInParent": 4,
          "dataSource": "products",
          "style": {
            "display": "flex",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            
            "overflowX": "auto",
            "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

          },
          "itemStyle": {
            "backgroundColor": "#ffffff",
            "padding": 15,
            "borderRadius": 12,
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
            "minWidth": 250
          },
          "children": [
            {
              "id": 3022,"hidden": False,
              "type": "card",
              "parentId": 3021,
              "indexInParent": 0,
              "style": {
                "display": "flex",
                "flexDirection": "column",
                "gap": 10,
                "backgroundColor": "#d8d8f0",
                "borderRadius": 12,
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "alignItems": "center",
                "paddingTop": 10,
"paddingBottom": 10,
"paddingLeft": 10,
"paddingRight": 10

              },
              "children": [
                {
                  "id": 3023,"hidden": False,
                  "type": "image",
                  "src": "Product1",
                  "parentId": 3022,
                  "indexInParent": 0,
                  "dataFields": ["src"],
                  "style": {
                    "width": "100%",
                    "height": 150,
                    "objectFit": "cover",
                    
                    "borderRadius": 12
                  }
                },
                {
                  "id": 3024,
                  "type": "text","hidden": False,
                  "value": "Featured Item",
                  "parentId": 3022,
                  "indexInParent": 1,
                  "dataFields": ["name"],
                  "style": {
                    "fontSize": 16,
                    "fontWeight": 600,
                    "color": "#1a202c",
                    "textAlign": "center",
                    "alignSelf": "flex-start"
                  }
                },
                {
                  "id": 3025,
                  "type": "button","hidden": False,
                  "value": "Buy Now",
                  "parentId": 3022,
                  "indexInParent": 2,
                  "style": {
                    "backgroundColor": "#007BFF",
                    "color": "#fff",
                    "borderRadius": 8,
                    "cursor": "pointer",
                    "alignSelf": "center",
                    "border": "none"
                  },
                  "props": {
                    "onClick": "onBuyNow"
                  }
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
  "id": 3,
  "name": "Login Page",
  "width": "100%",
  "backgroundColor": "#f5f7fa",
  "parentId": None,
  "indexInParent": 2,
  "children": [
    {
      "id": 91000,
      "type": "column-container",
      "parentId": 3,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "paddingTop": 20,
        "paddingBottom": 20,
        "paddingLeft": 20,
        "paddingRight": 20,
        "flexDirection": "column"
      },
      "children": [
        {
  "id": 9101,
  "type": "column-container",
  "parentId": 91000,
  "indexInParent": 0,
  "style": {
    "width": 400,
    "backgroundColor": "#ffffff",
    "paddingTop": 30,
    "paddingBottom": 30,
    "paddingLeft": 30,
    "paddingRight": 30,
    "borderRadius": 16,
    "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
    "gap": 20,
    "display": "flex",
    "flexDirection": "column",

    "alignSelf": "center"
  },
          "children": [
            {
              "id": 9102,
              "type": "text",
              "parentId": 9101,
              "indexInParent": 0,
              "value": "Welcome Back 👋",
              "style": {
                "fontSize": 26,
                "fontWeight": "600",
                "textAlign": "center",
                "marginBottom": 10
              }
            },
            {
              "id": 9103,
              "type": "input",
              "parentId": 9101,
              "indexInParent": 1,
              "placeholder": "Email",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "loginEmailChange" }
            },
            {
              "id": 9104,
              "type": "input",
              "parentId": 9101,
              "indexInParent": 2,
              "placeholder": "Password",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "loginPasswordChange" }
            },
            {
              "id": 9105,
              "type": "button",
              "parentId": 9101,
              "indexInParent": 3,
              "value": "Login",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "backgroundColor": "#4a90e2",
                "color": "#ffffff",
                "fontWeight": "600",
                "borderRadius": 10,
                "cursor": "pointer"
              },
              "props": { "onClick": "onLoginSubmit" }
            },
            {
              "id": 9106,
              "type": "text",
              "parentId": 9101,
              "indexInParent": 4,
              "value": "Don't have an account? ",
              "style": {
                "textAlign": "center",
                "marginTop": 10
              }
            },
            {
              "id": 9107,
              "type": "button",
              "parentId": 9101,
              "indexInParent": 5,
              "value": "Create Account",
              "style": {
                "backgroundColor": "transparent",
                "color": "#4a90e2",
                "textDecoration": "underline",
                "fontWeight": "600",
                "cursor": "pointer",
                "marginLeft": "auto",
                "marginRight": "auto"
              },
              "props": { "onClick": "goToSignupPage" }
            }
          ]
        }
      ]
    }
  ]
}
,{
  "id": 4,
  "name": "Signup Page",
  "width": "100%",
  "backgroundColor": "#f5f7fa",
  "parentId": None,
  "indexInParent": 3,
  "children": [
    {
      "id": 92000,
      "type": "column-container",
      "parentId": 4,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "paddingTop": 20,
        "paddingBottom": 20,
        "paddingLeft": 20,
        "paddingRight": 20,
        "flexDirection": "column"
      },
      "children": [
        {
          "id": 9201,
          "type": "column-container",
          "parentId": 92000,
          "indexInParent": 0,
          "style": {
            "width": 400,
            "backgroundColor": "#ffffff",
            "paddingTop": 30,
            "paddingBottom": 30,
            "paddingLeft": 30,
            "paddingRight": 30,
            "borderRadius": 16,
            "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
            "gap": 20,
            "display": "flex",
            "flexDirection": "column",
            "alignSelf": "center"
          },
          "children": [
            {
              "id": 9202,
              "type": "text",
              "parentId": 9201,
              "indexInParent": 0,
              "value": "Create Account ✨",
              "style": {
                "fontSize": 26,
                "fontWeight": "600",
                "textAlign": "center",
                "marginBottom": 10
              }
            },
            {
              "id": 9203,
              "type": "input",
              "parentId": 9201,
              "indexInParent": 1,
              "placeholder": "Full Name",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "signupNameChange" }
            },
            {
  "id": 9204,
  "type": "input",
  "parentId": 9201,
  "indexInParent": 2,
  "placeholder": "Username",
  "style": {
    "width": "100%",
    "paddingTop": 14,
    "paddingBottom": 14,
    "paddingLeft": 14,
    "paddingRight": 14,
    "borderRadius": 10,
    "border": "1px solid #ccc"
  },
  "props": { "onChange": "signupUsernameChange" }
},

            {
              "id": 9205,
              "type": "input",
              "parentId": 9201,
              "indexInParent": 3,
              "placeholder": "Email",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "signupEmailChange" }
            },
            {
              "id": 9206,
              "type": "input",
              "parentId": 9201,
              "indexInParent": 4,
              "placeholder": "Password",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "signupPasswordChange" }
            },
            {
              "id": 9207,
              "type": "input",
              "parentId": 9201,
              "indexInParent": 5,
              "placeholder": "Confirm Password",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "signupConfirmPasswordChange" }
            },
            {
              "id": 9208,
              "type": "button",
              "parentId": 9201,
              "indexInParent": 6,
              "value": "Signup",
              "style": {
                "width": "100%",
                "paddingTop": 14,
                "paddingBottom": 14,
                "paddingLeft": 14,
                "paddingRight": 14,
                "backgroundColor": "#4a90e2",
                "color": "#ffffff",
                "fontWeight": "600",
                "borderRadius": 10,
                "cursor": "pointer"
              },
              "props": { "onClick": "onSignupSubmit" }
            },
            {
              "id": 9209,
              "type": "text",
              "parentId": 9201,
              "indexInParent": 7,
              "value": "Already have an account?",
              "style": {
                "textAlign": "center",
                "marginTop": 10
              }
            },
            {
              "id": 9210,
              "type": "button",
              "parentId": 9201,
              "indexInParent": 8,
              "value": "Login Here",
              "style": {
                "backgroundColor": "transparent",
                "color": "#4a90e2",
                "textDecoration": "underline",
                "fontWeight": "600",
                "cursor": "pointer",
                "marginLeft": "auto",
                "marginRight": "auto"
              },
              "props": { "onClick": "goToLoginPage" }
            }
          ]
        }
      ]
    }
    

  ]
},
{
  "id": 5,
  "name": "Reset Password Page",
  "width": "100%",
  "backgroundColor": "#f5f7fa",
  "parentId": None,
  "indexInParent": 4,
  "children": [
    {
      "id": 93000,
      "type": "column-container",
      "parentId": 5,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": 20,
        "flexDirection": "column"
      },
      "children": [
        {
          "id": 9301,
          "type": "column-container",
          "parentId": 93000,
          "indexInParent": 0,
          "style": {
            "width": 400,
            "backgroundColor": "#ffffff",
            "padding": 30,
            "borderRadius": 16,
            "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
            "gap": 20,
            "display": "flex",
            "flexDirection": "column",
            "alignSelf": "center"
          },
          "children": [
            {
              "id": 9302,
              "type": "text",
              "parentId": 9301,
              "indexInParent": 0,
              "value": "Reset Your Password 🔒",
              "style": {
                "fontSize": 26,
                "fontWeight": "600",
                "textAlign": "center",
                "marginBottom": 10
              }
            },
            {
              "id": 9303,
              "type": "input",
              "parentId": 9301,
              "indexInParent": 1,
              "placeholder": "Email",
              "style": {
                "width": "100%",
                "padding": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "resetEmailChange" }
            },
            {
              "id": 9304,
              "type": "input",
              "parentId": 9301,
              "indexInParent": 2,
              "placeholder": "Old Password",
              "style": {
                "width": "100%",
                "padding": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "resetOldPasswordChange" }
            },
            {
              "id": 9305,
              "type": "input",
              "parentId": 9301,
              "indexInParent": 3,
              "placeholder": "New Password",
              "style": {
                "width": "100%",
                "padding": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "resetNewPasswordChange" }
            },
            {
              "id": 9306,
              "type": "input",
              "parentId": 9301,
              "indexInParent": 4,
              "placeholder": "Confirm Password",
              "style": {
                "width": "100%",
                "padding": 14,
                "borderRadius": 10,
                "border": "1px solid #ccc"
              },
              "props": { "onChange": "resetConfirmPasswordChange" }
            },
            {
              "id": 9307,
              "type": "button",
              "parentId": 9301,
              "indexInParent": 5,
              "value": "Reset Password",
              "style": {
                "width": "100%",
                "padding": 14,
                "backgroundColor": "#4a90e2",
                "color": "#ffffff",
                "fontWeight": "600",
                "borderRadius": 10,
                "cursor": "pointer"
              },
              "props": { "onClick": "onResetSubmit" }
            }
          ]
        }
      ]
    }
  ]
},
  {
  "id": 6,
  "name": "Charts Page 1",
  "width": "1500",
  "backgroundColor": "#f9fafb",
  "parentId": None,
  "indexInParent": 5,
  "children": [
    {
      "id": 6000,
      "type": "column-container",
      "hidden": False,
      "parentId": 6,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "gap": 30,
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "stretch",
        "paddingTop": 20,
        "paddingBottom": 20,
        "paddingLeft": 20,
        "paddingRight": 20,
        "backgroundColor": "#ffffff"
      },
      "children": [
        {
          "id": 6001,
          "type": "piechart",
          "hidden": False,
          "parentId": 6000,
          "indexInParent": 0,
          "style": {"height": 300, "width": "100%"},
          "data": {
            "labels": ["Red", "Blue", "Yellow", "Green"],
            "datasets": [
              {
                "label": "Pie Dataset",
                "data": [12, 19, 7, 15],
                "backgroundColor": ["#f87171", "#34d399", "#60a5fa", "#fbbf24"],
                "borderColor": "#1f2937",
                "borderWidth": 1
              }
            ]
          }
        },
        {
          "id": 6002,
          "type": "barchart",
          "hidden": False,
          "parentId": 6000,
          "indexInParent": 1,
          "style": {"height": 300, "width": "100%"},
          "data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [
              {
                "label": "Bar Dataset",
                "data": [30, 45, 28, 60],
                "backgroundColor": ["#60a5fa","#fbbf24","#f87171","#34d399"],
                "borderColor": "#1f2937",
                "borderWidth": 1
              }
            ]
          }
        },
        {
          "id": 6003,
          "type": "linechart",
          "hidden": False,
          "parentId": 6000,
          "indexInParent": 2,
          "style": {"height": 300, "width": "100%"},
          "data": {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "datasets": [
              {
                "label": "Line Dataset",
                "data": [10, 25, 15, 40],
                "backgroundColor": "#34d399",
                "borderColor": "#34d399",
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
,
{
  "id": 7,
  "name": "Charts Page 2",
  "width": "1500",
  "backgroundColor": "#f9fafb",
  "parentId": None,
  "indexInParent": 6,
  "children": [
    {
      "id": 7000,
      "type": "column-container",
      "hidden": False,
      "parentId": 7,
      "indexInParent": 0,
      "style": {
        "width": "100%",
        "gap": 30,
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "stretch",
        "paddingTop": 20,
        "paddingBottom": 20,
        "paddingLeft": 20,
        "paddingRight": 20,
        "backgroundColor": "#ffffff"
      },
      "children": [
        {
          "id": 7002,
          "type": "radarchart",
          "hidden": False,
          "parentId": 7000,
          "indexInParent": 1,
          "style": {"height": 300, "width": "100%"},
          "data": {
            "labels": ["Strength", "Speed", "Skill", "Stamina"],
            "datasets": [
              {
                "label": "Radar Dataset",
                "data": [65, 59, 90, 81],
                "backgroundColor": "rgba(54,162,235,0.2)",
                "borderColor": "rgba(54,162,235,1)",
                "borderWidth": 1
              }
            ]
          }
        },
        {
          "id": 7003,
          "type": "areachart",
          "hidden": False,
          "parentId": 7000,
          "indexInParent": 2,
          "style": {"height": 300, "width": "100%"},
          "data": {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "datasets": [
              {
                "label": "Area Dataset",
                "data": [12, 19, 7, 15],
                "backgroundColor": "rgba(75,192,192,0.4)",
                "borderColor": "rgba(75,192,192,1)",
                "fill": True,
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

workflow = [
    {
        "id": "w1",
        "pageId": 1,
        "pageName": "Home Page",
        "elementId": 13,
        "elementType": "link",
        "trigger": {
            "type": "element",
            "scope": "element",
            "event": "clicked"
        },
        "description": "Navigates to Second Page from Home Page navbar.",
        "conditions": [
        ],
        "actions": [
            {
                "category": "navigation",
                "actionType": "navigate",
                "targetPageId": 2,
                "conditions": []
            }
        ]
    },

    {
    "id": "w2",
    "pageId": 1,
    "actions": [
      {
        "popupId": "login_popup",
        "category": "element",
        "actionType": "open_popup",
        "conditions": [],
        "targetPageId": 2
      }
    ],
    "trigger": {
      "type": "element",
      "event": "clicked",
      "scope": "element"
    },
    "pageName": "Home Page",
    "elementId": "77200",
    "conditions": [],
    "description": "Navigate to Login Page from Home Page.",
    "elementType": ""
  },
    {
        "id": "w3",
        "pageId": 2,
        "pageName": "Second Page",
        "elementId": 3003,
        "elementType": "link",
        "trigger": {
            "type": "element",
            "scope": "element",
            "event": "clicked"
        },
        "description": "Navigates to Home Page from Second Page navbar.",
        "conditions": [],
        "actions": [
            {
                "actionType": "navigate",
                "targetPageId": 1,
                "conditions": []
            }
        ]
    },
    {
        "id": "w4",
        "pageId": 1,
        "pageName": "Home Page",
        "elementId": 77200,
        "trigger": {
            "type": "element",
            "scope": "element",
            "event": "clicked"
        },
        "description": "Redirect to login if user not logged in",
        "conditions": [
        ],
        "actions": [
      {
        "email": {
          "source": "",
          "property": "",
          "operators": [],
          "returnType": "text"
        },
        "category": "account",
        "password": {
          "source": "",
          "property": "",
          "operators": [],
          "returnType": "text"
        },
        "actionType": "login",
        "conditions": [],
        "targetPageId": 2
      }
    ],
    },

    {
    "id": "w5",
    "pageId": 1,
    "actions": [
      {
        "popupId": "login_popup",
        "category": "account",
        "actionType": "logout",
        "conditions": [],
        "targetPageId": 2
      }
    ],
    "trigger": {
      "type": "element",
      "event": "clicked",
      "scope": "element"
    },
    "pageName": "Home Page",
    "elementId": "76222",
    "conditions": [],
    "description": "Opens login popup",
    "elementType": ""
  }
]







datatypes = [

    # ---------------- USERS ----------------
    {
        "name": "users",
        "fields": [
            {"name": "name", "type": "text", "cardinality": "single"},
            {"name": "email", "type": "email", "cardinality": "single"},
            {"name": "passwordHash", "type": "text", "cardinality": "single"},
            {"name": "isAdmin", "type": "boolean", "cardinality": "single"},
            {"name": "createdAt", "type": "date", "cardinality": "single"},
            {"name": "platformUserId", "type": "number", "cardinality": "single"},

            # 🔹 Virtual / reverse relations (Bubble auto-creates these)
            {
                "name": "orders",
                "type": "orders",
                "cardinality": "list",
                "relation": {"from": "users", "to": "orders"}
            },
            {
                "name": "searchHistory",
                "type": "searchHistory",
                "cardinality": "list",
                "relation": {"from": "users", "to": "searchHistory"}
            },
            {
                "name": "preferences",
                "type": "preferences",
                "cardinality": "single",
                "relation": {"from": "users", "to": "preferences"}
            }
        ]
    },

    # ---------------- SESSIONS ----------------
    {
        "name": "sessions",
        "fields": [
            {"name": "token", "type": "text", "cardinality": "single"},
            {
                "name": "user",
                "type": "users",
                "cardinality": "single",
                "relation": {"from": "sessions", "to": "users"}
            },
            {"name": "createdAt", "type": "date", "cardinality": "single"},
            {"name": "expiresAt", "type": "date", "cardinality": "single"}
        ]
    },

    # ---------------- PRODUCTS ----------------
    {
        "name": "products",
        "fields": [
            {"name": "name", "type": "text", "cardinality": "single"},
            {"name": "description", "type": "text", "cardinality": "single"},
            {"name": "price", "type": "number", "cardinality": "single"},
            {"name": "stockQuantity", "type": "number", "cardinality": "single"},
            {"name": "src", "type": "image", "cardinality": "single"},
            {"name": "createdAt", "type": "date", "cardinality": "single"},

            {
                "name": "category",
                "type": "categories",
                "cardinality": "single",
                "relation": {"from": "products", "to": "categories"}
            },

            {
                "name": "orders",
                "type": "orders",
                "cardinality": "list",
                "relation": {"from": "products", "to": "orders"}
            },
            {
            "name": "creatorId",
            "type": "users",
            "cardinality": "single",
            "relation": {"from": "products", "to": "users"}
            }
        ]
    },
    

    # ---------------- CATEGORIES ----------------
    {
        "name": "categories",
        "fields": [
            {"name": "name", "type": "text", "cardinality": "single"},

            {
                "name": "products",
                "type": "products",
                "cardinality": "list",
                "relation": {"from": "categories", "to": "products"}
            }
        ]
    },

    # ---------------- SEARCH HISTORY ----------------
    {
        "name": "searchHistory",
        "fields": [
            {"name": "query", "type": "text", "cardinality": "single"},
            {"name": "createdAt", "type": "date", "cardinality": "single"},
            {
                "name": "user",
                "type": "users",
                "cardinality": "single",
                "relation": {"from": "searchHistory", "to": "users"}
            }
        ]
    },

    # ---------------- USER PREFERENCES ----------------
    {
        "name": "preferences",
        "fields": [
            {"name": "onSaleOnly", "type": "boolean", "cardinality": "single"},
            {"name": "selectedOption", "type": "text", "cardinality": "single"},
            {"name": "selectedDropdown", "type": "text", "cardinality": "single"},
            {"name": "newsletterSubscribed", "type": "boolean", "cardinality": "single"},
            {"name": "gender", "type": "text", "cardinality": "single"},
            {"name": "updatedAt", "type": "date", "cardinality": "single"},

            {
                "name": "user",
                "type": "users",
                "cardinality": "single",
                "relation": {"from": "preferences", "to": "users"}
            }
        ]
    },

    # ---------------- ORDERS ----------------
    {
        "name": "orders",
        "fields": [
            {"name": "quantity", "type": "number", "cardinality": "single"},
            {"name": "totalPrice", "type": "number", "cardinality": "single"},
            {"name": "status", "type": "text", "cardinality": "single"},
            {"name": "createdAt", "type": "date", "cardinality": "single"},

            {
                "name": "user",
                "type": "users",
                "cardinality": "single",
                "relation": {"from": "orders", "to": "users"}
            },
            {
                "name": "product",
                "type": "products",
                "cardinality": "single",
                "relation": {"from": "orders", "to": "products"}
            }
        ]
    }
]


app_datas = {
    "users": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "passwordHash": "hash_12345",
            "isAdmin": False,
            "createdAt": "2024-01-10",
            "platformUserId": 101
        },
        {
            "id": 2,
            "name": "Sarah Smith",
            "email": "sarah@example.com",
            "passwordHash": "hash_67890",
            "isAdmin": False,
            "createdAt": "2024-02-14",
            "platformUserId": 102
        },
        {
            "id": 3,
            "name": "Ajith",
            "email": "ajithravichandran@gmail.com",
            "passwordHash": "Ajith",
            "isAdmin": True,
            "createdAt": "2025-11-12",
            "platformUserId": 103
        },

    ],

    "categories": [
        {"id": 1, "name": "Electronics"},
        {"id": 2, "name": "Pets"},
        {"id": 3, "name": "Furniture"},
        {"id": 4, "name": "Sale"}
    ],

    "products": [
        {
            "id": 100,
            "name": "Cat Food Premium",
            "description": "High quality dry food for adult cats.",
            "price": 19.99,
            "stockQuantity": 45,
            "src": "live/image1.jpg",
            "categoryId": 2,
             "creatorId": 1,
            "createdAt": "2024-03-01"
        },
        {
            "id": 101,
            "name": "Bluetooth Speaker",
            "description": "Portable wireless speaker with high bass.",
                       "price": 49.99,
            "stockQuantity": 120,
            "src": "live/image8.jpg",
            "categoryId": 1,
             "creatorId": 1,
            "createdAt": "2024-03-05"
        },
        {
            "id": 102,
            "name": "Modern Office Chair",
            "description": "Ergonomic chair with cushion support.",
            "price": 129.99,
            "stockQuantity": 30,
            "src": "live/image1.jpg",
            "categoryId": 3,
             "creatorId": 1,
            "createdAt": "2024-02-20"
        },
        {
            "id": 103,
            "name": "Sale Headphones",
            "description": "Noise-cancelling headphones on sale.",
            "price": 59.99,
            "stockQuantity": 15,
            "src": "live/image8.jpg",
            "categoryId": 4,
             "creatorId": 1,
            "createdAt": "2024-01-25"
        },
        {
            "id": 104,
            "name": "Phoes",
            "description": "Noise-cancelling headphones on sale.",
            "price": 59.99,
            "stockQuantity": 15,
            "src": "live/image3.jpg",
            "categoryId": 4,
             "creatorId": 2,
            "createdAt": "2024-01-25"
        },
        {
            "id": 105,
            "name": "Cricket Bat",
            "description": "Noise-cancelling headphones on sale.",
            "price": 59.99,
            "stockQuantity": 15,
            "src": "hp_sale.jpg",
            "categoryId": 4,
             "creatorId": 2,
            "createdAt": "2024-01-25"
        },
        {
            "id": 106,
            "name": "Sun Glasses",
            "description": "Noise-cancelling headphones on sale.",
            "price": 59.99,
            "stockQuantity": 15,
            "src": "hp_sale.jpg",
            "categoryId": 4,
             "creatorId": 2,
            "createdAt": "2024-01-25"
        },
        {
            "id": 107,
            "name": "Monitor",
            "description": "Noise-cancelling headphones on sale.",
            "price": 59.99,
            "stockQuantity": 15,
            "src": "hp_sale.jpg",
            "categoryId": 4,
             "creatorId": 2,
            "createdAt": "2024-01-25"
        },
    ],

    "searchHistory": [
        {
            "id": 1,
            "userId": 1,
            "query": "cat food",
            "createdAt": "2024-03-10"
        },
        {
            "id": 2,
            "userId": 2,
            "query": "chair",
            "createdAt": "2024-03-11"
        }
    ],

    "preferences": [
        {
            "id": 1,
            "userId": 1,
            "onSaleOnly": False,
            "selectedOption": "option2",
            "selectedDropdown": "d1",
            "newsletterSubscribed": True,
            "gender": "male",
            "updatedAt": "2024-03-10"
        },
        {
            "id": 2,
            "userId": 2,
            "onSaleOnly": True,
            "selectedOption": "option1",
            "selectedDropdown": "d3",
            "newsletterSubscribed": False,
            "gender": "female",
            "updatedAt": "2024-03-11"
        }
    ],

    "orders": [
        {
            "id": 1,
            "userId": 1,
            "productId": 100,
            "quantity": 2,
            "totalPrice": 39.98,
            "status": "paid",
            "createdAt": "2024-03-12"
        },
        {
            "id": 2,
            "userId": 2,
            "productId": 103,
            "quantity": 1,
            "totalPrice": 59.99,
            "status": "pending",
            "createdAt": "2024-03-13"
        }
    ]
}

# def to_schema(data):
#     """
#     Converts data into a schema template.
#     Keeps structure but removes real values.
#     """
#     if isinstance(data, dict):
#         schema = {}
#         for k, v in data.items():
#             if isinstance(v, (dict, list)):
#                 schema[k] = to_schema(v)
#             else:
#                 if isinstance(v, str):
#                     schema[k] = ""
#                 elif isinstance(v, bool):
#                     schema[k] = False
#                 elif isinstance(v, int):
#                     schema[k] = 0      # 👈 FIX: never None
#                 elif isinstance(v, float):
#                     schema[k] = 0.0
#                 else:
#                     schema[k] = None
#         return schema

#     elif isinstance(data, list):
#         return [to_schema(data[0])] if data else []

#     return None


# # Usage
# app_datas= to_schema(app_datass)

# # Print result
# import pprint
# pprint.pprint(app_datas)
