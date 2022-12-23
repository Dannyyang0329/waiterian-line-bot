from transitions.extensions import GraphMachine

from utils import *

class Waiterian_Machine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)


    def is_going_to_idle(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'idle':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'WAITERIAN':
                show_mainmenu(event)
                return True
        elif self.state == 'search_restaurant':
            if msg == 'QUIT':
                print_quit_msg(event, 'search_restaurant')
                return True
        elif self.state == 'search_recipe':
            if msg == 'QUIT':
                print_quit_msg(event, 'search_recipe')
                return True
        elif self.state == 'help':
            if msg == 'QUIT':
                print_quit_msg(event, 'help')
                return True
        return False


    def is_going_to_search_restaurant(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'search_restaurant':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'SHOW ALL SETTINGS':
                show_all_setting(event)
                return True
            elif msg == 'START':
                show_all_restaurant(event)
                return True
        elif self.state == 'idle':
            if msg == 'SEARCH RESTAURANT':
                show_search_filter(event)
                return True;
        elif self.state == 'get_location':
            return get_the_location(event)
        elif self.state == 'get_radius':
            return get_the_radius(event)
        elif self.state == 'get_price_level':
            return get_the_price_level(event)
        elif self.state == 'get_keyword':
            return get_the_keyword(event)

        return False;


    def is_going_to_get_location(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'get_location':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'search_restaurant':
            if msg == 'SET LOCATION':
                show_location_message(event)
                return True
        return False


    def is_going_to_get_radius(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'get_radius':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'search_restaurant':
            if msg == 'SET RADIUS':
                show_radius_message(event)
                return True
        return False


    def is_going_to_get_price_level(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'get_price_level':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'search_restaurant':
            if msg == 'SET PRICE LEVEL':
                show_price_level_message(event)
                return True
        return False


    def is_going_to_get_keyword(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'get_keyword':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'search_restaurant':
            if msg == 'SET KEYWORD':
                show_keyword_message(event)
                return True
        return False


    def is_going_to_search_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'search_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'idle':
            if msg == 'SEARCH RECIPE':
                show_search_recipe(event)
                return True
        elif self.state == 'dessert_recipe':
            if msg == 'QUIT':
                show_search_recipe(event)
                return True
        elif self.state == 'dish_recipe':
            if msg == 'QUIT':
                show_search_recipe(event)
                return True
        elif self.state == 'exotic_recipe':
            if msg == 'QUIT':
                show_search_recipe(event)
                return True
        elif self.state == 'drink_recipe':
            if msg == 'QUIT':
                show_search_recipe(event)
                return True
        elif self.state == 'wait_target_recipe':
            return get_the_target_recipe(event)

        return False

    def is_going_to_dessert_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'dessert_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'RANDOM':
                show_all_recipe(event, 'dessert', 'random')
                return True
            elif msg == 'PUDDING':
                show_all_recipe(event, 'dessert', 'pudding')
                return True
            elif msg == 'CHOCOLATE':
                show_all_recipe(event, 'dessert', 'chocolate')
                return True
            elif msg == 'COOKIE':
                show_all_recipe(event, 'dessert', 'cookie')
                return True
            elif msg == 'BREAD':
                show_all_recipe(event, 'dessert', 'bread')
                return True
        elif self.state == 'search_recipe':
            if msg == 'GET DESSERT RECIPE':
                show_dessert_recipe_category(event)
                return True
        return False


    def is_going_to_dish_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'dish_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'RANDOM':
                show_all_recipe(event, 'dish', 'random')
                return True
            elif msg == 'BEEF':
                show_all_recipe(event, 'dish', 'beef')
                return True
            elif msg == 'PORK':
                show_all_recipe(event, 'dish', 'pork')
                return True
            elif msg == 'CHICKEN':
                show_all_recipe(event, 'dish', 'chicken')
                return True
            elif msg == 'SEAFOOD':
                show_all_recipe(event, 'dish', 'seafood')
                return True
            elif msg == 'EGG':
                show_all_recipe(event, 'dish', 'egg')
                return True
            elif msg == 'VEGETABLE':
                show_all_recipe(event, 'dish', 'vegetable')
                return True
        elif self.state == 'search_recipe':
            if msg == 'GET CUISINE RECIPE':
                show_dish_recipe_category(event)
                return True
        return False


    def is_going_to_exotic_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'exotic_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'JAPANESE':
                show_all_recipe(event, 'exotic', 'japanese')
                return True
            elif msg == 'AMERICAN':
                show_all_recipe(event, 'exotic', 'american')
                return True
            elif msg == 'KOREAN':
                show_all_recipe(event, 'exotic', 'korean')
                return True
            elif msg == 'ITALIAN':
                show_all_recipe(event, 'exotic', 'italian')
                return True
            elif msg == 'THAI':
                show_all_recipe(event, 'exotic', 'thai')
                return True
        elif self.state == 'search_recipe':
            if msg == 'GET EXOTIC RECIPE':
                show_exotic_recipe_category(event)
                return True
        return False


    def is_going_to_drink_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'drink_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'TOPPINGS':
                show_all_recipe(event, 'drink', 'toppings')
                return True
            elif msg == 'DRINK':
                show_all_recipe(event, 'drink', 'drink')
                return True
            elif msg == 'ICE':
                show_all_recipe(event, 'drink', 'ice')
                return True
        elif self.state == 'search_recipe':
            if msg == 'GET DRINK RECIPE':
                show_drink_recipe_category(event)
                return True
        return False


    def is_going_to_wait_target_recipe(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'wait_target_recipe':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
        elif self.state == 'search_recipe':
            if msg == 'GET SPECIFIC RECIPE':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="可以輸入要搜尋的食譜了!")
                )
                return True
        return False


    def is_going_to_help(self, event):
        msg = event.message.text.upper() if event.message.type == 'text' else ''
        if self.state == 'help':
            if msg == 'INFORMATION':
                show_information(event, self.state)
                return True
            elif msg == 'HELP SEARCH RESTAURANT':
                show_help_manual(event, 'search_restaurant')
                return True
            elif msg == 'HELP SEARCH RECIPE':
                show_help_manual(event, 'search_recipe')
                return True

        elif self.state == 'idle':
            if msg == "HELP":
                show_help_manual_category(event)
                return True;
        return False


def get_fsm(init_state):
    states = [
        "idle", 
        "search_restaurant",
        "get_location", 
        "get_radius", 
        "get_price_level",
        "get_keyword",
        "search_recipe",
        "dessert_recipe",
        "dish_recipe",
        "exotic_recipe",
        "drink_recipe",
        "wait_target_recipe",
        "help",
    ]
    transitions = [
        # source is 'idle'
        {
            "trigger": "advance",
            "source": "idle",
            "dest": "idle",
            "conditions": "is_going_to_idle",
        },
        {
            "trigger": "advance",
            "source": "idle",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        {
            "trigger": "advance",
            "source": "idle",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        {
            "trigger": "advance",
            "source": "idle",
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        # source is 'search_restaurant'
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "idle",
            "conditions": "is_going_to_idle",
        },
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "get_location",
            "conditions": "is_going_to_get_location",
        },
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "get_radius",
            "conditions": "is_going_to_get_radius",
        },
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "get_price_level",
            "conditions": "is_going_to_get_price_level",
        },
        {
            "trigger": "advance",
            "source": "search_restaurant",
            "dest": "get_keyword",
            "conditions": "is_going_to_get_keyword",
        },
        # source is 'get_location'
        {
            "trigger": "advance",
            "source": "get_location",
            "dest": "get_location",
            "conditions": "is_going_to_get_location",
        },
        {
            "trigger": "advance",
            "source": "get_location",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        # source is 'get_radius'
        {
            "trigger": "advance",
            "source": "get_radius",
            "dest": "get_radius",
            "conditions": "is_going_to_get_radius",
        },
        {
            "trigger": "advance",
            "source": "get_radius",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        # source is 'get_price_level'
        {
            "trigger": "advance",
            "source": "get_price_level",
            "dest": "get_price_level",
            "conditions": "is_going_to_get_price_level",
        },
        {
            "trigger": "advance",
            "source": "get_price_level",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        # source is 'get_keyword'
        {
            "trigger": "advance",
            "source": "get_keyword",
            "dest": "get_keyword",
            "conditions": "is_going_to_get_keyword",
        },
        {
            "trigger": "advance",
            "source": "get_keyword",
            "dest": "search_restaurant",
            "conditions": "is_going_to_search_restaurant",
        },
        # source is 'search_recipe'
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "idle",
            "conditions": "is_going_to_idle",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "dessert_recipe",
            "conditions": "is_going_to_dessert_recipe",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "dish_recipe",
            "conditions": "is_going_to_dish_recipe",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "exotic_recipe",
            "conditions": "is_going_to_exotic_recipe",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "drink_recipe",
            "conditions": "is_going_to_drink_recipe",
        },
        {
            "trigger": "advance",
            "source": "search_recipe",
            "dest": "wait_target_recipe",
            "conditions": "is_going_to_wait_target_recipe",
        },
        # source is 'dessert_recipe'
        {
            "trigger": "advance",
            "source": "dessert_recipe",
            "dest": "dessert_recipe",
            "conditions": "is_going_to_dessert_recipe",
        },
        {
            "trigger": "advance",
            "source": "dessert_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        # source is 'dish_recipe'
        {
            "trigger": "advance",
            "source": "dish_recipe",
            "dest": "dish_recipe",
            "conditions": "is_going_to_dish_recipe",
        },
        {
            "trigger": "advance",
            "source": "dish_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        # source is 'exotic_recipe'
        {
            "trigger": "advance",
            "source": "exotic_recipe",
            "dest": "exotic_recipe",
            "conditions": "is_going_to_exotic_recipe",
        },
        {
            "trigger": "advance",
            "source": "exotic_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        # source is 'drink_recipe'
        {
            "trigger": "advance",
            "source": "drink_recipe",
            "dest": "drink_recipe",
            "conditions": "is_going_to_drink_recipe",
        },
        {
            "trigger": "advance",
            "source": "drink_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        # source is 'drink_recipe'
        {
            "trigger": "advance",
            "source": "wait_target_recipe",
            "dest": "wait_target_recipe",
            "conditions": "is_going_to_wait_target_recipe",
        },
        {
            "trigger": "advance",
            "source": "wait_target_recipe",
            "dest": "search_recipe",
            "conditions": "is_going_to_search_recipe",
        },
        # source is 'help'
        {
            "trigger": "advance",
            "source": "help",
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        {
            "trigger": "advance",
            "source": "help",
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
