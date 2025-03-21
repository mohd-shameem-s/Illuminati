import os
import sys
import exifread
import PyPDF2
import docx
from PIL import Image
from datetime import datetime

# Function to extract metadata from images
def extract_image_metadata(image_path):
    print(f"\n📷 Extracting Metadata from Image: {image_path}")
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            print("\n📜 EXIF Data:")
            for tag, value in exif_data.items():
                print(f"   {tag}: {value}")

        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            print("\n📌 EXIF Read Metadata:")
            for tag, value in tags.items():
                print(f"   {tag}: {value}")

    except Exception as e:
        print(f"⚠️ Error extracting image metadata: {e}")

# Function to extract metadata from PDFs
def extract_pdf_metadata(pdf_path):
    print(f"\n📄 Extracting Metadata from PDF: {pdf_path}")
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata

            if metadata:
                print("\n📜 PDF Metadata:")
                for key, value in metadata.items():
                    print(f"   {key}: {value}")
            else:
                print("⚠️ No metadata found in the PDF.")

    except Exception as e:
        print(f"⚠️ Error extracting PDF metadata: {e}")

# Function to extract metadata from DOCX files
def extract_doc_metadata(doc_path):
    print(f"\n📑 Extracting Metadata from Document: {doc_path}")
    try:
        doc = docx.Document(doc_path)
        core_props = doc.core_properties

        print("\n📜 Document Metadata:")
        print(f"   Title: {core_props.title or 'N/A'}")
        print(f"   Author: {core_props.author or 'N/A'}")
        print(f"   Last Modified By: {core_props.last_modified_by or 'N/A'}")
        print(f"   Created Date: {core_props.created or 'N/A'}")
        print(f"   Modified Date: {core_props.modified or 'N/A'}")

    except Exception as e:
        print(f"⚠️ Error extracting document metadata: {e}")

# Main function
def extract_metadata(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File does not exist: {file_path}")
        return

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in [".jpg", ".jpeg", ".png"]:
        extract_image_metadata(file_path)
    elif file_extension == ".pdf":
        extract_pdf_metadata(file_path)
    elif file_extension == ".docx":
        extract_doc_metadata(file_path)
    else:
        print("❌ Unsupported file type!")

# Run script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_path = input("📂 Enter the full file path: ").strip()
    else:
        file_path = sys.argv[1]

    extract_metadata(file_path)
