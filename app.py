from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, AudioSendMessage
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    if user_msg == "早安":
        audio_url = f"{request.url_root}static/ohayo.mp3"
        line_bot_api.reply_message(
            event.reply_token,
            AudioSendMessage(
                original_content_url=audio_url,
                duration=3000
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請說 '早安' 來聽聽小松鼠的聲音唷！")
        )

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
