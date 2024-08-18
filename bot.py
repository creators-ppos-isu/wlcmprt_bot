#!/usr/bin/env python

import logging
import os

import django
from dotenv import load_dotenv
from telegram.ext import Application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_bot.settings")
django.setup()

# NOTE: мы не можем использовать модули до `django.setup()`
import accounts.router # noqa

logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    load_dotenv()

    application = Application.builder().token(os.getenv("TG_BOT_TOKEN")).build()

    application.add_handlers(accounts.router.HANDLERS)

    application.run_polling()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
