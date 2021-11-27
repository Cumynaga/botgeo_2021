# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

import geocode


# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    #print(update.message)
    print("Отправлено", update.message['chat']['first_name'], "ID", update.message['chat']['id'])
    print("=>", update.message.text)
    text = update.message.text
    if text.lower() in ["привет","здаров","hello"]:
        text = "И тебе привет мой аналоговый друг :)"
    update.message.reply_text(text)

# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")

def geomap(update, context):
    text = update.message.text
    print(update.message['chat']['first_name']," => Запрос на поиск карты по адресу", text)
    update.message.reply_text("Ищем карту по адресу "+text)
    coord = geocode.get_cord(text)
    if coord:
        content = geocode.get_map(coord)
        if content:
            context.bot.send_photo(update.message.chat_id,content, caption="Результат поиска")
    else:
        update.message.reply_text("Карты по адресу НЕТ")
        return




def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    print("Бот работает.....")
    TOKEN = "2119835383:AAGHs67DilRtN5GrxZNE2LWrljcPN8aRDVk"

    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    # text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик в диспетчере.

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("getmap", geomap))

    dp.add_handler(MessageHandler(Filters.text, echo))



    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
