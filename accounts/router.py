from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from accounts.models import User

FULL_NAME = 0
CHOOSE_SPECIE_REPLY_MARKUP = ReplyKeyboardMarkup.from_button(
    KeyboardButton("Выбрать антилокацию"), resize_keyboard=True
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Афиша мероприятия", reply_markup=CHOOSE_SPECIE_REPLY_MARKUP
    )

    if not await User.objects.filter(pk=update.effective_user.id).aexists():
        await update.message.reply_text("Для начала укажи свое ФИО")
        return FULL_NAME


async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка правильно введенного ФИО"""

    last_name, first_name, middle_name = update.message.text.strip().split(maxsplit=3)

    await User.objects.aupdate_or_create(
        pk=update.effective_user.id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "username": update.effective_user.username or update.effective_user.id,
        },
    )

    await update.message.reply_text(
        f"Приятно познакомиться, {first_name}!",
        reply_markup=CHOOSE_SPECIE_REPLY_MARKUP,
    )
    return ConversationHandler.END


async def wrong_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("ФИО имеет неверный формат")
    return FULL_NAME


HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            FULL_NAME: [
                MessageHandler(
                    filters.Regex(r"^[А-ЯЁа-яё]+(?: [А-ЯЁа-яё]+){2}$"), full_name
                ),
                MessageHandler(filters.TEXT, wrong_full_name),
            ],
        },
        fallbacks=[CommandHandler("cancel", cmd_start)],
    ),
]
