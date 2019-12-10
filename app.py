import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

load_dotenv()


machine = TocMachine(
    states=["user", "m_or_o", "menu","order","howmany","conti","o_or_s","show"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "m_or_o",
            "conditions": "is_going_to_m_or_o",
        },
        {
            "trigger": "go_menu",
            "source": "m_or_o",
            "dest": "menu",
        },
        {
            "trigger": "go_order",
            "source": "m_or_o",
            "dest": "order",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "order",
            "conditions": "is_going_to_order",
        },
        {
            "trigger": "advance",
            "source": "order",
            "dest": "howmany",
            #"conditions": "is_going_to_howmany",
        },
        {
            "trigger": "advance",
            "source": "howmany",
            "dest": "conti",
            #"conditions": "is_going_to_conti",
        },
        {
            "trigger": "advance",
            "source": "conti",
            "dest": "o_or_s",
            "conditions": "is_going_to_o_or_s",
        },
        {
            "trigger": "go_order",
            "source": "o_or_s",
            "dest": "order",
        },
        {
            "trigger": "go_show",
            "source": "o_or_s",
            "dest": "show",
        },
        {
            "trigger": "go_back", 
            "source": "show",
            #"source": ["menu","order","howmany","conti","show"], 
            "dest": "user",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET","f943675a8f098a73f67e1d092a16ebe3" )
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN","s3ntie+rmQFtWDKR3hNPHD6MSN//zVZqPoBYI4qakRU38Bdg9age/Uh7TaO7KAOwAUNSj0PzMW/0ov/n3P1lIi2GUs5+mncP9zUAQmKke2q6tLe9xvgzo/7muWkg2kTy/nySqH8TYVLNyIS7dGXbewdB04t89/1O/w1cDnyilFU=")
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

        pass
        #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'linebot-0561acbdf0d0.json'
        GSpreadSheet = 'pythonlinebot'
        while True:
            try:
                scope = ['https://spreadsheets.google.com/feeds']
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                worksheet = gc.open(GSpreadSheet).sheet1
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt=""
            textt+=event.message.text
            if textt!="":
                worksheet.append_row((datetime.datetime.now(), textt))
                print('新增一列資料到試算表' ,GSpreadSheet)
                return textt    


    return "OK"



@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
