from django.conf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from accounts.models import User
from species.models import Specie, SpeciePhoto


async def species_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем список антилокаций пользователю"""

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
        text="Выбери свою антилокацию",
        reply_markup=InlineKeyboardMarkup.from_column(buttons),
    )


async def specie_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение информации о антилокации"""

    query = update.callback_query
    await query.answer()

    _, specie_pk = query.data.split(":")

    specie: Specie = await Specie.objects.aget(pk=specie_pk)

    # async for media in SpeciePhoto.objects.filter(specie=specie_pk):
    #     if file_id := context.bot_data[media.photo.name]: 
    #         photo = file_id
    #     else:
    #         photo = await context.bot.get_file(media.photo)
    
    photos = [InputMediaPhoto(media=media.photo) async for media in SpeciePhoto.objects.filter(specie=specie_pk)]

    await update.effective_message.reply_media_group(
        media=photos,
        caption=f"<b>{specie.title}</b>\n\n{specie.description}",
        parse_mode=ParseMode.HTML,
    )

    await update.effective_message.reply_text(
        text=f"Свободных мест: {specie.participants_left}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(
                    f"{'🔒 ' if specie.participants_left == 0 else '' }Выбрать",
                    callback_data=f"choose_specie:{specie_pk}",
                ),
                # InlineKeyboardButton("Назад", callback_data="back:specie_list"),
            ],
        ),
    )


CHOOSE_SPECIE_SUCCESS= """
Поздравляем с выбором антилокации - {specie}!

Наш рейв состоится в самом центре Асперы, победит лишь один - а ты готов к тому, чтобы доказать, что именно твоя антилокация лучшая?

Встречаемся
📅5 сентября
🕑21:00
🏠Гриль-бар “The Rocks”
"""

async def choose_specie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор антилокации"""

    query = update.callback_query

    _, specie_pk = query.data.split(":")

    specie: Specie = await Specie.objects.aget(pk=specie_pk)
    user: User = await User.objects.aget(pk=update.effective_user.id)

    if specie.participants_left <= 0:
        return await query.answer("Нет свободных мест!", show_alert=True)

    if user.spacie_id is not None:
        return await query.answer("Ты уже выбрал свою антилокацию!", show_alert=True)

    user.spacie = specie
    specie.participants_left -= 1
    await user.asave()
    await specie.asave()

    await query.answer()
    await query.edit_message_reply_markup()
    await update.effective_message.reply_html(CHOOSE_SPECIE_SUCCESS.format(specie=specie.title))


HANDLERS = [
    MessageHandler(filters.Text(["Выбрать антилокацию"]), species_list),
    # CallbackQueryHandler(species_list, pattern="^back:specie_list"),
    CallbackQueryHandler(specie_detail, pattern="^specie_detail:"),
    CallbackQueryHandler(choose_specie, pattern="^choose_specie:"),
]
