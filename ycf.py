import json
import logging
import os
import yfinance

from aiogram import types
from aiogram.dispatcher.webhook import BaseResponse

from bot import prepare_dispatcher


async def trigger_handler(messages):
    dispatcher = prepare_dispatcher()
    trigger_id = os.getenv("YC_TRIGGER_ID")
    admin_id = int(os.getenv("TELEGRAM_ADMIN_ID"))
    price = yfinance.Ticker("RUB=X").info["regularMarketPrice"]
    for message in messages:
        if message["details"].get("trigger_id") == trigger_id:
            await dispatcher.bot.send_message(
                chat_id=admin_id,
                text=f"USD/RUB {price}",
            )
    return {"statusCode": 200}


async def http_handler(body):
    dispatcher = prepare_dispatcher()
    results = await dispatcher.process_update(types.Update.to_object(json.loads(body)))
    for result in results:
        if isinstance(result, BaseResponse):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(result.get_response()),
            }
    return {"statusCode": 200}


async def handler(event, _):
    logging.getLogger().setLevel(logging.INFO)

    messages = event.get("messages")
    if messages is not None:
        return await trigger_handler(messages)

    body = event.get("body")
    if body is not None:
        return await http_handler(body)

    return {"statusCode": 400}
