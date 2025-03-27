import os
import exifread
import PyPDF2
import olefile
import docx
from PIL import Image
from PIL.ExifTags import TAGS

# ANSI color codes
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"

def extract_image_metadata(file_path):
    """Extract metadata from image files (JPEG, PNG)."""
    print(f"\n📷 {BOLD}{CYAN}Extracting Metadata from Image:{RESET} {file_path}")

    try:
        with open(file_path, "rb") as img_file:
            tags = exifread.process_file(img_file)
        
        if not tags:
            print(f"{YELLOW}[⚠] No EXIF metadata found.{RESET}")
        else:
            for tag, value in tags.items():
                print(f"  {GREEN}{tag}:{RESET} {value}")

        # Using PIL for additional metadata
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data:
            print(f"\n{BOLD}{BLUE}📌 Additional Metadata:{RESET}")
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                print(f"  {GREEN}{tag}:{RESET} {value}")

    except Exception as e:
        print(f"{RED}[❌] Error extracting image metadata: {e}{RESET}")

def extract_pdf_metadata(file_path):
    """Extract metadata from PDF files."""
    print(f"\n📄 {BOLD}{CYAN}Extracting Metadata from PDF:{RESET} {file_path}")

    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            metadata = reader.metadata

        if metadata:
            print(f"\n{BOLD}{BLUE}📌 PDF Metadata:{RESET}")
            for key, value in metadata.items():
                print(f"  {GREEN}{key.replace('/', '')}:{RESET} {value}")
        else:
            print(f"{YELLOW}[⚠] No metadata found in PDF.{RESET}")

    except Exception as e:
        print(f"{RED}[❌] Error extracting PDF metadata: {e}{RESET}")

def extract_doc_metadata(file_path):
    """Extract metadata from Word documents (.docx, .doc)."""
    print(f"\n📜 {BOLD}{CYAN}Extracting Metadata from Word Document:{RESET} {file_path}")

    if file_path.lower().endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            metadata = doc.core_properties

            print(f"\n{BOLD}{BLUE}📌 Word Document Metadata:{RESET}")
            print(f"  {GREEN}Title:{RESET} {metadata.title}")
            print(f"  {GREEN}Author:{RESET} {metadata.author}")
            print(f"  {GREEN}Created:{RESET} {metadata.created}")
            print(f"  {GREEN}Last Modified:{RESET} {metadata.modified}")
            print(f"  {GREEN}Subject:{RESET} {metadata.subject}")

        except Exception as e:
            print(f"{RED}[❌] Error extracting DOCX metadata: {e}{RESET}")

    elif file_path.lower().endswith(".doc"):
        try:
            ole = olefile.OleFileIO(file_path)
            meta = ole.get_metadata()

            print(f"\n{BOLD}{BLUE}📌 DOC File Metadata:{RESET}")
            print(f"  {GREEN}Title:{RESET} {meta.title}")
            print(f"  {GREEN}Author:{RESET} {meta.author}")
            print(f"  {GREEN}Created:{RESET} {meta.create_time}")
            print(f"  {GREEN}Last Saved By:{RESET} {meta.last_saved_by}")
            print(f"  {GREEN}Last Modified:{RESET} {meta.last_saved_time}")

        except Exception as e:
            print(f"{RED}[❌] Error extracting DOC metadata: {e}{RESET}")

def extract_metadata(file_path):
    """Determine the file type and extract metadata accordingly."""
    if not os.path.exists(file_path):
        print(f"{RED}[❌] File not found: {file_path}{RESET}")
        return

    print(f"\n📂 {BOLD}{CYAN}Analyzing File:{RESET} {file_path}")

    if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        extract_image_metadata(file_path)
    elif file_path.lower().endswith(".pdf"):
        extract_pdf_metadata(file_path)
    elif file_path.lower().endswith((".docx", ".doc")):
        extract_doc_metadata(file_path)
    else:
        print(f"{YELLOW}[⚠] Unsupported file format.{RESET}")

# Main script execution
if __name__ == "__main__":
    file_path = input(f"{CYAN}📂 Enter the full file path: {RESET}").strip()

    if file_path:
        extract_metadata(file_path)
    else:
        print(f"{RED}[❌] No file path entered!{RESET}")
