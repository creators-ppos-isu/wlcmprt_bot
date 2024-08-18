from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from accounts.models import User
from species.models import Specie


async def species_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем список рас пользователю"""

    buttons = []
    async for specie in Specie.objects.all():
        buttons.append(InlineKeyboardButton(specie.title, callback_data=f'choose_specie:{specie.pk}'))
    
    await update.effective_message.reply_text(
        "Выбери свою расу",
        reply_markup=InlineKeyboardMarkup.from_column(buttons),
    )


HANDLERS = [
    MessageHandler(filters.Text(["Выбрать расу"]), species_list)
]
