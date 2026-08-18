import pymupdf
import os
from pathlib import Path
from datetime import datetime


def load_pdf(file_path: str) -> list:
    documents = []
    try:
        doc = pymupdf.open(file_path)
        file_name = Path(file_path).name
        print(f"Loading: {file_name} — {len(doc)} pages")

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text = " ".join(text.split()).replace("\x00", "").strip()

            if not text:
                continue

            document = {
                "content": text,
                "metadata": {
                    "document_name": file_name,
                    "document_type": detect_doc_type(file_name),
                    "page_number": page_num + 1,
                    "total_pages": len(doc),
                    "source": file_path,
                    "business_domain": detect_domain(file_name),
                    "loaded_at": datetime.now().isoformat()
                }
            }
            documents.append(document)

        doc.close()
        print(f"Extracted {len(documents)} pages from {file_name}")

    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        raise

    return documents


def detect_doc_type(file_name: str) -> str:
    file_name = file_name.lower()
    if "sop" in file_name:
        return "SOP"
    elif "policy" in file_name:
        return "POLICY"
    elif "guideline" in file_name:
        return "GUIDELINE"
    elif "regulatory" in file_name:
        return "REGULATORY"
    else:
        return "DOCUMENT"


def detect_domain(file_name: str) -> str:
    file_name = file_name.lower()
    if "motor" in file_name:
        return "Motor Insurance"
    elif "health" in file_name:
        return "Health Insurance"
    elif "claims" in file_name:
        return "Claims"
    elif "regulatory" in file_name:
        return "Regulatory"
    else:
        return "General"


def load_all_documents(data_dir: str = "data") -> list:
    all_documents = []
    data_path = Path(data_dir)
    pdf_files = list(data_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {data_dir}")
        return []

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        docs = load_pdf(str(pdf_file))
        all_documents.extend(docs)

    print(f"\nTotal pages extracted: {len(all_documents)}")
    return all_documents


if __name__ == "__main__":
    documents = load_all_documents("data")

    if documents:
        print("\n--- Sample Document ---")
        print(f"Content preview: {documents[0]['content'][:200]}")
        print(f"Metadata: {documents[0]['metadata']}")
