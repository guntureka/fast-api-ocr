from pydantic import BaseModel, HttpUrl


class SubmitVLExtractionTaskRequest(BaseModel):
    file_url: str
    file_name: str
    folder_id: str
    template_id: str


class GetVLExtractionResultRequest(BaseModel):
    task_id: str
