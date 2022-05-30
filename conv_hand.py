'''
Conversation Handler usage example with python-telegram-bot wrapper
It is just a test code written to understand how Conversation Handler concept works
Hope it helps someone

30.05.22
Written by Askhat Aubakirov
'''

import logging
import re
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s + %(levelname)s - %(message)s"
)

updater = Updater("TOKEN")
dispatcher = updater.dispatcher

STATE0, STATE1, STATE2, STATE3 = range(4)


def start(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup([["State 1", "State 2", "State 3"]], one_time_keyboard = True)
    update.message.reply_text(f"Hello, {update.effective_user.first_name} \n Please choose the state you want to try:",
        reply_markup = reply_markup,
    )

    return STATE0

def choosing_state(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() in ["state 1"]:
        update.message.reply_text("this is state 1")
        return STATE1
    elif update.message.text.lower() in ["state 2"]:
        update.message.reply_text("this is state 2")
        return STATE2
    elif update.message.text.lower() in ["state 3"]:
        update.message.reply_text("this is state 3")
        return STATE3

def state1(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"You've chosen {update.message.text}. I now return you STATE0")
    return STATE0

def state2(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"You've chosen {update.message.text}. I now return you STATE0")
    return STATE0

def state3(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"You've chosen {update.message.text}. I now return you STATE0")
    return STATE0

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(f"It was a good test. Bye then!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

choice_regex = re.compile(r"^(State 1|State 2|State 3)$", re.IGNORECASE)

handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        STATE0: [MessageHandler(Filters.regex(choice_regex), choosing_state)],
        STATE1: [MessageHandler(Filters.regex(choice_regex), state1)],
        STATE2: [MessageHandler(Filters.regex(choice_regex), state2)],
        STATE3: [MessageHandler(Filters.regex(choice_regex), state3)],
    },
    fallbacks= [CommandHandler("cancel", cancel)],
)

dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()
