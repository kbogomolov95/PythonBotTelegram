import telegram.ext
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, User
import sqlite3
import db
import admins
from threading import Thread
from requests import get
from time import sleep

reply_keyboard = [['Получить чек-лист']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)



def start(bot, update):
    # print(update)
    # print(update.message.chat.id)

    user_id = update.message.chat.id
    username = update.message.chat.username

    update.message.reply_text(
        "Держи свой чек-лист:\ndrive.google.com/fsjsdfjsjfkjs\n\n"
        + "Телеграм-канал, где Инна делится инсайтами по финансовой грамотности:\n\n"
        + "t.me/test_channel12312")

    flag = False
    for row in db.get_info():
        if row[0] == user_id:
            flag = True

    if not flag:
        db.add_message(int(user_id), username)


def users_list(bot, update):
    if check_for_admin(bot, update):
        for row in db.get_info():
            update.message.reply_text(row)


def check_for_admin(bot, update):
    user_id = update.message.chat.id
    for row in admins.get_info():
        if user_id == row[0]:
            return True
        else:
            update.message.reply_text('Нет доступа')


broad = False


def broadcast(bot, update):
    if check_for_admin(bot, update):
        update.message.reply_text('Введите сообщение для транслирования:\n\nВ противном случае введите: /cancel')
        global broad
        broad = True


add_adm = False


def want_admin(bot, update):
    if check_for_admin(bot, update):
        update.message.reply_text('Добавить администратора: введите username БЕЗ @\n\nНазад: /cancel')
        global add_adm
        add_adm = True


del_adm = False


def del_admin(bot, update):
    if check_for_admin(bot, update):
        update.message.reply_text('Удалить администратора: введите username БЕЗ @\n\nНазад: /cancel')
        global del_adm
        del_adm = True


def list_admins(bot, update):
    if check_for_admin(bot, update):
        for row in admins.get_info():
            update.message.reply_text(row)


def users_file(bot, update):
    bot.sendDocument(update.message.chat.id, document=open('users.db', 'rb'))


def actions(bot, update):
    global add_adm
    # print(add_adm)
    if add_adm:
        if update.message.text == '/cancel':
            add_adm = False
        else:
            for row in db.get_info():
                if row[1] == update.message.text:
                    admins.add_message(row[0], row[1])
                    update.message.reply_text(str(update.message.text) + ' теперь админ.')
                    add_adm = False
                    return
            update.message.reply_text('Неправильный username.')

    global del_adm

    if del_adm:
        if update.message.text == '/cancel':
            del_adm = False
        else:
            for row in db.get_info():
                if row[1] == update.message.text:
                    if update.message.text != 'kirr_ya':
                        admins.del_message(row[0], row[1])
                        del_adm = False
                        update.message.reply_text(str(update.message.text) + ' теперь НЕ админ.')
                        return
            update.message.reply_text('Неправильный username.')

    global broad
    if broad:
        if update.message.text == '/cancel':
            broad = False
        else:
            for row in db.get_info():
                try:
                    bot.send_message(row[0], update.message.text)
                except:
                    pass
            broad = False


def heroku_life():
    while True:
        a = get('https://testfin1.herokuapp.com/')
        sleep(20 * 60)


def main():
    updater = Updater("1189228020:AAFPKveXq1dV_LuP8cCUQH81DR4rLdivgGQ")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('users_list', users_list))
    dp.add_handler(CommandHandler('broadcast', broadcast))
    dp.add_handler(CommandHandler('add_admin', want_admin))
    dp.add_handler(CommandHandler('del_admin', del_admin))
    dp.add_handler(CommandHandler('admins_list', list_admins))
    dp.add_handler(CommandHandler('users_file', users_file))

    text_handler = MessageHandler(Filters.text, actions)
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    Thread(target=heroku_life).start()

    while True:
        main()
