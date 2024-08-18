from telegram import Update
from telegram.ext import ContextTypes


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO сделать создание пользователя после регистрации
    # user, created = await User.objects.aget_or_create(
    #     pk=update.effective_user.id,
    #     username=update.effective_user.username,
    # )
    await update.message.reply_text("Hi!")
