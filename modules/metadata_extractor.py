import os
import sys
import exifread
import PyPDF2
import docx
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

# Function to format dates correctly
def format_date(timestamp):
    if isinstance(timestamp, str) and timestamp.startswith("D:"):
        try:
            return datetime.strptime(timestamp[2:16], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return timestamp  # Return as is if parsing fails
    elif isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return "Unknown"

# Function to extract metadata from images
def extract_image_metadata(image_path):
    print(f"\n📷 Extracting Metadata from Image: {image_path}")
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            print("\n📜 EXIF Data:")
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if "Date" in tag_name and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass  # Keep original value if parsing fails
                print(f"   {tag_name}: {value}")

        # Extract metadata using exifread
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            if tags:
                print("\n📌 EXIF Read Metadata:")
                for tag, value in tags.items():
                    if "Date" in tag:
                        try:
                            value = datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass  # Keep original value if parsing fails
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
                    if "date" in key.lower():
                        value = format_date(value)
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
        print(f"   Created Date: {format_date(core_props.created)}")
        print(f"   Modified Date: {format_date(core_props.modified)}")

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
