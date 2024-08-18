from . import views
from telegram.ext import CommandHandler

HANDLERS = [CommandHandler("start", views.cmd_start)]
