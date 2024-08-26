from django.conf import settings
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


POSTER_TEXT = """
2475 год. Из-за тоталитарного режима действующего правительства - президента Игнис, общество столкнулось с неравенством социальных групп, начались протесты и угнетение некоторых слоев населения, вследствие чего страна Аспера, будучи полноценным государством, начала распадаться на области, называемые “Антилокациями”, жители которых стали объединяться и формировать свой менталитет, стараясь занять свое место под Солнцем. 

Жители каждой антилокации обладают уникальным характером, стилем одежды и миссией, всего их 7:
Девиты - приближенная к Президенту элита общества
Элиноры - разбойники-ассасины, бывшие дворецкие Президента
Люминеры - звездочеты и оракулы
Сефиры - номады и жители пустынных долин
Кондуиты - русалы и сирены морских побережий
Мераморцы - люди, имеющие духовную связь с природой и лесом
Либера - свободолюбивые кочевые потомки ковбоев

<b>Для того, чтобы принять участие в рейве, нажми на кнопку ниже, чтобы выбрать свою антилокацию⬇️</b>

<b>‼️ВНИМАНИЕ: выбирайте с умом, ведь от того, какую антилокацию вы выберете - будет зависеть ваш дресс-код на тусовку!</b>
"""


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=settings.BASE_DIR / "static/" / "images/" / "poster.jpg",
        reply_markup=CHOOSE_SPECIE_REPLY_MARKUP,
    )
    await update.message.reply_html(text=POSTER_TEXT)

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
