def get_carousel_images():
    carousel_images = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/37rIrGT.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "FOOD"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/6q22Ncz.png",
                    "aspectMode": "cover",
                    "size": "full",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "ROULETTE"
                    }
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/fydfmTU.png",
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

def get_single_restaurant(image_url, name, grade, price_level, address, web_url):
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
                            "text": grade,
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "url": dollar_url if (price_level >= 1) else background_url,
                            "offsetStart": "xxl"
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "url": dollar_url if (price_level >= 2) else background_url,
                            "offsetStart": "xxl"
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "url": dollar_url if (price_level >= 3) else background_url,
                            "offsetStart": "xxl"
                        },
                        {
                            "type": "icon",
                            "size": "xs",
                            "url": dollar_url if (price_level >= 4) else background_url,
                            "offsetStart": "xxl"
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
                                    "text": "地址",
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
                    "label": "查看地圖",
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


