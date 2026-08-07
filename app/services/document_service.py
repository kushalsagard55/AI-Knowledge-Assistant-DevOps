from pathlib import Path

from docx import Document
from pypdf import PdfReader

UPLOAD_FOLDER = "uploads"


def save_uploaded_file(uploaded_file):

    Path(UPLOAD_FOLDER).mkdir(
        exist_ok=True
    )

    file_path = Path(UPLOAD_FOLDER) / uploaded_file.filename

    with open(file_path, "wb") as destination_file:
        destination_file.write(uploaded_file.file.read())

    return str(file_path)


def read_pdf(file_path: str):

    pdf_reader = PdfReader(file_path)

    document_text = ""

    print("=" * 60)
    print("Reading PDF:", file_path)

    for page_number, page in enumerate(pdf_reader.pages):

        page_text = page.extract_text()

        characters = len(page_text or "")

        print(f"Page {page_number + 1}: {characters} characters")

        if page_text:
            document_text += page_text + "\n"

    print("=" * 60)
    print("Total Extracted Characters:", len(document_text))
    print("=" * 60)

    return document_text


def read_docx(file_path: str):

    document = Document(file_path)

    document_text = ""

    for paragraph in document.paragraphs:
        document_text += paragraph.text + "\n"

    return document_text


def read_text_file(file_path: str):

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return file.read()


def extract_document_text(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    if extension == ".docx":
        return read_docx(file_path)

    if extension == ".txt":
        return read_text_file(file_path)

    raise Exception("Unsupported document type.")