from pydantic import BaseModel


class UploadedDocument(BaseModel):
    file_name: str
    file_type: str
    uploaded_by: str