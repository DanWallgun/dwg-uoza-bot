import os
import random
import uuid

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage, AnswerInlineQuery


async def echo(message: types.Message):
    return SendMessage(message.chat.id, message.as_json())


async def inline_random_case(inline_query: types.InlineQuery):
    transform = lambda text: "".join(
        [
            character.upper() if random.getrandbits(1) else character
            for character in text.lower()
        ]
    )
    transformed_text = transform(inline_query.query)
    return AnswerInlineQuery(
        inline_query_id=inline_query.id,
        results=[
            types.InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Random case",
                description=transformed_text,
                input_message_content=types.InputTextMessageContent(transformed_text),
            )
        ],
    )


def prepare_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(Bot(os.getenv("TELEGRAM_BOT_TOKEN")))
    dispatcher.setup_middleware(LoggingMiddleware())
    dispatcher.register_message_handler(echo)
    dispatcher.register_inline_handler(inline_random_case)
    return dispatcher
