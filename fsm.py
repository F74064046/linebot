from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return text.lower() == "start"

    def is_going_to_guess(self, event):
        text = event.message.text
        return text.lower() == "ok"

    def is_going_to_check(self, event):
        text = event.message.text
        if text.isdigit():
            return True
        else:
            return False

    

    def on_enter_start(self, event):
        print("I'm entering start")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入 ok 開始玩遊戲!\n\n規則:\n謎底為一個四位數號碼(數字不重複)\n機器人會回復線索,以?A?B形式呈現，直到答對(4A0B)為止。\n(例如:當謎底為8123，而猜謎者猜1052時，出題者必須提示0A2B)")


    def on_enter_guess(self, event):
        print("I'm entering guess")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入一個四位數號碼,數字不得重複")

    
    def on_enter_check(self, event):
        print("I'm entering check")

        reply_token = event.reply_token
        send_text_message(reply_token, "right")
        self.goto_user(event)