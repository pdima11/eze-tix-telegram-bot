from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN


def start(update, context):
    user = update.message.from_user

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {user['first_name']}!")


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
