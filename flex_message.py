def get_mainmenu_json():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/V6gyhBr.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "SEARCH RESTAURANT"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/wCBqkDm.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "SEARCH RECIPE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/Bq65EiI.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "INFORMATION"
                    }
                }
            }
        ]
    }
    return carousel_images

# ============================================================================

def get_search_restaurant_json():
    filter = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            },
            "url": 'https://i.imgur.com/V6gyhBr.png'
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "?????????????????????",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "?????????",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "???????????????????????????!!!",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#F5F5DC"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "SET LOCATION"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "SET RADIUS"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "SET PRICE LEVEL"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "???????????????",
                        "text": "SET KEYWORD"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "??????????????????",
                        "text": "SHOW ALL SETTINGS"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "START"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "??????",
                        "text": "QUIT"
                    }
                }
            ],
            "flex": 0,
            "backgroundColor": "#F5F5DC"
        }
    }
    return filter

# ============================================================================

def get_single_restaurant_json(image_url, name, grade, price_level, address, web_url):
    whole_star_url = 'https://i.imgur.com/XOV82JN.png'
    empty_star_url = 'https://i.imgur.com/1HeQOqo.png'
    dollar_url = 'https://i.imgur.com/5UfyD1N.png'
    background_url = 'https://i.imgur.com/TL7E1pM.png'

    restaurant = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": whole_star_url if (grade >= 1) else empty_star_url
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": whole_star_url if (grade >= 2) else empty_star_url
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": whole_star_url if (grade >= 3) else empty_star_url
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": whole_star_url if (grade >= 4) else empty_star_url
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": whole_star_url if (grade >= 5) else empty_star_url
                        },
                        {
                            "type": "text",
                            "text": str(grade),
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "offsetStart": "xxl",
                            "url": dollar_url if (price_level >= 1) else background_url
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "offsetStart": "xxl",
                            "url": dollar_url if (price_level >= 2) else background_url
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "offsetStart": "xxl",
                            "url": dollar_url if (price_level >= 3) else background_url
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "offsetStart": "xxl",
                            "url": dollar_url if (price_level >= 4) else background_url
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "??????",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": address,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#F5F5DC"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                    "type": "uri",
                    "label": "????????????",
                    "uri": web_url
                },
                "height": "sm",
                "margin": "none",
                "offsetTop": "sm"
                }
            ],
            "flex": 0,
            "backgroundColor": "#F5F5DC"
        }
    }
    return restaurant

# ============================================================================

def get_search_recipe_json():
    filter = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            },
            "url": 'https://i.imgur.com/wCBqkDm.png'
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "????????????????????????",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "?????????",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": '????????????"??????????????????"????????????????????????!!!',
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#F5F5DC"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "???????????????",
                        "text": "GET DESSERT RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "GET CUISINE RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "GET EXOTIC RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "???????????????",
                        "text": "GET DRINK RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "??????????????????",
                        "text": "GET SPECIFIC RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "??????",
                        "text": "QUIT"
                    }
                }
            ],
            "flex": 0,
            "backgroundColor": "#F5F5DC"
        }
    }
    return filter

# ============================================================================

def get_single_recipe_json(image_url, name, ingredient, web_url):
    recipe = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "??????",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": ingredient,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#F5F5DC"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                    "type": "uri",
                    "label": "????????????",
                    "uri": web_url
                },
                "height": "sm",
                "margin": "none",
                "offsetTop": "sm"
                }
            ],
            "flex": 0,
            "backgroundColor": "#F5F5DC"
        }
    }
    return recipe

# ============================================================================

def get_dessert_recipe_json():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/5X5L31I.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "RANDOM"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/uD7sauw.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "PUDDING"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/0tdUAoZ.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "CHOCOLATE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/O6GyVqt.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "COOKIE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/aMovNEI.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "BREAD"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/l1TQyNh.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "QUIT"
                    }
                }
            }
        ]
    }
    return carousel_images

# ============================================================================

def get_dish_recipe_json():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/5X5L31I.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "RANDOM"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/NbtLncN.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "BEEF"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/DgeGMHT.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "PORK"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/PtbGAQ7.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "CHICKEN"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/UuaR9Un.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "SEAFOOD"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/cqAfjHc.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "EGG"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/Ws8sAHK.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "VEGETABLE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/l1TQyNh.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "QUIT"
                    }
                }
            }
        ]
    }
    return carousel_images

# ============================================================================

def get_exotic_recipe_json():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/cfGygWY.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "JAPANESE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rYGv1NM.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "AMERICAN"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/hyCqoCr.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "KOREAN"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/cB64sj9.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "ITALIAN"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/L9uS9c8.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "THAI"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/l1TQyNh.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "QUIT"
                    }
                }
            }
        ]
    }
    return carousel_images

# ============================================================================

def get_drink_recipe_json():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/JgOtibn.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "TOPPINGS"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/oCiA4Mv.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "DRINK"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/eZSAvrV.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "ICE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/l1TQyNh.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "QUIT"
                    }
                }
            }
        ]
    }
    return carousel_images


# ============================================================================

def get_help_manual_category_json():
    filter = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            },
            "url": 'https://i.imgur.com/Cgz26a1.png'
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "?????????????????????",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "?????????",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": '?????????"INFORMATION"????????????????????????!',
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#F5F5DC"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "HELP SEARCH RESTAURANT"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "????????????",
                        "text": "HELP SEARCH RECIPE"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "??????",
                        "text": "QUIT"
                    }
                }
            ],
            "flex": 0,
            "backgroundColor": "#F5F5DC"
        }
    }
    return filter
