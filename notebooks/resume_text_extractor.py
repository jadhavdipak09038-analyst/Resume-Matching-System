import os
import pdfplumber
import docx
from tqdm import tqdm

# Folder paths
input_folder = "resumes_raw"
output_folder = "resumes_text"

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Function to read PDF
def extract_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to read DOCX
def extract_docx_text(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Get all resume files
files = os.listdir(input_folder)

# Process each resume
for file in tqdm(files):

    file_path = os.path.join(input_folder, file)

    if file.endswith(".pdf"):
        text = extract_pdf_text(file_path)

    elif file.endswith(".docx"):
        text = extract_docx_text(file_path)

    else:
        continue

    output_file = os.path.join(
        output_folder,
        file.replace(".pdf", ".txt").replace(".docx", ".txt")
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)