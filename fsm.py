from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_m_or_o(self, event):
        text = event.message.text
        if text.lower() == "menu":
            return True
        elif text.lower() == "order":
            return True
        else:
            return False

    def is_going_to_o_or_s(self, event):
        text = event.message.text
        if text.lower() == "order":
            return True
        elif text.lower() == "ok":
            return True
        else:
            return False
    def is_go_back(self, event):
        text = event.message.text
        return text.lower() == "bye"

    def is_going_to_order(self, event):
        text = event.message.text
        return text.lower() == "order"

    def on_enter_m_or_o(self, event):
        print("I'm entering m_or_o")

        text = event.message.text
        if text.lower() == "menu":
            self.go_menu(event)
        elif text.lower() == "order":
            self.go_order(event)

    def on_enter_o_or_s(self, event):
        print("I'm entering o_or_s")

        text = event.message.text
        if text.lower() == "show":
            self.go_show(event)
        elif text.lower() == "order":
            self.go_order(event)




    def on_enter_user(self, event):
        print("I'm entering user")

        reply_token = event.reply_token
        send_text_message(reply_token, "hi~\nreply menu if you want to watch the menu\nreply order if you want to order something")

    def on_enter_menu(self, event):
        print("I'm entering menu")

        reply_token = event.reply_token
        send_text_message(reply_token, "A,B,C\nreply order if you want to order something\nreply cancel if you want to go back")
    
    def on_enter_order(self, event):
        print("I'm entering order")

        reply_token = event.reply_token
        send_text_message(reply_token, "you can enter what you want to eat.")
    
    def on_enter_howmany(self, event):
        print("I'm entering howmany")

        reply_token = event.reply_token
        send_text_message(reply_token, "how many?")

    def on_enter_conti(self, event):
        print("I'm entering conti")

        reply_token = event.reply_token
        send_text_message(reply_token, "reply order if you want to continue to order something\nreply ok if you have finished your order")

    def on_enter_show(self, event):
        print("I'm entering conti")

        reply_token = event.reply_token
        send_text_message(reply_token, "show")

        self.go_back(event)

