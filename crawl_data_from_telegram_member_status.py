# pip install python-telegram-bot --upgrade
# pip install pyTelegramBotAPI
import telebot
import csv
import datetime

bot_token = '5678044774:AAHsLT1r-xv-tnxoX2jmMgcQz5gb1qFcpKQ'

bot = telebot.TeleBot(token=bot_token) 

@bot.message_handler(content_types=['new_chat_members','left_chat_member'])
def on_member(message):
    csv_rows = []
    with open('telegram_member_status.csv', mode='a', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        csv_rows.append(datetime.datetime.now())
        csv_rows.append(message.chat.id)
        csv_rows.append(message.chat.title)
        csv_rows.append(message.from_user.id)
        csv_rows.append(message.from_user.is_bot)
        csv_rows.append(message.from_user.first_name)
        csv_rows.append(message.from_user.last_name)
        csv_rows.append(message.from_user.username)
        csv_rows.append(message.content_type)
        print(csv_rows)
        writer.writerow(csv_rows)
        csv_rows.clear()
    #print(message)

bot.polling()
