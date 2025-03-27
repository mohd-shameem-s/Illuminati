import os
import sys
import exifread
import PyPDF2
import docx
import olefile  # Required for .doc (older Word files)
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

# ANSI Escape Codes for Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

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
    print(f"\n{CYAN}📷 Extracting Metadata from Image:{RESET} {image_path}")
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            print(f"\n{YELLOW}📜 EXIF Data:{RESET}")
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if "Date" in tag_name and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                print(f"   {GREEN}{tag_name}:{RESET} {value}")

        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            if tags:
                print(f"\n{YELLOW}📌 EXIF Read Metadata:{RESET}")
                for tag, value in tags.items():
                    print(f"   {GREEN}{tag}:{RESET} {value}")

    except Exception as e:
        print(f"{RED}⚠️ Error extracting image metadata:{RESET} {e}")

# Function to extract metadata from PDFs
def extract_pdf_metadata(pdf_path):
    print(f"\n{CYAN}📄 Extracting Metadata from PDF:{RESET} {pdf_path}")
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata

            if metadata:
                print(f"\n{YELLOW}📜 PDF Metadata:{RESET}")
                for key, value in metadata.items():
                    print(f"   {GREEN}{key}:{RESET} {format_date(value)}")
            else:
                print(f"{RED}⚠️ No metadata found in the PDF.{RESET}")

    except Exception as e:
        print(f"{RED}⚠️ Error extracting PDF metadata:{RESET} {e}")

# Function to extract metadata from DOCX files
def extract_docx_metadata(docx_path):
    print(f"\n{CYAN}📑 Extracting Metadata from DOCX Document:{RESET} {docx_path}")
    try:
        doc = docx.Document(docx_path)
        core_props = doc.core_properties

        print(f"\n{YELLOW}📜 Document Metadata:{RESET}")
        print(f"   {GREEN}Title:{RESET} {core_props.title or 'N/A'}")
        print(f"   {GREEN}Author:{RESET} {core_props.author or 'N/A'}")
        print(f"   {GREEN}Last Modified By:{RESET} {core_props.last_modified_by or 'N/A'}")
        print(f"   {GREEN}Created Date:{RESET} {format_date(core_props.created)}")
        print(f"   {GREEN}Modified Date:{RESET} {format_date(core_props.modified)}")

    except Exception as e:
        print(f"{RED}⚠️ Error extracting DOCX metadata:{RESET} {e}")

# Function to extract metadata from DOC files (Older Microsoft Word)
def extract_doc_metadata(doc_path):
    print(f"\n{CYAN}📑 Extracting Metadata from DOC Document:{RESET} {doc_path}")
    try:
        ole = olefile.OleFileIO(doc_path)
        meta = ole.get_metadata()
        
        print(f"\n{YELLOW}📜 Document Metadata:{RESET}")
        print(f"   {GREEN}Title:{RESET} {meta.title or 'N/A'}")
        print(f"   {GREEN}Author:{RESET} {meta.author or 'N/A'}")
        print(f"   {GREEN}Last Saved By:{RESET} {meta.last_saved_by or 'N/A'}")
        print(f"   {GREEN}Created Date:{RESET} {format_date(meta.create_time)}")
        print(f"   {GREEN}Modified Date:{RESET} {format_date(meta.last_saved_time)}")

    except Exception as e:
        print(f"{RED}⚠️ Error extracting DOC metadata:{RESET} {e}")

# Main function
def extract_metadata(file_path):
    if not os.path.exists(file_path):
        print(f"{RED}❌ File does not exist:{RESET} {file_path}")
        return

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in [".jpg", ".jpeg", ".png"]:
        extract_image_metadata(file_path)
    elif file_extension == ".pdf":
        extract_pdf_metadata(file_path)
    elif file_extension == ".docx":
        extract_docx_metadata(file_path)
    elif file_extension == ".doc":
        extract_doc_metadata(file_path)
    else:
        print(f"{RED}❌ Unsupported file type!{RESET}")

# Run script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_path = input(f"{CYAN}📂 Enter the full file path:{RESET} ").strip()
    else:
        file_path = sys.argv[1]

    extract_metadata(file_path)

    input(f"\n{BLUE}💀 Press [ENTER] to return to the main menu...{RESET}\n")
