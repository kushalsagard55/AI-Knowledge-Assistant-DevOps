from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from datetime import datetime
from bson import ObjectId
from app.db.mongodb import database
from app.services.document_service import extract_document_text
from app.services.document_service import save_uploaded_file
from app.rag.vector_store import build_vector_store
router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    supported_extensions = [
        ".pdf",
        ".docx",
        ".txt"
    ]

    extension = "." + file.filename.split(".")[-1].lower()

    if extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    existing_document = await database.documents.find_one(
        {
            "file_name": file.filename
        }
    )

    if existing_document:

        raise HTTPException(
            status_code=400,
            detail="This document has already been uploaded."
        )

    saved_file_path = save_uploaded_file(file)

    extracted_text = extract_document_text(saved_file_path)
    total_chunks = build_vector_store(extracted_text)
    document = {
        "file_name": file.filename,
        "file_path": saved_file_path,
        "document_text": extracted_text,
        "uploaded_at": datetime.utcnow(),
    }

    result = await database.documents.insert_one(document)

    return {
        "message": "Document uploaded successfully",
        "document_id": str(result.inserted_id),
        "characters": len(extracted_text),
        "chunks_created": total_chunks
    }

@router.get("/")
async def get_all_documents():

    documents = await database.documents.find(
        {},
        {
            "document_text": 0
        }
    ).to_list(length=100)

    for document in documents:
        document["_id"] = str(document["_id"])
        if "uploaded_at" in document:
            document["uploaded_at"] = document["uploaded_at"].strftime(
                "%d-%m-%Y %I:%M %p"
            )

    return {
        "total_documents": len(documents),
        "documents": documents
    }

@router.delete("/{document_id}")
async def delete_document(document_id: str):

    result = await database.documents.delete_one(
        {
            "_id": ObjectId(document_id)
        }
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document deleted successfully."
    }