from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode
from accounts.models import User
from species.models import Specie


async def species_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем список рас пользователю"""

    buttons = []
    async for specie in Specie.objects.all():
        buttons.append(
            InlineKeyboardButton(
                specie.title, callback_data=f"specie_detail:{specie.pk}"
            )
        )

    func = update.effective_message.reply_text

    if query := update.callback_query:
        await query.answer()
        func = query.edit_message_text

    await func(
        text="Выбери свою расу",
        reply_markup=InlineKeyboardMarkup.from_column(buttons),
    )


async def specie_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о расе"""

    query = update.callback_query
    await query.answer()

    _, specie_pk = query.data.split(":")

    specie: Specie = await Specie.objects.aget(pk=specie_pk)
    await query.edit_message_text(
        text=f"<b>{specie.title}</b>\n\n{specie.description}\nСвободных мест: {specie.participants_left}",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(
                    f"{'🔒 ' if specie.participants_left == 0 else '' }Выбрать",
                    callback_data=f"choose_specie:{specie_pk}",
                ),
                InlineKeyboardButton("Назад", callback_data="back:specie_list"),
            ],
        ),
        parse_mode=ParseMode.HTML,
    )


async def choose_specie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор расы"""

    query = update.callback_query

    _, specie_pk = query.data.split(":")

    specie: Specie = await Specie.objects.aget(pk=specie_pk)
    user: User = await User.objects.aget(pk=update.effective_user.id)

    if specie.participants_left <= 0:
        return await query.answer("Нет свободных мест!", show_alert=True)

    if user.spacie_id is not None:
        return await query.answer("Ты уже выбрал свою расу!", show_alert=True)

    user.spacie = specie
    specie.participants_left -= 1
    await user.asave()
    await specie.asave()

    await query.answer()
    await query.edit_message_text(f"Ты выбрал расу: {specie.title}")
    await update.effective_message.reply_html("Поздравляю с выбором расы!")


HANDLERS = [
    MessageHandler(filters.Text(["Выбрать расу"]), species_list),
    CallbackQueryHandler(species_list, pattern="^back:specie_list"),
    CallbackQueryHandler(specie_detail, pattern="^specie_detail:"),
    CallbackQueryHandler(choose_specie, pattern="^choose_specie:"),
]
