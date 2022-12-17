from transitions.extensions import GraphMachine

from utils import *

type_dict = {}

class Waiterian_Machine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_information(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == 'INFORMATION':
            info = f"""
            Type    : {event.source.type}
            State   : {self.state}
            """
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))
        return False

    def is_going_to_search_filter(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'idle':
            if msg == 'WAITERIAN':
                show_carousel_images(event)     # idle -> idle
                return False
            elif msg == 'RESTAURANT':
                show_search_filter(event, 'RESTAURANT')
            elif msg == 'DESSERT':
                show_search_filter(event, 'DESSERT')
            elif msg == 'CAFE':
                show_search_filter(event, 'CAFE')
            else:
                return False
            return True
        if self.state == 'search_filter':
            if msg == '顯示所有設定':
                show_all_setting(event)         # search_filter -> search_filter
                return True
        if self.state == 'get_location':
            return get_the_location(event)      # get_location -> search_filter
        if self.state == 'get_radius':
            return get_the_radius(event)        # get_location -> search_filter
        if self.state == 'get_price':
            return get_the_price(event)         # get_location -> search_filter
        if self.state == 'get_keyword':
            return get_the_keyword(event)       # get_location -> search_filter

        return False


    def is_going_to_get_location(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == '設定位置訊息':
            show_location_message(event)        # search_filter -> get_location
            return True
        return False


    def is_going_to_get_radius(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == '設定搜索半徑':
            show_radius_message(event)          # search_filter -> get_radius
            return True
        return False


    def is_going_to_get_price(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == '設定價錢標準':
            show_price_message(event)           # search_filter -> get_price
            return True
        return False


    def is_going_to_get_keyword(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == '使用關鍵字搜尋':
            show_keyword_message(event)
            return True
        return False


    def is_going_to_idle(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if msg == '開始搜尋':
            show_all_restaurant(event, type_dict[get_id(event)])          # search_filter -> idle
            return True
        return False


def get_fsm(init_state):
    states = [
        "idle", 
        "select_type",
        "search_filter", 
        "get_location", 
        "get_radius", 
        "get_price",
        "get_keyword",
        "information",
    ]
    transitions = [
        {
            "trigger": "advance",
            "source": [
                "idle", 
                "search_filter", 
                "get_location", 
                "get_radius", 
                "get_price",
                "get_keyword",
            ],
            "dest": "information",
            "conditions": "is_going_to_information",
        },
        { "trigger": "go_back", "source": "information", "dest": "idle" },
        { "trigger": "go_back", "source": "information", "dest": "select_type" },
        { "trigger": "go_back", "source": "information", "dest": "search_filter" },
        { "trigger": "go_back", "source": "information", "dest": "get_location" },
        { "trigger": "go_back", "source": "information", "dest": "get_radius" },
        { "trigger": "go_back", "source": "information", "dest": "get_price" },
        { "trigger": "go_back", "source": "information", "dest": "get_keyword" },
        {
            "trigger": "advance",
            "source": "idle",
            "dest": "select_filter",
            "conditions": "is_going_to_search_filter",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "get_location",
            "conditions": "is_going_to_get_location",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "get_radius",
            "conditions": "is_going_to_get_radius",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "get_price",
            "conditions": "is_going_to_get_price",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "get_keyword",
            "conditions": "is_going_to_get_keyword",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "search_filter",
            "conditions": "is_going_to_search_filter",
        },
        {
            "trigger": "advance",
            "source": [
                "get_location",
                "get_radius",
                "get_price",
                "get_keyword",
            ],
            "dest": "search_filter",
            "conditions": "is_going_to_search_filter",
        },
        {
            "trigger": "advance",
            "source": "search_filter",
            "dest": "idle",
            "conditions": "is_going_to_idle",
        },
    ]

    machine = Waiterian_Machine(
        states=states,
        transitions=transitions,
        initial=init_state,
        auto_transitions=False,
        show_conditions=True,
    )
    return machine


# machine = get_fsm('idle')
# print(machine.state)
# print(machine.advance('FOOD'))
# print(machine.state)
# get_fsm("idle").get_graph().draw("fsm.png", prog="dot", format="png")
