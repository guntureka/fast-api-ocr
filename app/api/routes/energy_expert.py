import asyncio

from fastapi import APIRouter, HTTPException

from app.models.energy_expert import (
    GetVLExtractionResultRequest,
    SubmitVLExtractionTaskRequest,
)
from app.services.energy_expert_service import (
    get_vlextraction_result_service,
    submit_vlextraction_task_service,
)

router = APIRouter(prefix="/energy-expert", tags=["Energy Expert"])


@router.post("/submit-vlextraction-task")
async def submit_vlextraction_task(payload: SubmitVLExtractionTaskRequest):
    try:
        return await submit_vlextraction_task_service(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-vlextraction-result")
async def get_vlextraction_task(payload: GetVLExtractionResultRequest):
    try:
        return await get_vlextraction_result_service(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit-and-get-vlextraction-result")
async def submit_and_get_vlextraction_result(payload: SubmitVLExtractionTaskRequest):
    try:
        submit_result = await submit_vlextraction_task_service(payload)
        task_id = submit_result.get("data", {}).get("taskId")
        if not task_id:
            raise HTTPException(
                status_code=500, detail="No task_id returned from submit."
            )

        for _ in range(3):
            await asyncio.sleep(15)
            get_payload = GetVLExtractionResultRequest(task_id=task_id)
            result = await get_vlextraction_result_service(get_payload)

            if result:
                return result

        raise HTTPException(status_code=408, detail="Timeout waiting for result.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
