import io
import json
import os
import zipfile

from google.protobuf.json_format import MessageToDict
from google.protobuf.duration_pb2 import Duration
from yandex.cloud.serverless.functions.v1.function_pb2 import Resources, Version
from yandex.cloud.serverless.functions.v1.function_service_pb2 import (
    CreateFunctionVersionMetadata,
    CreateFunctionVersionRequest,
)
from yandex.cloud.serverless.functions.v1.function_service_pb2_grpc import (
    FunctionServiceStub,
)
import yandexcloud


ycf_zip = io.BytesIO()
with zipfile.ZipFile(ycf_zip, "w") as zip_file:
    zip_file.write("requirements.txt")
    zip_file.write("bot.py")
    zip_file.write("ycf.py")

sdk = yandexcloud.SDK(service_account_key=json.loads(os.getenv("YC_SA_KEY")))
function_service = sdk.client(FunctionServiceStub)
duration = Duration()
duration.FromSeconds(3)
operation = function_service.CreateVersion(
    CreateFunctionVersionRequest(
        function_id="d4evksata88kls5vtpcb",
        runtime="python39",
        entrypoint="ycf.handler",
        resources=Resources(memory=134217728),
        execution_timeout=duration,
        service_account_id="aje8at9dccectav28113",
        content=ycf_zip.getvalue(),
        environment={
            "TELEGRAM_ADMIN_ID": os.getenv("TELEGRAM_ADMIN_ID"),
            "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
            "YC_TRIGGER_ID": os.getenv("YC_TRIGGER_ID"),
        },
    )
)
operation_result = sdk.wait_operation_and_get_result(
    operation,
    response_type=Version,
    meta_type=CreateFunctionVersionMetadata,
)
response = MessageToDict(operation_result.response)
del response["environment"]
print(json.dumps(response, indent=4))
