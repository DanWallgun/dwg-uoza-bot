import json

from aiogram import types
from aiogram.dispatcher.webhook import BaseResponse

from bot import prepare_dispatcher


async def handler(event, _):
    if event["httpMethod"] != "POST":
        return {"statusCode": 400}

    dispatcher = prepare_dispatcher()
    results = await dispatcher.process_update(
        types.Update.to_object(json.loads(event["body"]))
    )
    for result in results:
        if isinstance(result, BaseResponse):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(result.get_response()),
            }
    return {"statusCode": 200}
