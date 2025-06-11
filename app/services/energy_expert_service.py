import json

from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_energyexpertexternal20220923 import models as EnergyExpertModel
from alibabacloud_energyexpertexternal20220923.client import (
    Client as EnergyExpertClient,
)
from alibabacloud_tea_openapi import models as open_api_models

from app.core.config import settings
from app.models.energy_expert import (
    GetVLExtractionResultRequest,
    SubmitVLExtractionTaskRequest,
)


def create_client() -> EnergyExpertClient:
    credential = CredentialClient()
    config = open_api_models.Config(credential=credential)
    config.access_key_id = settings.ALIBABA_CLOUD_ACCESS_KEY_ID
    config.access_key_secret = settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET
    config.endpoint = settings.ALIBABA_ENERGY_EXPERT_ENDPOINT
    return EnergyExpertClient(config)


async def submit_vlextraction_task_service(payload: SubmitVLExtractionTaskRequest):
    client = create_client()
    request = EnergyExpertModel.SubmitVLExtractionTaskRequest(
        file_url=payload.file_url,
        file_name=payload.file_name,
        folder_id=payload.folder_id,
        template_id=payload.template_id,
    )

    result = await client.submit_vlextraction_task_async(request)
    return result.body.to_map()


async def get_vlextraction_result_service(payload: GetVLExtractionResultRequest):
    client = create_client()
    request = EnergyExpertModel.GetVLExtractionResultRequest(task_id=payload.task_id)

    result = await client.get_vlextraction_result_async(request)
    data = result.body.to_map()

    kv_list_info = data.get("data", {}).get("kvListInfo", [])

    parsed_items = []
    for item in kv_list_info:
        key_value_str = item.get("keyValue", "")

        # Bersihkan escape character jika perlu
        key_value_str = key_value_str.strip()

        try:
            key_value_dict = json.loads(key_value_str)

            # Normalisasi key: lowercase, spasi → underscore
            normalized_dict = {
                key.strip().lower().replace(" ", "_"): value
                for key, value in key_value_dict.items()
            }

            parsed_items.append(normalized_dict)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            continue  # Skip kalau error JSON

    return parsed_items
